# btu.py

Python library that makes fetching data from BTU Classroom really easy.

## Example usage of library:
```python
from btu.classroom import Classroom

username = ""  # ბითიუს მეილი ან პირადი ნომერი
password = ""  # პაროლი

classroom = Classroom(username, password)

print(f"შემოსულია {classroom.inbox} წაუკითხავი შეტყობინება")
```

see [examples](https://github.com/Graphity/btu.py/tree/main/examples) for more.

# btu-fetch

Script to run scrapers and output data in json format.

## Usage of script:
```console
usage: btu-fetch [-h] [-s source] [-o path] [--username username] [--password password]
                 {notifications,courses,messages} [{notifications,courses,messages} ...]

Run BTU Classroom scrapers.

positional arguments:
  {notifications,courses,messages}
                        scraper to run

options:
  -h, --help            show this help message and exit
  -s source             path to source file.json
  -o path               path to output directory
  --username username   classroom username
  --password password   classroom password
```

## Installation
```console
pip install btu.py
```
