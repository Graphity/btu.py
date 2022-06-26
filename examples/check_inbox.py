from btu.classroom import Classroom

username = ""  # ბითიუს მეილი ან პირადი ნომერი
password = ""  # პაროლი

classroom = Classroom(username, password)

print(f"შემოსულია {classroom.inbox} წაუკითხავი შეტყობინება")
