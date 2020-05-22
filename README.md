_This project is part of my Carrecognizer-project group and was developed as a part of my thesis at the Budapest University of Technology and Economics._

***
# Goal
My task was to design and implement a deep convolutional neural network-based application, which is able to recognize several features of a vehicle based on a picture, mainly the make and the model. Furthermore, I had to develop an application that allows the users to use the functionality of this model conveniently and easily. Based on this, my
work can be divided into two main parts:

The first stage involved doing research tasks as, so far there has been no good
solution, so my task was to plan and implement the whole process from the initial steps
to the birth of the trained model. In this section, I will introduce methods such as creating
WebCrawlers that process unstructured data from websites to build big data databases
with low resource requirements, preprocessing steps with pre-trained neural networks,
knowledge transfer (transfer train) on convolutional networks and various self-designed
evaluation algorithms. To solve these tasks, I had to try different techniques, combine
different approaches, and evaluate the results. Many of my attempts have not been
successful, but in the end, I managed to create a model that can perform this task with
sufficient accuracy.

The second part covers engineering tasks in the traditional sense with all their
challenges. These include the design and the development of a well-scalable, secure
backend and database that can quickly serve the requests of the clients and leverage the
capabilities of the neural model. The clients for the application would allow the users to
use the features conveniently and easily. In order to attract a larger userbase an Angular
based web client, an Android application written in Kotlin and a Facebook chatbot were
also created.

However, the final application is much more capable than that. The entire learning
-testing process, the backend and the clients are designed to provide a solution to any
image recognition problem. The steps in the teaching process were created from wellseparable, independent, and reusable components, and the functionality of the backend
and the clients is completely independent of the specific problem.

As a result of my work I managed to lay down a base for a universal, deep convolutional neural network-based
application, and a backend and clients for this application, that can help to solve any
image processing problem. I also illustrated the work of the application by teaching it on
vehicle categorization to prove the results and usability.

***
# About this program

This program you can find:
* The implementations of my webcrawler that I used to build my image [dataset](https://github.com/banda13/Carrecognizer-database) about cars. These crawlers not only download and build a huge image database, but also process html file of the vehicles, and build a stuctured postgresql big data database. **My idea was that there is a lot of image on the internet about vehicles, and on used-car pages people already labeled it only for me, and my job only to collect it and be gratefull.** These technice worked pretty well for me so I can recommned this to anybody, feel free to contact me if you have a question. (Most of the implementation of these crawlers can be found in the input folder. Mainly I used beautisoup, urllib and sqlalchemy to donwload & process the data)

* Note that these data are really dirty, because people want to make my job harder, and they also upload inside pictures, advertisements and etc. So in the preprosess folder you can find my algorithms to make the data cleaner. I did some experiments with OpenCV algorithms, but I achived the biggest success with an another neural network, that is trained to determine good and bad pictures. [The NN is here.](https://github.com/banda13/Carrecognizer-preclassifier)

* My model can be found in the classifier's folder. I transfer-trained MobileNetV2 (due to the lack of a big infrastructure) I trained a model for every make, and I also created an object detector which can determine the make logo on the picture. (It's inside the pipline folder)

* Another interesting part is the main_controller, which controlles the training and testing process, serialize the results, and log every action. Every run has a different name, which is generated with an lstm trained on pet names. (Well the names of the models are not even close to real pet names, but it's because I didn't trained the LSTM long enough.. fair enough)

* A lot of other interesting scripts, and experiments can be find there (helpers), feel free to look around.

***
# Images
#### WebCrawler results for the category Ford
![WebCrawler results for the category Ford](https://github.com/banda13/Carrecognizer/blob/master/images/sucker_stat.png)

#### Classifier pipline
![Classifier pipline](https://github.com/banda13/Carrecognizer/blob/master/images/classifier_pipline.png)

#### Make object detection
![Make object detection](https://github.com/banda13/Carrecognizer/blob/master/images/audi_objektum_detect.png)

#### Controller
![Controller](https://github.com/banda13/Carrecognizer/blob/master/images/train_pipline.png)

***
# Links
## Other parts of the project
* [Carrecognizer main program, building & training convolutional networks, webcrawelers implementation & lot of other scripts and experiment results](https://github.com/banda13/Carrecognizer)
* [Preclassification convolutional modell determine valid vehicle images](https://github.com/banda13/Carrecognizer-preclassifier)
* [Database](https://github.com/banda13/Carrecognizer-database)
* [Django backend](https://github.com/banda13/Carrecognizer-backend)
* [Angular web application](https://github.com/banda13/Carrecognizer-backend)
* [Android application](https://github.com/banda13/Carrecognizer-android)
* [Messenger chatbot](https://github.com/banda13/Carrecongnizer-chatbot)
## Demos
* [Android client](https://www.youtube.com/watch?v=MohFNK0EPZ8)
* [Angular client](https://www.youtube.com/watch?v=G77Rl3K1amk)
## Thesis
* [Thesis](https://diplomaterv.vik.bme.hu/en/Theses/Gepjarmu-kategorizalas-konvolucios-neuralis)

_I hope you enjoy it (as much as I did) and I hope it can help a little bit to you! <3_
