# Úrad verejného zdravotníctva - BOT

## Overview
This app is created as unoffical project to spread data from ÚVZ SR to the public. It pulls data from [RSS feed of ÚVZ](https://www.uvzsr.sk/index.php?option=com_content&view=frontpage&Itemid=1&type=rss&format=feed "ÚVZ SR RSS feed"), and posts it to [Twitter](https://twitter.com/NewsletterUvz, "Twitter Feed"). Project is hosted on [Heroku](https://rss-uvz.herokuapp.com/ "Heroku page") as an backgroud process of Flask server.

## Techincal details
Currently bot has 4 services: 
* Email service
  ##### Sends updates as formated HTML mails to subscribers.
* RSS listener service
  ##### Listens for updates on RSS feed of ÚVZ SR.
* Twitter service
  ##### Posts updated to twitter.
* Refresh service (microservice)
  ##### This is microservice which keeps Heroku dyno from falling asleep, should be reaplced down the road by something more permanent.
Currently each service is running as separate process run all from main thread. Down the road this should be replaced by creating separate therads for each process, to make them more independent, and modular.

## Future goals:
* Create twitter dialog through direct messages, to subscribe to newsletter
* Improve test coverage
* Add automatic shutodown of processes, for when they are inactive for longer persions of time 
* Create database service
* Move environmnet varibles such as "reciever_emails" to database service so they can be dynamicaly updated
* Add support for facebook
  ##### This feature is blocked by need of obtaining developer account from Facebook
* Create custom email (probably SMTP) server on from which emails will be sent
* Add autmated pipeline for running tests

## How to contribute
* Ideas for feature improvements please send to this [email](mailto:mtoth575@gmail.com?subject=[Github]%20ÚVZ%20BOT%20, "Personal email")
* Pull requests need to comply with test, if they dont pass, current tests can be changed, but cannot be removed unless approved
* Each new service has to implement IService interface
* After each new service has to have its coresponding test suite
* No need to ask for persmission when adding new library, but remember to do `pip3 freeze > requirements.txt`, otherwise build will fail
* Project is developed on Python 3.8, as of now I don't see reason whz this should change

<a href="mailto:mtoth575@gmail.com?subject=[Github]%20ÚVZ%20BOT%20?"><img src="https://img.shields.io/badge/gmail-%23DD0031.svg?&style=for-the-badge&logo=gmail&logoColor=white"/></a>
![version](https://img.shields.io/badge/version-1.0.0-blue)
![dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-green)
![coverage](https://img.shields.io/badge/coverage-0%25-red)
![uptime](https://img.shields.io/badge/uptime-100%25-brightgreen)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)]("https://rss-uvz.herokuapp.com/")


