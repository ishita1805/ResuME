# [ResuME - Website Generator ](https://github.com/ishita1805/ResuME)
#### **A CLI Tool to generate and deploy beautiful websites in under 5 minuites**

Hey there 👋🏽, I'm Ishita and I've made this project to help fellow developers build and deploy their portfolio websites within minuites. 🧁

## **Table of Contents**
- [Installation](#installation)
- [Usage](#usage)
    - [Requirements](#requirements)
    - [Integration with Github](#integration-with-github)
    - [Commands and Features](#commands-and-features)
- [Bugs and Feature Requests](#bugs-and-feature-requests)
- [Contributing](https://github.com/ishita1805/ResuME/blob/main/CONTRIBUTING.md)


### **Installation**

You can find all versions of the CLI [here](https://github.com/ishita1805/resuMe/dist):

To install the CLI:
- download the latest version
- run the command:
```
pip install <path-to-whl-file>
```
### **Usage**

#### **Reqruitments**
To be able to use the CLI you must have the following:
- Python
- Git CLI
#### **Integration with Github**
To have a github project show up on the website, add the topic: `resume-cli` to it.

#### **Commands and Features**
ResuMe has a bunch of cool features:
- to configure the CLI run: 
    ```
    resuMe init
    ```
    *this is a one-time step.*


- to build a website using your linkedin and github accounts:
    ```
    resuMe build
    ```
    *This command creates a website and pushes it to your github account.*


- to deploy the website:
    ```
    resuMe deploy
    ```
    *This command deploys the website to github pages*


- to list all your websites:
    ```
    resuMe list
    ```


- to delete a website:
    ```
    resuMe delete
    ```
    *Important Note: Please do not delete the local copy or the repository manually*
    **What if i have already deleted my github repository or my local copy:**
    - Incase you have deleted your local copy, please delete the corresponding github repository.
    - Incase you have deleted your github repository, please delete the corresponding local copy.

- to update your website:
    ```
    resuMe update
    ```

### **Bugs and Feature Requests**
- Please add your bug report or feature request to the issues tab with an appropriate label.
- Make sure to look through the issues to not create a duplicate issue

