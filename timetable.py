
#Declaring global courses to be used in functions
courses = {

        1: {
            "name": "Programming Principles",
            "grouping": {
                1: "PEP1: G1-G3, 8am - 10am",
                2: "PEP2: G4-G6, 3pm - 5pm"
            }
        },
        2:{
            "name": "Mathematics",
            "grouping": {
                1: "MT1: G1-G3, 8:15am - 10:15am",
                2: "MT2: G4-G6, 3:30pm - 5:30pm"
            }
        },
        3: {
            "name": "Web Design",
            "grouping": {
                1: "WD1: G1-G3, 10am - 12pm",
                2: "WD2: G4-G6, 1pm - 3pm"
            }
        },
        4: {
            "name": "Database Fundamentals",
            "grouping": {
                1: "DF1: G1-G3, 8:30am - 10:30am",
                2: "DF2: G4-G6 2pm - 4pm"
            }
        },
        5: {
            "name": "English",
            "grouping": {
                1: "ENG 1: G1-G3, 9am-11am",
                2: "ENG 2: G4-G6, 4pm-6pm"
            }
        }
    }

#Create student timetable
def createTimetable(studentID):
    print("Available Courses:")
    for courseID, courseInfo in courses.items():
        print(f"{courseID}. {courseInfo['name']}")
        for key, value in courseInfo["grouping"].items():
            print(f"   {key}. {value}")
    
    timetable = []
    registeredCourses = set()  #To check for already registered courses.
    try:
        amount = int(input("How many courses do you want to register for?: "))
        if amount <= 0:
            print("You must register for at least one course.")
            return
    except ValueError:
        print("Please enter a valid number of courses.")
    #Reiterates based on amount of courses to be registered
    for i in range(amount):
        try:
            choice = int(input("Select a course (Enter 0 to exit): "))  
            if choice == 0:
                break
            elif choice in courses:
                if choice in registeredCourses:
                    print("You have already registered for this course.") 
                    continue
                else:
                    registeredCourses.add(choice)  
                    print(f"Course selected: {courses[choice]['name']}")
                    for key, value in courses[choice]["grouping"].items():
                        print(f"   {key}. {value}")
                    timeslot = int(input("Select a course timeslot: "))
                    if timeslot in courses[choice]["grouping"]:
                        newTimetable = courses[choice]["grouping"][timeslot]
                        timetable.append(newTimetable)
                    else:
                        print("Invalid timeslot choice.")
            else:
                print("Invalid course choice.")
        except ValueError:
            print("Please enter an integer")

    print("Courses successfully registered.")
    #Write to text file
    with open("timetables_StudentID.txt", "a") as file:
        file.write(f"\n{studentID}:\n")
        for entry in timetable:
            file.write(entry + "\n")
        file.write("\n")

#Adding a new course
def addCourse():
    try:
        courseName = input("Enter the name of the course: ")
        courseCode = input("Enter course code: ")
        amount = int(input("How many groups? "))
        courseGrouping = {}  
        for i in range(amount):
            group = input("Enter group: ")
            time = input("Enter timeslot: ")
            courseGrouping[i + 1] = f"{group}, {time}"  
        courses[courseCode] = {'name': courseName, 'grouping': courseGrouping}  
        print("Course added successfully")
        return courses
    except ValueError:
        print("Please enter appropriate values")
    
def viewCourse(studentID):
    found = False
    with open("timetables_StudentID.txt", "r") as file:
        for line in file:
            if line.strip() == str(studentID) + ":": #Looks for StudentID
                found = True
                print("Your timetable is: ")
            elif found:
                if line.strip() == "":
                    found = False  
                    break #Stops when reaches end of timetable for the specified student
                print(line.strip())

def updateCourse(courseID):
    if courseID not in courses:
        print("Invalid course ID.")
        return
    print(f"Current details for course {courseID} are as follows: ")
    print(f"Name: {courses[courseID]['name']}")
    print("Grouping: ")
    for key, value in courses[courseID]['grouping'].items():
        print(f"{key}. {value}")

    print("What would you like to update?")
    print("1. Course Name")
    print("2. Course Details")
    try:
        choice = int(input("Your choice : "))
    except ValueError:
        print("Please enter a valid choice")
    if choice == 1:
        newName = input("Enter new course name: ")
        courses[courseID]['name'] = newName
    elif choice == 2:
        amount = int(input("How many groups?"))
        for i in range(amount):
            newCode = input("Enter new course code: ")
            newGrouping = input("Enter groups: ")
            newTimeslot = input("Enter timeslot: ")
        courseDetails = f"{newCode}, {newGrouping}, {newTimeslot}"
        courses[courseID] = {'grouping': {1:courseDetails}}
    
def deleteCourse(courseID):
    if courseID not in courses:
        print("Invalid Course ID.")
        return
    
    courseName = courses[courseID]['name']
    del courses[courseID]
    print(f"Course {courseName} was deleted successfully.")

    newCourses = {}
    index = 1
    for courseID, courseDetails in courses.items():
        newCourses[index] = courseDetails
        index += 1
    courses.clear()
    courses.update(newCourses)

def courseMenu():
    print("Course Menu")
    print("1. View all available courses")
    print("2. Register for Courses")
    print("3. View timetable")
    print("4. Exit")
    try:
        query = int(input("Enter your choice (1-4): "))
    except ValueError:
        print("Please enter a number")
    return query

def courseList():
    print("Available Courses:")
    for courseID, courseInfo in courses.items():
        print(f"{courseID}. {courseInfo['name']}")
        for key, value in courseInfo["grouping"].items():
            print(f"   {key}. {value}")

