
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

#save courses to a text file
def saveCourses(courses):
    with open("courses.txt", "w") as file:
        for courseID, courseInfo in courses.items():
            file.write(f"{courseID}. {courseInfo['name']}\n")
            for option, details in courseInfo['grouping'].items():
                file.write(f"   {option}. {details}\n")
            file.write("\n") #spacing for clarity

#read text file for courses
def loadCourses():
    loadedCourses = {}
    with open("courses.txt", "r") as file:
        courseID = 1 #index
        courseInfo = {}
        for line in file:
            if line.strip():  
                if line.startswith(" "):  #Grouping
                    parts = line.strip().split(". ")
                    groupID = int(parts[0])
                    groupInfo = parts[1]
                    courseInfo["grouping"][groupID] = groupInfo
                else:  #CourseName
                    if courseInfo:
                        loadedCourses[courseID] = courseInfo
                        courseID += 1
                    courseInfo = {}
                    parts = line.strip().split(". ")
                    courseInfo["name"] = parts[1]
                    courseInfo["grouping"] = {}
        # Add the last course
        if courseInfo:
            loadedCourses[courseID] = courseInfo
    return loadedCourses

courses = loadCourses()

#Create student timetable
def createTimetable(studentID):
    courses = loadCourses()
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
            print("You must register for at least one course.") #Error Handling
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
    courses = loadCourses()
    try:
        nextIndex = max(courses.keys(), default = 0) + 1
        courseName = input("Enter the name of the course: ")
        if courseName in courses:
            print("Course already exists.") #Error Handling
        amount = int(input("How many groups? "))
        courseGrouping = {}  
        for i in range(amount):
            courseCode = input("Enter course code: ")
            group = input("Enter group: ")
            time = input("Enter timeslot: ")
            courseGrouping[i + 1] = f"{courseCode}: {group}, {time}"  
        courses[nextIndex] = {'name': courseName, 'grouping': courseGrouping}  
        print("Course added successfully")
        saveCourses(courses) #Save new courses
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
    courses = loadCourses()
    if courseID not in courses:
        print("Invalid course ID.")
        return
    #For clarity
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
        if choice == 1:
            newName = input("Enter new course name: ")
            courses[courseID]['name'] = newName
        elif choice == 2:
            amount = int(input("How many groups? "))
            newDetails = {}
            for i in range(amount):
                newCode = input("Enter new course code: ")
                newGrouping = input("Enter groups: ")
                newTimeslot = input("Enter timeslot: ")
                newDetails[i + 1] = f"{newCode}: {newGrouping}, {newTimeslot}"
            courses[courseID]['grouping'] = newDetails
        else:
            print("Please enter a valid choice.")
            return
        saveCourses(courses) #Save new course details
        print("Course details updated successfully.")
    except ValueError:
        print("Please enter a number.")
    
def deleteCourse(courseID):
    courses = loadCourses()
    if courseID not in courses:
        print("Invalid Course ID.")
        return
    courseName = courses[courseID]['name']
    del courses[courseID]
    print(f"Course {courseName} was deleted successfully.")

    newCourses = {}
    index = 1
    for oldcourseID, courseInfo in courses.items():
        newCourses[index] = courseInfo
        index += 1 #Reindex the entries so that its coherent
    courses.clear()
    courses.update(newCourses)
    saveCourses(courses)

def courseMenu():
    #for clarity
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
    #for ease of use
    courses = loadCourses()
    print("Available Courses:")
    for courseID, courseInfo in courses.items():
        print(f"{courseID}. {courseInfo['name']}")
        for key, value in courseInfo["grouping"].items():
            print(f"   {key}. {value}")

