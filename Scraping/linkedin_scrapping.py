#importing libraries
import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_binary
import json

#accessing the browser
def scraping():    
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    caps = options.to_capabilities()
    browser = webdriver.Chrome(desired_capabilities=caps)
    browser.maximize_window()
    browser.get('https://www.linkedin.com/uas/login')
    files = open('config.txt')
    lines = files.readlines()
    username = lines[0]
    password = lines[1]

    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    profile='https://www.linkedin.com/in/paige-liwanag/'
    browser.get(profile)

    full_height = browser.execute_script('return document.body.scrollHeight');
    cur_height = browser.execute_script('return window.innerHeight');

    data = {}
    basic = ""
    about = ""
    education= ""
    experience= ""
    volunteer = ""

    # ---------------------------------------------------------- #

    while cur_height<full_height:
        sleep(10)
        
        #get basics
        try:
            if(basic == ''):
                exp = browser.find_elements_by_class_name('pv-text-details__left-panel')
                if(exp):
                    basic = exp[0].get_attribute('innerHTML')
        except Exception as e:
            pass
    
        #get about
        try:
            if(about == ''):
                exp = browser.find_elements_by_class_name('pv-about-section')
                if(exp):
                    button = exp[0].find_elements_by_css_selector('button')
                    if(len(button)>=1):
                        button[0].click()
                    exp_new = browser.find_elements_by_class_name('pv-about-section')
                    about = exp_new[0].get_attribute('innerHTML')
        except Exception as e:
            pass
        
        #get experience 
        try:
            if(experience == ''):
                exp = browser.find_element_by_id('experience-section')
                if(exp):
                    experience = exp.get_attribute('innerHTML')
        except Exception as e:
            pass
    
        
        #get education 
        try:
            if(education == ''):
                exp = browser.find_element_by_id('education-section')
                if(exp):
                    education = exp.get_attribute('innerHTML')
        except Exception as e:
            pass
        
        
        #get volunteer 
        try:
            if(volunteer == ''):
                exp = browser.find_elements_by_class_name('volunteering-section')
                if(exp):
                    volunteer = exp[0].get_attribute('innerHTML')
        except Exception as e:
            pass

        browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
        cur_height+=cur_height


    browser.close()

    # ----------------------------------------- #

    #GET BASIC INFO
    try:
        basic_obj = {
        "Name": "",
        "Headline": "",
        "Location": "",
        }
        BASIC = BeautifulSoup(basic, "lxml")
        if(BASIC.find("h1")):
            basic_obj["Name"] = BASIC.find("h1").get_text().strip()
        if(BASIC.find_all("div", class_="text-body-medium")):
            basic_obj["Headline"] = BASIC.find_all("div", class_="text-body-medium")[0].get_text().strip()
        if(BASIC.find_all("span", class_="text-body-small")): 
            basic_obj["Location"] = BASIC.find_all("span", class_="text-body-small")[0].get_text().strip()
        data["profile"]=basic_obj
    except Exception as e:
        pass

    #GET ABOUT INFO
    try:
        ABOUT = BeautifulSoup(about, "lxml").get_text().split("   ")[-1].strip()
        data["about"] = ABOUT
    except Exception as e:
        pass
    
    #GET EDUCATIONAL INFO
    try:
        EDUCATION = BeautifulSoup(education, "lxml")
        Eds = EDUCATION.find_all("li")
        Educations = []
        for i in range(len(Eds)):
            ed = {
                "Institute":"",
                "Degree":"",
                "Time":"",
                "Branch":""
                }
            if(Eds[i].find("h3")):
                Institute = Eds[i].find("h3").get_text().strip()
                ed["Institute"] = Institute
                
            if(len(Eds[i].find_all("span"))>1):
                Degree = Eds[i].find_all("span")[1].get_text().strip()
                ed["Degree"] = Degree  
                
            if(len(Eds[i].find_all("time"))>1):
                Time = Eds[i].find_all("time")[0].get_text().strip()+"-"+Eds[i].find_all("time")[1].get_text().strip()
                ed["Time"] = Time  
                
            if(len(Eds[i].find_all("span"))>3):
                Branch = Eds[i].find_all("span")[3].get_text().strip()
                ed["Branch"] = Branch   
            Educations.append(ed)
        data["education"]=Educations
    except Exception as e:
        pass

    #GET EXPERIENCES
    try:
        EXPERIENCE = BeautifulSoup(experience, "lxml")
        Exs = EXPERIENCE.find_all("li", class_="pv-profile-section__list-item")
        Experiences = []
        for i in range(len(Exs)):
            lis = Exs[i].find_all("li")
            if(len(lis)>0): #case with roles
                ex = {
                "Company":"",
                "Duration":"",
                "Roles":[]
                }
                spans = Exs[i].find_all("span")
                if(len(spans)>=2):
                    ex["Company"] = spans[1].get_text().strip()
                if(len(spans)>=4):
                    ex["Duration"] = spans[3].get_text().strip()
                for j in range(len(lis)):
                    role = {
                    "Title":"",
                    "Dates":"",
                    "Duration":"",
                    "Location":""
                    }
                    spans_in = lis[j].find_all("span")
                    role["Title"] = spans_in[2].get_text().strip()
                    if(len(spans_in)>=5):
                        role["Dates"] = spans_in[4].get_text().strip()
                    if(len(spans_in)>=7):
                        role["Duration"] = spans_in[6].get_text().strip()
                    if(len(spans_in)>=9):
                        role["Location"] = spans_in[8].get_text().strip()
                    ex["Roles"].append(role)
                Experiences.append(ex)
            else: #case without roles
                ex = {
                    "Role":"",
                    "Company":"",
                    "Job_Type":"",
                    "Dates":"",
                    "Duration":"",
                    "Location":""
                }
                spans_2 = Exs[i].find_all("span")
                if(Exs[i].find_all("h3")[0]):
                    ex["Role"] = Exs[i].find_all("h3")[0].get_text().strip()
                if(len(Exs[i].find_all("p"))>=2):
                    ex["Company"] = Exs[i].find_all("p")[1].get_text().strip().split("\n")[0]
                if(len(spans_2)>=1):
                    ex["Job_Type"] = spans_2[0].get_text().strip()
                if(len(spans_2)>=3):
                    ex["Dates"] = spans_2[2].get_text().strip()
                if(len(spans_2)>=5):
                    ex["Duration"] = spans_2[4].get_text().strip()
                if(len(spans_2)>=7):
                    ex["Location"] = spans_2[6].get_text().strip()
                Experiences.append(ex)   
        data["experience"]=Experiences
    except Exception as e:
        pass

    #GET VOLUNTEER
    try:
        VOLUNTEER = BeautifulSoup(volunteer, "lxml")
        Vls = VOLUNTEER.find_all("li")
        Volunteers = []
        for i in range(len(Vls)):
            vl = {
                "Title":"",
                "Description":""
            }
            vl["Title"]=Vls[i].find_all("h3")[0].get_text().strip()
            vl["Description"] = Vls[i].find_all("p")[0].get_text().strip()
            h4s = Vls[i].find_all("h4")
            for j in range(len(h4s)):
                spans = h4s[j].find_all("span")
                vl[spans[0].get_text().strip()]=spans[1].get_text().strip()
            Volunteers.append(vl)
        data["volunteer"]=Volunteers
    except Exception as e:
        pass
    
    return(data)

data = scraping()

json_object = json.dumps(data, indent = 4)  
print(json_object)

# to do: fix the displacement bug 
# do it like volunteer wherever possible
