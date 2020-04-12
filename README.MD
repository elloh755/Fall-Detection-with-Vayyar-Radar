Fall-Detection-with-Vayyar-Radar
Jorge Mazariegos,Danny Nguyen, Liam O’Donnell
Project Overview:
We plan to use the provided Walabot Vayyar Radar to collect real world data of people moving within a room and trying to distinguish whether or not they have fallen. We would like to be able to detect a fall and upon detection of a fall have an automated text message sent to a recipient, like a family member. 

Problem:
Elderly residents living alone may fall and be unable to call for help. Wearables and camera based detection devices have been implemented before, but these come with certain disadvantages. 

Solution:
Using the Vayyar Radar as an alternative to wearables and camera based fall detection devices provides us with a way to detect when a fall occurs without compromising the privacy of users. The Vayyar Radar also provides us with a way of detecting users in the vicinity more accurately not requiring direct-line-of-sight. Upon detection of a fall an automated text message sent to an emergency contact will be a reliable means of ensuring help reaches the resident.

Methodologies:
We will be making use of the Walabot sdk and Python in order to collect real time data as well as read that data and save it into a pandas dataframe object. As for classifying this raw data we will be utilizing scikit learn for basic classification using algorithms such as Random forest, Naive bayes and decision trees. These may change if we find an algorithm that gives a more accurate fitting of our data. If time provides we would like to make use of firebase to integrate some sort of alert mechanism that will send a notification to users phones.

Data-Collect.py can be run using: "python Data_collect.py X"
X can be 0, 1 or 2 and correspond to Walking, Standing or Falling as the activity that is being recorded.
It runs for 5 minutes or until the user intterupts it with Ctrl+C. 