# importing libraries
import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import chromedriver_binary
import json

# accessing the browser


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

    profile = url
    browser.get(profile)

    full_height = browser.execute_script('return document.body.scrollHeight')
    cur_height = browser.execute_script('return window.innerHeight')

    data = dict()

    # ---------------------------------------------------------- #

    while cur_height <= full_height:
        sleep(10)
        # about expand
        try:
            button = browser.find_element_by_xpath("//button[@class='inline-show-more-text__button inline-show-more-text__button--light link']")
            browser.execute_script("arguments[0].click();", button)
        except Exception as e:
            pass
        # experience expand
        try:
            button = browser.find_element_by_xpath("//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted']")
            browser.execute_script("arguments[0].click();", button)
        except Exception as e:
            pass
        # skills expand
        try:
            button = browser.find_element_by_xpath("//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid artdeco-button--muted']")
            browser.execute_script("arguments[0].click();", button)
        except Exception as e:
            pass
        # see more buttons expand
        try:
            button = browser.find_element_by_xpath("//button[@class='inline-show-more-text__buttond']")
            browser.execute_script("arguments[0].click();", button)
        except Exception as e:
            pass
        # accomplishments expand
        try:
            button = browser.find_element_by_xpath("//button[@class='pv-accomplishments-block__expand artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")
            browser.execute_script("arguments[0].click();", button)
        except Exception as e:
            pass

        browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
        cur_height += cur_height

    src = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()

    # ------------------------------------------ #

    # GET BASIC INFO
    try:
        BASIC = src.find_all("div", {"class": "pv-text-details__left-panel"})[0]
        basic_obj = dict()
        basic_obj["Name"] = BASIC.find("h1").get_text().strip()
        basic_obj["Headline"] = BASIC.find("div", {"class": "text-body-medium"}).get_text().strip()
        basic_obj["Location"] = BASIC.find("span", {"class": "text-body-small"}).get_text().strip()
        data["profile"] = basic_obj
    except Exception as e:
        pass

    # GET ABOUT INFO
    try:
        ABOUT = src.find_all("section",{"class":'pv-about-section'})[0].get_text().split("   ")[-1].strip()
        if(ABOUT != 'About'):
            data["about"] = ABOUT
    except Exception as e:
        pass

    # GET EDUCATIONAL INFO
    try:
        EDUCATION = src.find_all("section",{"id":'education-section'})[0]
        Eds = EDUCATION.find_all("li")
        Educations = []
        for i in range(len(Eds)):
            ed = dict()
            if(Eds[i].find("h3")):
                Institute = Eds[i].find("h3").get_text().strip()
                ed["Institute"] = Institute

            OtherInfo = Eds[i].find_all("p")
            for j in range(len(OtherInfo)):
                ed[OtherInfo[j].find_all("span")[0].get_text().strip(
                )] = OtherInfo[j].find_all("span")[1].get_text().strip()

            Educations.append(ed)
        data["education"] = Educations
    except Exception as e:
        pass

    # GET EXPERIENCES
    try:
        EXPERIENCE = src.find_all("section",{"id":'experience-section'})[0]
        Exs = EXPERIENCE.find_all("li", {"class":"pv-profile-section__list-item"})
        Experiences = []
        for i in range(len(Exs)):
            exp = dict()
            if(len(Exs[i].find_all("ul")) > 0):
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
                        if(len(sp)>1):
                            exp1[sp[0].get_text().strip()] = sp[1].get_text().strip()
                    for k in range(len(dt2)):
                        sp = dt2[k].find_all("span")
                        if(len(sp)>1):
                            exp1[sp[0].get_text().strip()] = sp[1].get_text().strip()
                    exp1_arr.append(exp1)
                exp['Roles'] = exp1_arr

            else:
                # heading
                exp['Role'] = Exs[i].find("h3").get_text().strip()
                dataList = Exs[i].find_all("h4")
                # other data
                for j in range(len(dataList)):
                    exp[dataList[j].find_all("span")[0].get_text().strip(
                    )] = dataList[j].find_all("span")[1].get_text().strip()
                # company name
                exp[Exs[i].find_all("p")[0].get_text().strip()] = Exs[i].find_all("p")[
                    1].get_text().strip().split("\n")[0]
            # adding to list
            Experiences.append(exp)
        data["experience"] = Experiences
    except Exception as e:
        pass

    # GET VOLUNTEER
    try:
        VOLUNTEER = src.find_all("section",{"class":'volunteering-section'})[0]
        Vls = VOLUNTEER.find_all("li")
        Volunteers = []
        for i in range(len(Vls)):
            vl = {
                "Title": "",
                "Description": ""
            }
            vl["Title"] = Vls[i].find_all("h3")[0].get_text().strip()
            vl["Description"] = Vls[i].find_all("p")[0].get_text().strip()
            h4s = Vls[i].find_all("h4")
            for j in range(len(h4s)):
                spans = h4s[j].find_all("span")
                vl[spans[0].get_text().strip()] = spans[1].get_text().strip()
            Volunteers.append(vl)
        data["volunteer"] = Volunteers
    except Exception as e:
        pass

    # GET SKILLS
    try:
        SKILLS =  src.find_all("section",{"class":'pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view'})[0]
        all_skills = SKILLS.find_all("span", {"class": "pv-skill-category-entity__name-text t-16 t-black t-bold"})
        my_skills = []
        for i in range(len(all_skills)):
            my_skills.append(all_skills[i].get_text().strip())
        data["skills"] = my_skills
    except Exception as e:
        pass

    json_object = json.dumps(data, indent=4)
    return(json_object)

# data = scraping("https://www.linkedin.com/in/ishita-kabra-3b305818b/")
# print(data)
