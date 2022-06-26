import argparse
import pathlib
import os
import json

from .classroom import Classroom
from getpass import getpass


def main():
    choices = [
        "notifications",
        "courses",
        "messages"
    ]
    parser = argparse.ArgumentParser(description="Run BTU Classroom scrapers.")
    parser.add_argument("scraper", choices=choices, nargs="+",
                        help="scraper to run")
    parser.add_argument("-s", metavar="source", type=open,
                        help="path to source file.json")
    parser.add_argument("-o", metavar="path", type=pathlib.Path, default="./",
                        help="path to output directory")
    parser.add_argument("--username", metavar="username", default="",
                        help="classroom username")
    parser.add_argument("--password", metavar="password", default="",
                        help="classroom password")

    args = parser.parse_args()

    if args.s:
        with args.s as f:
            data = json.load(f)
        args.username = data["username"]
        args.password = data["password"]

    if not args.username:
        args.username = input("username: ")
    if not args.password:
        args.password = getpass("password: ")

    if not args.username or not args.password:
        raise Exception("username and password is required")

    classroom = Classroom(args.username, args.password)

    if "notifications" in args.scraper:
        notifications = classroom.fetch_notifications()
        path = os.path.join(args.o, "notifications.json")
        with open(path, "w") as f:
            json.dump(notifications, f, indent=4, ensure_ascii=False)

    if "courses" in args.scraper:
        courses = classroom.fetch_selected_courses()
        path = os.path.join(args.o, "selected_courses.json")
        with open(path, "w") as f:
            json.dump(courses, f, indent=4, ensure_ascii=False)

    if "messages" in args.scraper:
        messages = classroom.fetch_messages()
        path = os.path.join(args.o, "messages.json")
        with open(path, "w") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
