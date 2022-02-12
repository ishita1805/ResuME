# importing libraries
from filecmp import dircmp
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import json
import os


def scraping(email,password,url,github):

    # accessing the browser
    # conf_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    options = ChromeOptions()
    options.add_argument("--incognito")
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("http://www.python.org")
    assert "Python" in browser.title
    browser.maximize_window()
    browser.get('https://www.linkedin.com/uas/login')
    # files = open(conf_path)
    # lines = files.readlines()
    # username = lines[0]
    # password = lines[1]

    elementID = browser.find_element_by_id('username')
    elementID.send_keys(email)
    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    profile = url
    browser.get(profile)

    full_height = browser.execute_script('return document.body.scrollHeight')
    cur_height = browser.execute_script('return window.innerHeight')


    skills = False
    about = False
    exper = False
    more = False
    accomp = False
    

    data = dict()

    # ---------------------------------------------------------- #

    while cur_height <= full_height:
        sleep(15)
        # about expand
        try:
            if(about == False):    
                button = browser.find_element_by_xpath("//button[@class='inline-show-more-text__button inline-show-more-text__button--light link']")
                browser.execute_script("arguments[0].click();", button)
                about = True
        except Exception as e:
            pass
        # experience expand
        try:
            if(exper == False):
                button = browser.find_element_by_xpath("//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle artdeco-button artdeco-button--tertiary artdeco-button--muted']")
                browser.execute_script("arguments[0].click();", button)
                exper = True
        except Exception as e:
            pass
        # skills expand
        try:
            if(skills == False):
                button = browser.find_element_by_xpath("//button[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid artdeco-button--muted']")
                browser.execute_script("arguments[0].click();", button)
                skills = True
        except Exception as e:
            pass
        # see more buttons expand
        try:
            if(more == False):
                button = browser.find_element_by_xpath("//button[@class='inline-show-more-text__buttond']")
                browser.execute_script("arguments[0].click();", button)
                more = True
        except Exception as e:
            pass
        # accomplishments expand
        try:
            if(accomp == False):
                button = browser.find_element_by_xpath("//button[@class='pv-accomplishments-block__expand artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view']")
                browser.execute_script("arguments[0].click();", button)
                accomp = True
        except Exception as e:
            pass

        browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
        cur_height += cur_height

    src = BeautifulSoup(browser.page_source, 'lxml')

    # ---------------------------------------------------------- #

    # GET BASIC INFO
    try:
        BASIC = src.find_all("section",{ "class": ["artdeco-card", "ember-view", "pv-top-card"] })[0]
        basic_obj = dict()
        basic_obj["name"] = BASIC.find("h1").get_text().strip()
        basic_obj["headline"] = BASIC.find("div", {"class": "text-body-medium"}).get_text().strip()
        basic_obj["location"] = BASIC.find("span", {"class": "text-body-small inline t-black--light break-words"}).get_text().strip()
        data["profile"] = basic_obj
    except Exception as e:
        pass

    # GET ABOUT INFO
    try:
        ABOUT = src.find("div",{ "id": "about" }).find_next_siblings()[1].get_text().strip();
        if(ABOUT != 'About'):
            data["about"] = ABOUT
    except Exception as e:
        pass

    # GET SKILLS
    try:
        SKILLS = src.find("div",{ "id": "skills" }).find_next_siblings()[1];
        allSkills = SKILLS.find("div",{ "class": "pvs-list__footer-wrapper" });
        Skills = [];
        if allSkills :
            skillLink = allSkills.find("a", href=True)["href"];
            browser.get(skillLink);
            fh = browser.execute_script('return document.body.scrollHeight');
            ch = browser.execute_script('return window.innerHeight');
            while ch <= fh:
                sleep(15)
                browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
                ch += ch
            skillPage = BeautifulSoup(browser.page_source, 'lxml')
            skills = skillPage.find_all("li",{ "class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated" });
            for skillIten in skills:
                sks = skillIten.find_all("span",{ "class": "visually-hidden" })
                Skills.append(sks[0].get_text());
        else :     
            skills = SKILLS.find_all("li",{ "class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column" });
            for skill in skills:
                sks = skill.find_all("span",{ "class": "visually-hidden" })
                Skills.append(sks[0].get_text());
        data["skills"] = Skills
    except Exception as e:
        pass

     # ADD SOCIAL
    data["social"] = [
        url, #linkedin
       'https://github.com/'+github, #github
    ]

    # GET EXPERIENCES
    try:
        EXPERIENCE = src.find("div",{ "id": "experience" }).find_next_siblings()[1];
        allExps = EXPERIENCE.find("div",{ "class": "pvs-list__footer-wrapper" });
        Experiences = [];
        if allExps :
            expLink = allExps.find("a", href=True)["href"];
            browser.get(expLink);
            fh = browser.execute_script('return document.body.scrollHeight');
            ch = browser.execute_script('return window.innerHeight');
            while ch <= fh:
                sleep(15)
                browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
                ch += ch
            expPage = BeautifulSoup(browser.page_source, 'lxml');
            Exs = expPage.find_all("li", { "class": "pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated" });
            for i in Exs:
                exp = dict()
                expList = i.find_all("li", { "class": "pvs-list__paged-list-item" });
                if len(expList) > 0 : 
                    expRoles = [];
                    exp["heading"] = i.find("div",{ "class": "display-flex align-items-center" }).find("span", { "class": "visually-hidden"}).get_text().strip();
                    for expLiItem in expList:
                        expSpans = expLiItem.find_all("span",{ "class": "visually-hidden"});
                        expRoleBody = [];
                        for expSpItem in expSpans:
                            expRoleBody.append(expSpItem.get_text().strip());
                        expRoles.append(expRoleBody);
                    exp["roles"] = expRoles;      
                else :
                    expSpans = i.find_all("span",{ "class": "visually-hidden"});
                    exp["heading"] = expSpans.pop(0).get_text().strip();
                    expBody = []
                    for expBodyElm in expSpans:
                        expBody.append(expBodyElm.get_text().strip());
                    exp["body"] = expBody; 
                Experiences.append(exp);   
        else :
            Exs = EXPERIENCE.find_all("li", {"class":"pvs-list__item--line-separated"});
            for i in Exs:
                exp = dict()
                # this part doesn't work
                expList = i.find_all("li", { "class": "" })
                if len(expList) > 0 : 
                    expRoles = [];
                    exp["heading"] = i.find("div",{ "class": "display-flex align-items-center" }).find("span", { "class": "visually-hidden"}).get_text().strip();
                    for expLiItem in expList:
                        expSpans = expLiItem.find_all("span",{ "class": "visually-hidden"});
                        expRoleBody = [];
                        for expSpItem in expSpans:
                            expRoleBody.append(expSpItem.get_text().strip());
                        expRoles.append(expRoleBody);
                    exp["roles"] = expRoles;      
                # this part works
                else :
                    expSpans = i.find_all("span",{ "class": "visually-hidden"});
                    exp["heading"] = expSpans.pop(0).get_text().strip();
                    expBody = []
                    for expBodyElm in expSpans:
                        expBody.append(expBodyElm.get_text().strip());
                    exp["body"] = expBody; 
                Experiences.append(exp);  
        data["experience"] = Experiences
    except Exception as e:
        pass

    # GET EDUCATIONAL INFO
    try:
        EDUCATION = src.find("div",{ "id": "education" }).find_next_siblings()[1];
        allEds = EDUCATION.find("div",{ "class": "pvs-list__footer-wrapper" });
        Educations = []
        if allEds:
            edLink = allEds.find("a", href=True)["href"];
            browser.get(edLink);
            fh = browser.execute_script('return document.body.scrollHeight');
            ch = browser.execute_script('return window.innerHeight');
            while ch <= fh:
                sleep(15)
                browser.execute_script("window.scrollTo(0,"+str(cur_height)+");")
                ch += ch
            edsPage = BeautifulSoup(browser.page_source, 'lxml')
            Eds = edsPage.find_all("li",{ "class":"pvs-list__paged-list-item" });
            for i in Eds:
                ed = dict()
                eds = i.find_all("span",{ "class": "visually-hidden" })
                if len(eds) > 0 : ed["institute"] = eds.pop(0).get_text().strip();
                others = [];
                for j in eds:
                    others.append(j.get_text().strip());
                ed["body"] = others;
                Educations.append(ed);
        else:
            Eds = EDUCATION.find_all("li",{ "class":"pvs-list__item--line-separated" })
            for i in Eds:
                ed = dict()
                eds = i.find_all("span",{ "class": "visually-hidden" })
                if len(eds) > 0 : ed["institute"] = eds.pop(0).get_text().strip();
                others = [];
                for j in eds:
                    others.append(j.get_text().strip());
                ed["body"] = others;
                Educations.append(ed);
        data["education"] = Educations
    except Exception as e:
        pass

    # GET CERTIFICATIONS (TODO: VIEW ALL)
    try:
        CERTIFICATION = src.find("div",{"id":'licenses_and_certifications'}).find_next_siblings()[1];
        Certs = CERTIFICATION.find_all("li", { "class": "pvs-list__item--one-column" })
        Certifications = []
        for i in Certs:
            cer = dict()
            certs = i.find_all("span",{ "class": "visually-hidden"})
            if len(certs) > 0 : cer["course"] = certs.pop(0).get_text();
            if len(certs) > 0 : cer["organization"] = certs.pop(0).get_text();
            others = [];
            for j in certs:
                others.append(j.get_text().strip());
            cer["body"] = others;
            Certifications.append(cer);
        data["certifications"] = Certifications
    except Exception as e:
        pass  

    # GET VOLUNTEER (TODO: VIEW ALL)
    try:
        VOLUNTEER = src.find("div",{ "id": "volunteering_experience" }).find_next_siblings()[1];
        Vls = VOLUNTEER.find_all("li",{ "class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column" })
        Volunteers = []
        for i in Vls:
            vl = dict()
            vls = i.find_all("span",{ "class": "visually-hidden" });
            others = [];
            # organization, role
            if len(vls) > 0 : vl["role"] = vls.pop(0).get_text();
            if len(vls) > 0 : vl["organization"] = vls.pop(0).get_text();
            for j in vls:
                others.append(j.get_text().strip());
            vl["body"] = others;
            Volunteers.append(vl);
        data["volunteer"] = Volunteers
    except Exception as e:
        pass

    browser.close();

    json_object = json.dumps(data, indent=4)
    return(json_object)

# data = scraping('https://www.linkedin.com/in/paulhigginsmentoring/','ishita1805')
# print(data)

# https://www.linkedin.com/in/paige-liwanag/
# https://www.linkedin.com/in/paulhigginsmentoring/
