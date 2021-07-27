// dynamically add data to html file
var user_name = $('#p-name')
var user_tag = $('#p-tag')
var about = $('#about-text')
var education = $('#education')
var work = $('#work')
var projects = $('#project-cont')
var volunteer = $('volunteer')
var skills = $('#skills-cont')
var footer = $('#footer')
var git = $('#github')
var lin = $('#linkedin')

fetch('data.json')
.then(response=>response.json())
.then((result)=>{
    // user profile data
    user_name.text('I am '+result['profile']['Name'])
    user_tag.text(result['profile']['Headline']+' from '+result['profile']['Location'])
    git.attr("href", result['social'][1])
    lin.attr("href", result['social'][0])
    // about
    about.text(result['about'])
    // education
    if(result['education']){
        result['education'].forEach(element => {
            var edu = `<div class='education-cont'>
                            <h3>${element['Institute']}</h3>
                            <p><b>${element['Degree Name']}</b></p>
                            <p>${element['Field Of Study']}</p>
                            <p>${element['Dates attended or expected graduation']}</p>
                        </div>`
            education.append(edu)
        });
    }
    // experience
    if(result['experience']){
        result['experience'].forEach(element => {
            if(element['Roles']){
                var exp = `<div class='exp'>
                                <div class='exp-bullet'></div>
                                <div class='exp-col'>
                                <h3>${element['Roles'][0]['Title']}</h3>
                                <b>${element['Company Name']}</b>
                                <p>${element['Roles'][0]['Dates Employed']}</p>
                                <p>${element['Location']}</p>
                                </div>
                            </div>`
                work.append(exp)
            }
            else {
                var exp = `<div class='exp'>
                            <div class='exp-bullet'></div>
                            <div class='exp-col'>
                            <h3>${element['Role']}</h3>
                            <b>${element['Company Name']}</b>
                            <p>${element['Dates Employed']}</p>
                            <p>${element['Location']}</p>
                            </div>
                        </div>`
                work.append(exp)
            }
            
        });
    }
    // skills
    if(result['skills']){
        result['skills'].forEach(element => {
            var skill = ` <li>${element}</li>`
            skills.append(skill)
        });
    }
    // projects
    github_id = result['social'][1].replace('https://github.com/','')
    fetch(`https://api.github.com/users/${github_id}/repos`)
    .then(response => response.json())
    .then(resp => {
        resp.forEach(element => {        
            if(element.description !== null && element.fork === false){
                var project = `<div class='project-card'>
                                    <b>${element.name}</b>
                                    <p>Language: ${element.language}</p>
                                    <p class='project-text'>
                                        ${element.description}
                                    </p>
                                    <a href='${element.url}'><img class='icon' src='./assets/github.png'/></a>
                                </div>`
                projects.append(project)
            }
        });
    })
    // volunteering
    if(result['volunteering']){
        result['volunteering'].forEach(element => {
            var volun = `<div class='exp'>
                            <div class='exp-bullet'></div>
                            <div class='exp-col'>
                            <h3>${element['Title']}</h3>
                            <b>${element['Company Name']}</b>
                            <p>${element['Dates volunteered']}</p>
                            <p>${element['Cause']}: ${element['Description']}</p>
                            </div>
                        </div>`
            volunteer.append(volun)
        });
    }
    // footer
    footer.text('Made using ResuME - Website Generator')
})

// TODO
// 1. Check for missing sections/divs and remove them from the website