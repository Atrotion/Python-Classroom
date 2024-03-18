def main():
    print("Welcome!")
    print("1. Login as Admin")
    print("2. Login as Student")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        admin_login()
    elif choice == "2":
        student_login()
    else:
        print("Invalid choice. Please enter either 1 or 2.")
        main()

def admin_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == "admin" and password == "123":
        print("Access granted")
        admin_menu()
    else:
        print("Access denied")
        main()

def student_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_student_credentials(username, password):
        print("Access granted")
        student_menu()
    else:
        print("Access denied")
        main()

def check_student_credentials(username, password):
    with open("Students.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if stored_username == username and stored_password == password:
                return True
    return False

def admin_menu():
    print("\nAdmin Menu:")
    print("1. Manage Courses")
    print("2. Manage Students")
    print("3. Logout")

    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        manage_courses()
    elif choice == "2":
        manage_students()
    elif choice == "3":
        print("Logging out...")
    else:
        print("Invalid choice. Please enter a number from 1 to 3.")
        admin_menu()

def student_menu():
    print("\nStudent Menu:")
    print("1. View Courses")
    print("2. View Grades")
    print("3. Logout")

    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        view_courses()
    elif choice == "2":
        view_grades()
    elif choice == "3":
        print("Logging out...")
    else:
        print("Invalid choice. Please enter a number from 1 to 3.")
        student_menu()

def manage_courses():
    print("\nCourse Management Menu:")
    print("1. Add Course")
    print("2. Update Course")
    print("3. Delete Course")
    print("4. Back to Admin Menu")

    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        add_course()
    elif choice == "2":
        update_course()
    elif choice == "3":
        delete_course()
    elif choice == "4":
        admin_menu()
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")
        manage_courses()

def manage_students():
    print("\nStudent Management Menu:")
    print("1. Add Student")
    print("2. Delete Student")
    print("3. Back to Admin Menu")

    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        add_student()
    elif choice == "2":
        delete_student()
    elif choice == "3":
        admin_menu()
    else:
        print("Invalid choice. Please enter a number from 1 to 3.")
        manage_students()

def add_student():
    username = input("Enter new student's username: ")
    password = input("Enter new student's password: ")

    with open("Students.txt", "a") as file:
        file.write(f"{username}:{password}\n")
    print("Student added successfully.")

def delete_student():
    username = input("Enter student's username to delete: ")

    with open("Students.txt", "r") as file:
        lines = file.readlines()
    with open("Students.txt", "w") as file:
        for line in lines:
            if not line.startswith(username + ":"):
                file.write(line)
    print("Student deleted successfully.")

def add_course():
    print("Add Course functionality")

def update_course():
    print("Update Course functionality")

def delete_course():
    print("Delete Course functionality")

def view_courses():
    print("View Courses functionality")

def view_grades():
    print("View Grades functionality")

if __name__ == "__main__":
    main()
