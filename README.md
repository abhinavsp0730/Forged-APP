# Forged-APP
<img width="431" alt="Capture" src="https://user-images.githubusercontent.com/43638955/113031197-05a47b00-91ac-11eb-854a-3b7473807bc6.PNG">

# Watch this YouTube Video to understand what this project is all about 👇

[![Alt text](https://img.youtube.com/vi/xP8vPzHPoUw/sddefault.jpg)](https://www.youtube.com/watch?v=xP8vPzHPoUw)

## Problems 

* On social media platforms ,  photographs are manipulated and are used in a very improper way with bad intentions . 
* Forensic documents like Adhar cards , driving license , pan cards etc are manipulated . 
* Elections shape the results using photos manipulation .
* Advertisements are manipulated to mislead customers . 
* Women’s intimate pictures are morphed . 
* Celebrities are trolled by blending the pictures with some useless stuffs.

## Our Solutions

* We can simply just upload the image on our app or on our website , then our app will predict whether the image is manipulated or not even you will get to know about the portion being manipulated . 
* This will definitely help you to be aware of the  cyber crimes which happens for intentionally worst purposes . 
* On TWITTER , our twitter bot  platform will help you to get to the forged image of the actual image .

You can get the images verified and be aware of the morphing the images .  

## How to use(Without Docker):
You need ```Python 3.6``` in order to run this project
Go to ```Forged-App/ForgedApp-Backend``` and run ```pip install -r requirements.txt```.
You can start the server by using ```uvicorn main:app --reload``` .
It'll create a web server and and one can Send images as a ```HTTPS Post Requests``` to the created server and get the result from our model.
The format for the body of post request using json is ```{"url":"#url of the image"} ``` .
In order to use to use the twitter bot you need to create the Developer Account for twitter and then you'll get your access tokens. And you've to put these credententials to ```Forged-APP/Twitter-Bot/credentials.py```.

## How to use(With Docker):
Build the docker image by runing the command ```docker build -t myimage .```.
And then run the docker container ```docker run -d --name mycontainer -p 80:80 myimage```.
After that one can Send images as a ```HTTPS Post Requests``` to ```http://localhost:80/predict``` and get the result from our model.
The format for the body of post request using json is ```{"url":"#url of the image"} ``` .

