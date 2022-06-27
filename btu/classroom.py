import requests
from bs4 import BeautifulSoup
from typing import Optional


class Classroom:
    def __init__(self, username: str, password: str) -> None:
        self.soup = self.login(username, password)

    def login(self, username: str, password: str) -> BeautifulSoup:
        url = "https://classroom.btu.edu.ge/ge/login/trylogin"
        data = {
            "username": username,
            "password": password
        }
        self.session = requests.session()
        r = self.session.post(url, data=data)
        soup = BeautifulSoup(r.content, "html.parser")
        alert_message = soup.find("span", class_="alert-message")
        if alert_message:
            raise Exception(alert_message.text.strip())
        return soup

    @property
    def semester(self) -> str:
        """str: Represents current semester."""
        return self.soup.find("div", class_="custom_pre_tag").text.strip()

    @property
    def user(self) -> str:
        """str: Represents full name of logged in user."""
        return self.soup.find("a", class_="navbar-link").text.strip()

    @property
    def inbox(self) -> str:
        """str: Represents amount of unread messages."""
        return self.soup.find_all("span", class_="badge")[-1].text.strip()

    @property
    def balance(self) -> str:
        """str: Represents current balance."""
        return self.soup.find("span", {"id": "balance_sum"}).text.strip()

    @property
    def credits(self) -> str:
        """str: Represents total chosen credits."""
        return self.soup.find_all("strong")[-1].text.strip()

    def fetch_notifications(self) -> list:
        ul = self.soup.find("ul", class_="nav-tabs")
        li = ul.find_all("li", class_="nav-header")[-1]
        ul = ul.find_all("li")
        li_index = ul.index(li) + 1
        notifications = []
        for li in ul[li_index:]:
            a = li.find("a")
            notifications.append(
                {
                    "title": a["title"],
                    "url": a["href"]
                }
            )
        return notifications

    def icon_to_emoji(self, icon_class: str) -> str:
        icons = {
            "icon-circle": "🟠",
            "icon-ok": "✅",
            "icon-remove": "❌"
        }
        if icon_class in icons:
            return icons[icon_class]
        return icon_class
    
    def get_course_tabs(self, course_url) -> dict:
        r = self.session.get(course_url)
        soup = BeautifulSoup(r.content, "html.parser")
        ul = soup.find("ul", {"id": "course_tabs"}).find_all("li")
        hrefs = [li.find("a")["href"] for li in ul]
        return {
            "syllabus": hrefs[0],
            "groups": hrefs[1],
            "scores": hrefs[2],
            "resources": hrefs[3]
        }

    def fetch_course_scores(self, course_url: str) -> list:
        scores_url = self.get_course_tabs(course_url)["scores"]
        r = self.session.get(scores_url)
        soup = BeautifulSoup(r.content, "html.parser")
        scores = []
        for tr in soup.find("tbody").find_all("tr"):
            texts = [td.text.strip() for td in tr.find_all("td")]
            scores.append(
                {
                    "info": texts[0],
                    "value": texts[1]
                }
            )
        return scores

    def fetch_selected_courses(self) -> list:
        courses = []
        for tr in self.soup.find_all("tr")[1:-1]:
            tds = tr.find_all("td")
            url = tds[2].find("a")["href"]
            courses.append(
                {
                    "icon": self.icon_to_emoji(tds[0].find("i")["class"][0]),
                    "code": tds[1].text.strip(),
                    "name": tds[2].text.strip(),
                    "url": url,
                    "points": tds[3].text.strip(),
                    "min_credits": tds[4].text.strip(),
                    "credits": tds[5].text.strip(),
                    "scores": self.fetch_course_scores(url)
                }
            )
        return courses

    def get_message_tabs(self) -> dict:
        url = "https://classroom.btu.edu.ge/en/messages"
        ul = self.soup.find("ul", class_="nav-tabs")
        hrefs = [li.find("a")["href"] for li in ul.find_all("li")]
        return {
            "inbox": hrefs[0],
            "sent": hrefs[1],
            "recommendhreftion": hrefs[2]
        }

    def fetch_messages(self, sent: Optional[bool] = False) -> list:
        if sent:
            url = self.get_message_tabs()["sent"]
        else:
            url = self.get_message_tabs()["inbox"]
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        messages = []
        for tr in soup.find("tbody").find_all("tr")[1:]:
            tds = tr.find_all("td")
            a = tds[1].find("a")
            messages.append(
                {
                    "name": a.text.strip(),
                    "url": a["href"],
                    "title": tds[2].text.strip(),
                    "time": tds[3].text.strip()
                }
            )
        return messages
