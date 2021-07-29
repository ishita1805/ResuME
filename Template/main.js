// dynamically add data to html file

// declaring variables
var user_name = $('#p-name')
var user_tag = $('#p-tag')
var about = $('#about-text')
var work = $('#work')
var projects = $('#project-cont')
var volunteer = $('volunteer')
var skills = $('#skills-cont')
var footer = $('#footer')
var git = $('#github')
var lin = $('#linkedin')

var navigation = $('#navigation')

var aboutMain = $('#about')
var education = $('#education')
var certification = $('#certifications')
var skillsMain = $('#skills')
var workMain = $('#experiences')
var volunteerMain = $('#volunteering')
var projectsMain = $('#projects')

// load json file
fetch('data.json')
.then(response=>response.json())
.then((result)=>{
    // append data to html

    // user profile data
    user_name.text('I am '+result['profile']['Name'])
    user_tag.text(result['profile']['Headline']+' from '+result['profile']['Location'])
    git.attr("href", result['social'][1])
    lin.attr("href", result['social'][0])

    // about
    if(result['about']){ 
        about.text(result['about'])
        navigation.append("<li class='nav-items'><a href='#about'>About</a></li>")
    }
    else {
        aboutMain.remove()
    }

    // education
    if(result['education']){
        result['education'].forEach(element => {
            var edu = `<div class='education-cont'>
                            ${element['Institute']?`<h3>${element['Institute']}</h3>`:''}
                            ${element['Degree Name']?`<p><b>${element['Degree Name']}</b></p>`:''}
                            ${element['Field Of Study']?`<p>${element['Field Of Study']}</p>`:''}
                            ${element['Dates attended or expected graduation']?`<p>${element['Dates attended or expected graduation']}</p>`:''}
                        </div>`
            education.append(edu)
        });
    }
    else {
        education.remove()
    }

    // certifications
    if(result['certifications']){
        result['certifications'].forEach(element => {
            var cer = `<div class='education-cont'>
                            ${element['Title']?`<h3>${element['Title']}</h3>`:''}
                            ${element['Issuing authority']?`<p><b>${element['Issuing authority']}</b></p>`:''}
                            ${element['Issued date and, if applicable, expiration date of the certification or license']?`<p>${element['Issued date and, if applicable, expiration date of the certification or license']}</p>`:''}
                            ${element['Credential Identifier']?`<p>${element['Credential Identifier']}</p>`:''}
                        </div>`
                        certification.append(cer)
        });
    }
    else {
        certification.remove()
    }

    // skills
    if(result['skills']){
        result['skills'].forEach(element => {
            var skill = ` <li>${element}</li>`
            skills.append(skill)
        });
        navigation.append(" <li class='nav-items'><a href='#skills'>Skills</a></li>")
    } 
    else {
        skillsMain.remove()
    }

    // experience
    if(result['experience']){
        result['experience'].forEach(element => {
            if(element['Roles']){
                var exp = `<div class='exp'>
                                <div class='exp-bullet'></div>
                                <div class='exp-col'>
                                    ${element['Roles'][0]['Title']?`<h3>${element['Roles'][0]['Title']}</h3>`:''}
                                    ${element['Company Name']?`<b>${element['Company Name']}</b>`:''}
                                    ${element['Roles'][0]['Dates Employed']?`<p>${element['Roles'][0]['Dates Employed']}</p>`:''}
                                    ${element['Location']?`<p>${element['Location']}</p>`:''}    
                                </div>
                            </div>`
                work.append(exp)
            }
            else {
                var exp = `<div class='exp'>
                            <div class='exp-bullet'></div>
                            <div class='exp-col'>
                                    ${element['Role']?`<h3>${element['Role']}</h3>`:''}
                                    ${element['Company Name']?`<b>${element['Company Name']}</b>`:''}
                                    ${element['Dates Employed']?`<p>${element['Dates Employed']}</p>`:''}
                                    ${element['Location']?`<p>${element['Location']}</p>`:''}    
                            </div>
                        </div>`
                work.append(exp)
            }
        });
        navigation.append(" <li class='nav-items'><a href='#experiences'>Work</a></li>")
    }
    else {
        workMain.remove()
    }

    // projects
    github_id = result['social'][1].replace('https://github.com/','')
    fetch(`https://api.github.com/users/${github_id}/repos`)
    .then(response => response.json())
    .then(resp => {
        if(resp.length>0){
            resp.forEach(element => {        
                if(element.fork === false){
                    var project = `<div class='project-card'>
                                        <b>${element.name}</b>
                                        <p>Language: ${element.language===null?'Other':element.language}</p>
                                        ${element.description?`<p class='project-text'>
                                            ${element.description}
                                        </p>`:''}
                                        <a href='${element.html_url}' target='__blank'><img class='icon' src='./assets/github.png'/></a>
                                    </div>`
                    projects.append(project)
                }
            });
            navigation.append("<li class='nav-items'><a href='#projects'>Projects</a></li>")
        } else{
            projectsMain.remove()
        }
    })
    
    // volunteering
    if(result['volunteering']){
        result['volunteering'].forEach(element => {
            var volun = `<div class='exp'>
                            <div class='exp-bullet'></div>
                            <div class='exp-col'>
                                ${element['Title']?`<h3>${element['Title']}</h3>`:''}
                                ${element['Company Name']?`<b>${element['Company Name']}</b>`:''}
                                ${element['Dates volunteered']?`<p>${element['Dates volunteered']}</p>`:''}
                                ${element['Description']?`<p>${element['Cause']}: ${element['Description']}</p>`:''}
                            </div>
                        </div>`
            volunteer.append(volun)
        });
        navigation.append("<li class='nav-items'><a href='#volunteering'>Volunteering</a></li>")
    }
    else {
        volunteerMain.remove()
    }

    // footer
    footer.text('Made using ResuME - Website Generator')
})

// TODO
// 1. Check for missing divs and remove them from the website