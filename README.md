# WatchDog
App for dog trainers and behaviorists, created with Django.

## General Info
The application allows dog trainer to compose an exercise (i.e. give it a name, an instruction and precise what information should be saved in database) and assign it to any number of their clients. The application checks also the weather condition at the moment of registering the exercise (since wather may influence dog's behavior). The trainer can annulate ascription of an exercise to a client without loosing associated data.

## Functionalities in place
* Create account
* Create profile 
* Update profile
* Compose an exercise (for staff)
* Assign an exercise to a user (for staff)
* Annulate ascription of an exercise to a client (for staff)
* Register exercise (for client)
* See the history of executed exercises

## Planned Improvments
* Delete profile
* Change password
* Reset password
* Suspend client's profile (for staff)
* Enable client to set temporary location
* Add check historical weather to enable client to register their exercises with a delay
* Add functionality for the trainer to comment each instance of exercise
* Display details of each exercise
* Enable clients to register more than one dog per account
* Disable creating account for people not invited by the trainer

## Technologies
* Python 3.6
* Django 3.1
* Bootstrap 4

For further details see requrements.txt
