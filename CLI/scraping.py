#importing libraries
import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import chromedriver_binary
import json

#accessing the browser
def scraping(url):    
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

    profile=url
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

    while cur_height<=full_height:
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

        #get skills 
        
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
        if(ABOUT != 'About'):
            data["about"] = ABOUT
    except Exception as e:
        pass
    
    #GET EDUCATIONAL INFO
    try:
        EDUCATION = BeautifulSoup(education, "lxml")
        Eds = EDUCATION.find_all("li")
        Educations = []
        for i in range(len(Eds)):
            ed = dict()
            if(Eds[i].find("h3")):
                Institute = Eds[i].find("h3").get_text().strip()
                ed["Institute"] = Institute

            OtherInfo = Eds[i].find_all("p")
            for j in range(len(OtherInfo)):
                ed[OtherInfo[j].find_all("span")[0].get_text().strip()] = OtherInfo[j].find_all("span")[1].get_text().strip()      
        
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
            exp = dict()
            
            if(len(Exs[i].find_all("ul")) >0):
                # case with multiple roles
                exp['Company Name'] = Exs[i].find_all("h3")[0].find_all("span")[1].get_text().strip()
                roles = Exs[i].find_all("li")
                exp1_arr = []
                for j in range(len(roles)):
                    dt1 = roles[j].find_all("h3")
                    dt2 = roles[j].find_all("h4")
                    exp1 = dict()
                    for k in range(len(dt1)):
                        sp = dt1[k].find_all("span")
                        exp1[sp[0].get_text().strip()] = sp[1].get_text().strip()
                    for k in range(len(dt2)):
                        sp = dt2[k].find_all("span")
                        exp1[sp[0].get_text().strip()] = sp[1].get_text().strip()
                    exp1_arr.append(exp1)
                exp['Roles'] = exp1_arr

            else:
                # heading
                exp['Role'] = Exs[i].find("h3").get_text().strip()
                dataList = Exs[i].find_all("h4")
                # other data
                for j in range(len(dataList)):
                    exp[dataList[j].find_all("span")[0].get_text().strip()] = dataList[j].find_all("span")[1].get_text().strip()
                # company name
                exp[Exs[i].find_all("p")[0].get_text().strip()] = Exs[i].find_all("p")[1].get_text().strip().split("\n")[0]
            
            # adding to list
            Experiences.append(exp)  
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
    
    # GET SKILLS
    # try:
    #     SKILLS =  BeautifulSoup(skills, "lxml")
    #     print(SKILLS)
    # except Exception as e:
    #     pass

    return(data)

# data = scraping("https://www.linkedin.com/in/paige-liwanag/")
data = scraping("https://www.linkedin.com/in/ishita-kabra-3b305818b/")

json_object = json.dumps(data, indent = 4)  
print(json_object)

# TODOs: 
# 1. look for button clicks in the main scraping script
# 2. add skills
