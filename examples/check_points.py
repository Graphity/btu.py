from btu.classroom import Classroom
import json


with open("credentials.json") as f:
    credentials = json.load(f)
    username = credentials["username"]
    password = credentials["password"]

classroom = Classroom(username, password)
updated_courses = classroom.fetch_selected_courses()

with open("selected_courses.json") as f:
    cached_courses = json.load(f)

if updated_courses == cached_courses:
    print("No new points")
    exit()

for i in range(len(cached_courses)):
    old_points = cached_courses[i]["points"]
    new_points = updated_courses[i]["points"]

    if new_points != old_points:
        print(cached_courses[i]["name"])
        print(f"Overall: {new_points} Pts.")
        print("NEW:")
        old_scores = cached_courses[i]["scores"]
        new_scores = updated_courses[i]["scores"]

        for j in range(len(old_scores)):
            if new_scores[j] != old_scores[j]:
                info = new_scores[j]["info"]
                value = new_scores[j]["value"]
                print(f"\t{info}: {value}")
        print()
