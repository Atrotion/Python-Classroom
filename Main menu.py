from timetable import *


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
        student_menu(username)
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
    print("3. Update Assignments")
    print("4. Logout")

    # Get user choice
    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        manage_courses()
    elif choice == "2":
        manage_students()
    elif choice == "3":
        update_assignment_status()
    elif choice == "4":
        print("Logging out...")
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")
        admin_menu()

def student_menu(username):
    print("\nStudent Menu:")
    print("1. View Courses")
    print("2. Submit assignment")
    print("3. Check assignment status")
    print("4. Logout")

    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        while True:
            query = courseMenu()
            if query == 1:
                courseList()
            elif query == 2:
                createTimetable(username)
            elif query == 3:
                viewCourse(username)
            elif query == 4:
                break
    elif choice == "2":
        view_grades()
    elif choice == "3":
        submit_assignment(username)
    elif choice == "4":
        check_assignment_status(username)
    elif choice == "5":
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
        addCourse()
        courseList()
        manage_courses()
    elif choice == "2":
        courseList()
        try:
            courseID = int(input("Which course do you want to update? : "))
            updateCourse(courseID)
            manage_courses()
        except ValueError:
            print("Please enter a valid ID")
    elif choice == "3":
        courseList()
        try:
            courseID = int(input("Which course do you want to delete? : "))      
            deleteCourse(courseID)
            manage_courses()
        except ValueError:
            print("Please enter a valid course ID") 
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
    admin_menu()

def delete_student():
    username = input("Enter student's username to delete: ")

    with open("Students.txt", "r") as file:
        lines = file.readlines()
    with open("Students.txt", "w") as file:
        for line in lines:
            if not line.startswith(username + ":"):
                file.write(line)
    print("Student deleted successfully.")
    admin_menu()

def view_grades():
    print("View Grades functionality")

# Function to submit an assignment
def submit_assignment(username):
    # Get input from the user
    student_username = username
    course_code = input("Enter course code: ")
    assignment_name = input("Enter assignment name: ")
    submission_status = "Submitted"  # Assuming the submission status is initially set to "Submitted"

    # Write the assignment details to the assignments file
    with open("assignments_StudentID.txt", "a") as file:
        file.write(f"{student_username}:{course_code}:{assignment_name}:{submission_status}\n")
    print("Assignment submitted successfully.")

# Function to check the status of an assignment
def check_assignment_status(username):
    # Get input from the user
    student_username = username
    course_code = input("Enter course code: ")
    assignment_name = input("Enter assignment name: ")
    submission_status = "Not Submitted"  # Default status if not found

    # Read the assignment details from the assignments file and check status
    with open("assignments_StudentID.txt", "r") as file:
        for line in file:
            stored_username, stored_course_code, stored_assignment_name, stored_status = line.strip().split(":")
            if stored_username == student_username and stored_course_code == course_code and stored_assignment_name == assignment_name:
                submission_status = stored_status
                break

    # Print the assignment status
    print(f"Assignment '{assignment_name}' status for course '{course_code}': {submission_status}")

# Function to update assignment status
def update_assignment_status():
    # Get input from the user
    student_username = input("Enter student's username: ")
    course_code = input("Enter course code: ")
    assignment_name = input("Enter assignment name: ")
    new_status = input("Enter new status: ")

    # Read assignment details from the assignments file and update status
    with open("assignments_StudentID.txt", "r") as file:
        lines = file.readlines()

    with open("assignments_StudentID.txt", "w") as file:
        for line in lines:
            stored_username, stored_course_code, stored_assignment_name, stored_status = line.strip().split(":")
            if stored_username == student_username and stored_course_code == course_code and stored_assignment_name == assignment_name:
                line = f"{stored_username}:{stored_course_code}:{stored_assignment_name}:{new_status}\n"
            else:
                print("Assignment not found.")
            file.write(line)

    print("Assignment status updated successfully.")

if __name__ == "__main__":
    main()
