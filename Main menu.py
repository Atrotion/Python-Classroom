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
    print("4. Display Attendance")
    print("5. Logout")

    # Get user choice
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        manage_courses()
    elif choice == "2":
        manage_students()
    elif choice == "3":
        update_assignment_status()
    elif choice == "4":
        attendance_display()
    elif choice == "5":
        print("Logging out...")
        main()
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
        admin_menu()


def student_menu(username):
    print("\nStudent Menu:")
    print("1. View Courses")
    print("2. Submit assignment")
    print("3. Check assignment status")
    print("4. Mark Attendance")
    print("5. Logout")

    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        while True:
            query = courseMenu()
            if query == 1:
                print("Available Courses:")
                for courseID, courseInfo in courses.items():
                    print(f"{courseID}. {courseInfo['name']}")
                    for key, value in courseInfo["grouping"].items():
                        print(f"   {key}. {value}")          
            elif query == 2:
                createTimetable(username)
            elif query == 3:
                viewCourse(username)
            elif query == 4:
                break
        student_menu(username)
        
    elif choice == "2":
        submit_assignment(username)
        student_menu(username)
    elif choice == "3":
        check_assignment_status(username)
        student_menu(username)
    elif choice == "4":
        mark_attendance(username)
        student_menu(username)
    elif choice == "5":
        main()



subject_attendance = {}

def attendance_display():
    attendance_file = "attendance_StudentID.txt"

    with open(attendance_file, "r") as File:
        rows = File.readlines()
        for row in rows:
            print(row, end = '  ')
        print()
    

def mark_attendance(username):
    attendance_file = "attendance_StudentID.txt"
    
    course_code = input("Enter course code [e.g.XXX1234]: ")
    student_id = username
    class_time = input("Enter Class Time [e.g.12PM-2PM]: ")

    attendance_data = f"{course_code}, {student_id}, {class_time},PRESENT\n"

    with open(attendance_file, "a") as file:
        file.write(attendance_data)

    if course_code not in subject_attendance:
        subject_attendance[course_code] = {'total': 0, 'attended': 0}
    subject_attendance[course_code]['total'] += 1
    subject_attendance[course_code]['attended'] += 1

    print(f"{course_code}, {student_id}, {class_time}, PRESENT")


def display_subject_attendance():
    for course_code, data in subject_attendance.items():
        total_class = data['total']
        attended_class = data['attended']
        if total_class == 0:
            percentage = 0
        else:
            percentage = (attended_class / total_class) * 100
        print(f"Attendance Percentage for course {course_code}: {percentage:.2f}%")
    admin_menu()

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


# Function to submit an assignment
def submit_assignment(username):
    try:
        # Get input from the user
        student_username = username
        course_code = input("Enter course code: ")
        assignment_name = input("Enter assignment name: ")
        submission_status = "Submitted"  # Assuming the submission status is initially set to "Submitted"

        assignment_found = False

        # Write the assignment details to the assignments file
        with open("assignments_StudentID.txt", "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 4:
                    stored_username, stored_course_code, stored_assignment_name, stored_status = parts
                    if stored_course_code == course_code and stored_assignment_name == assignment_name and stored_status == submission_status:
                        print("Assignment already submitted.")
                        assignment_found = True
                        break
                else:
                    print("Invalid format in assignments file:", line)
        if not assignment_found:
            with open("assignments_StudentID.txt", "a") as file:
                file.write(f"{student_username}:{course_code}:{assignment_name}:{submission_status}\n")
            print("Assignment submitted sucessfully.")
    except Exception as e:
        print("An error occurred while submitting the assignment", e)
    
    choice = input("Do you want to enter another assignment? (Enter y/n): ")
    if choice.lower() == "y":
        submit_assignment(username)
    else:
        student_menu(username)

# Function to check the status of an assignment
def check_assignment_status(username):
    try:
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
                    # Print the assignment status
                    print(f"Assignment '{assignment_name}' status for course '{course_code}': {submission_status}")
                    break
                else:
                    print("Assignment not found.")
    except Exception as e:
        print("An error occured while checking the assignment status:", e)
    
    choice = input("Do you want to continue? (Enter y/n): ")
    if choice.lower() == "y":
        student_menu(username)
    else:
        print("Logging out...")


# Function to update assignment status
def update_assignment_status():
    try:
        # Get input from the user
        student_username = input("Enter student's username: ")
        course_code = input("Enter course code: ")
        assignment_name = input("Enter assignment name: ")
        new_status = input("Enter new status: ")

        # Read assignment details from the assignments file and update status
        with open("assignments_StudentID.txt", "r") as file:
            lines = file.readlines()

        with open("assignments_StudentID.txt", "w") as file:
            assignment_found = False
            for line in lines:
                stored_username, stored_course_code, stored_assignment_name, stored_status = line.strip().split(":")
                if stored_username == student_username and stored_course_code == course_code and stored_assignment_name == assignment_name:
                    line = f"{stored_username}:{stored_course_code}:{stored_assignment_name}:{new_status}\n"
                    assignment_found = True
                file.write(line)
        if assignment_found:
            print("Assignment status updated successfully.")
        else:
            print("Assignment not found")
    except Exception as e:
        print("An error occured while updating the assignment status:", e)
    

    print("Logging out...")
    


if __name__ == "__main__":
    main()