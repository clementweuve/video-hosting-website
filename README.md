# video-hosting-website
## Presentation
This project allows you to host a video host website yourself. Inspired by YouTube, it includes many features:
+ Account system
+ video upload system
+ subscription system
+ search system
+ comments system
+ likes/dislikes system
+ administration panel
+ darkmode

|Video Example|Channel Example|Darkmode Example|
|-------------|---------------|----------------|
|![video example](https://i.imgur.com/rQKrYKa.png)|![channel example](https://i.imgur.com/EGRq694.png)|![darkmode example](https://i.imgur.com/s4ym2cH.png)

## How to Setup
To Setup this project, you need to install Python and the following modules:
+ Flask
+ sqlite3
+ datetime
+ uuid

To start the server, you need to run the "flaskapp.py" file

## How to add an admin
To add the admin role to an existing user:
1. Get the UUID of the user
2. replace "uuid_of_the_user" with the uuid in add_admin.py
3. Run the python file

|Admin panel example|
|-------------------|
|![admin panel](https://i.imgur.com/tSlbagM.png)|
