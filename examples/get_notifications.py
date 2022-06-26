from btu.classroom import Classroom
import json

with open("credentials.json") as f:
    credentials = json.load(f)

username = credentials["username"]
password = credentials["password"]

classroom = Classroom(username, password)
notifications = classroom.fetch_notifications()

for notification in notifications:
    print(notification["title"])
