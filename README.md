# README #

## PROJECT STRUCTURE

This project developed with Python + Flask for backend and Bootstrap + jQuery for frontend.
You can see additional python packages in requirement.txt and additional frontend packages in bower.json.


+ script                `startup scripts`
+ src
    + pptxbuilder
        + assets        `application asset files`
        + static
            + css       `Frontend style files`
            + favicon   `Favicon images`
            + js        `Frontend javascript files`
        + templates     `Jinja templates`
        + tests         `Application tests`
        + views         `Blueprint views of flask app`
+ .bowerrc              `Bower environment file`
+ bower.json            `Required frontend packages`
+ package.json          `Required for heroku to install bower packages`
+ Procfile              `Heroku Procfile`
+ requirements.txt      `Required python packages`
+ run.py                `Main entry point for app on development`


##DEVELOPMENT SETUP

**Requirements: VirtualEnv with Python3 and Bower**

Create virtualenv on root path of project. `virtualenv -p python3 venv` And activate it `source venv/bin/activate`

Install python requirements from requirements.txt `pip install -r requirements.txt`

Install bower requirements `bower install` See how to install bower: https://bower.io

####Starting development server
Run `python run.py app` to start application on localhost.


###Testing
Run `python run.py test` to start testing.

Note that you need Sass support in order to build scss files. See: http://sass-lang.com/install


##INSTALLING ON HEROKU (from scratch)

1- Create your project on heroku

2- Add new project remote address to your git repo by following steps under "Deploy using Heroku Git"

3- Add python support to your project via heroku cli: `heroku buildpacks:add --index 1 heroku/python -a your_app_name`

4- Add nodejs support to run 'bower install' during build via heroku cli: `heroku buildpacks:add --index 1 heroku/nodejs -a your_app_name`

5- Set PYTHONPATH config variable under Settings > Config Variables `PYTHONPATH=/app/src/`

6- Set PYTHONPRODUCTION config variable under Settings > Config Variables `PYTHONPRODUCTION=1`

7- Set WEB_CONCURRENCY config variable `WEB_CONCURRENCY=3` (You can increase it depending on your visitor count)

## Build Process
Every time when you commit your code to heroku (git push heroku master), it will auto build on heroku.

## Configuration
There are 2 configuration files at root path of project. config.development.ini and config.production.ini.
These files contains basic application configuration. You can change these settings depending on your needs.
Or you can store new settings for future developments to these files. (such as database url etc.)
There is a Gmail account associated with report bug page (the one used for sending the emails). It needs to be defined through env variables:
BUG_EMAIL and BUG_EMAIL_PASSWORD.
The email to which these reports will be sent can also be changed through environment variable BUG_SEND_TO_EMAIL. If it is not defined it defaults to pptxbuilder@gmail.com.
