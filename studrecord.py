# Import os and json libraries
import os, json

# ========================================
# THESE ARE THE CONFIGURATION SETTINGS
# ALl of these can be modified.
# ========================================
CONFIG  = {
    # The passcode when attempting to modify the data.
    'passcode': '12345',

    # This is the file name of the data file where all the data is stored.
    'dataFile': 'students.dat',

    # How wide the displayed table would be?
    # Changing this to higher values makes the table more even.
    'columnPadding': 6
}

# ========================================
# The developers of this program
# All can be modified.
# ========================================
AUTHORS = {
    # Program design & logic
    'designer': '',
    # Lead programmer
    'lead_prog': '',
    # Assistant programmer
    'assist_prog': '',
    # Tester
    'tester': ''
}

# ========================================
# Clears the entire console
# ========================================
def clear():
    os.system('cls')

# ========================================
# Prepares the data file for storage
# Returns a Boolean
# ========================================
def prepareStorage():
    # Create an empty students list
    # This will serve as the empty list for the dictionaries that we will be inserting later on
    studentsList = []
    
    # Opening a file may throw some exception once it failed.
    try:
        # Open the data file in append mode
        # Or create it if it doesn't exist
        with open(CONFIG['dataFile'], 'a') as file:
            # Check first if the file is empty
            # Go to the end of the file
            file.seek(0, os.SEEK_END)
            
            # Check if the cursor has changed its position.
            # If it didn't, it means the file is empty.
            if file.tell() == 0:
                # Convert the data first into string
                # that can be stored into a file
                data = json.dumps(studentsList)
                
                # Save the data to the file.
                file.write(data)
    except:
        # Display an error message if the file does not open.
        print('Unable to access the data file.')
        return False
        
    return True

# ========================================
# Displays the main options of the program
# ========================================
def displayOptions():
    # A flag that tells if any of the commands has been entered
    # Cannot be modified.
    firstExec = True

    while True:
        clear()
        pad = 70
        print('=' * pad)
        print(f'{"STUDENT RECORD MANAGEMENT SYSTEM v 1.0":^{pad}}')
        print('=' * pad)

        # If the user selects a command for the first time...
        if firstExec:
            print('Welcome! Please select an option..\n')
        else:
            print('What would you like to do next?\n')

        print('Enter [A] to Add new student in record')
        print('Enter [E] to Update a student in record')
        print('Enter [D] to Delete a student in record')
        print('Enter [V] to View student records')
        print('Enter [W] to know the developer')
        print('Enter [X] to exit the program\n')
    
        # Prompt the option
        option = input('Enter your option: ')
    
        # Evaluates the chosen option
        if not evaluateOption(option): break
        else: firstExec = False

# ========================================
# Evaluates the chosen option
# Returns a Boolean
# ========================================
def evaluateOption(option):
    result = True # the return value
    
    # Only one character is allowed.
    if len(option) > 1:
        result = False
    
    option = option.lower() # make lowercase
    
    if option == 'a':
        promptAddStudent()
    elif option == 'e':
        promptEditStudent()
    elif option == 'd':
        promptDeleteStudent()
    elif option == 'v':
        displayData()
    elif option == 'w':
        displayCredits()
    elif option == 'x':
        result = False
    else:
        result = False
        
    # It's not the very first command entered anymore
    if result: firstExec = False
    
    return result

# ========================================
# Prompts the user to enter the passcode
# ========================================
def authenticate():
    clear()
    passcodeInput = ''

    while not passcodeInput == CONFIG['passcode']:
        passcodeInput = input('Enter the passcode to proceed: ')

        if not passcodeInput == CONFIG['passcode']:
            print('Wrong passcode.')

    input('Access granted! Press the Enter key to proceed.')

# ========================================
# This function does the validation of any input.
# It loops until the input is valid.
# Returns a string|float|int
# ========================================
def inputValidate(message, expectedType = ''):
    variable = None
    
    while True:
        variable = input(message)

        # break the loop if it's valid
        if not variable == '':
            if not expectedType == '':
                # converting a non-convertible value into int or float
                # will make the program throw an exception so better catch it ASAP
                try:
                    if expectedType == 'int':
                        variable = int(variable)
                    elif expectedType == 'float':
                        variable = float(variable)
                except:
                    print('Invalid entry')
                    continue
            else:
                # strip() removes any excess spaces (front & end)
                variable = variable.strip()

            break # important!

    return variable

# ========================================
# Prompts the user to add a student's info
# ========================================
def promptAddStudent():
    # Passcode required.
    authenticate()

    clear()
    isCancel = False
    pad = 50
    print("Add the student's information. Enter [C]/[c] to cancel.")
    print('=' * pad)

    while True:
        name = inputValidate('Full name: ')

        if name.lower() == 'c': return

        # Do a quick search here to check if the student already existed
        # before proceeding to avoid any conflicts in data processing
        if isStudentExists(name):
            print('This student was already added.')
        else:
            break

    # If the student is new, continue the prompt
    age     = inputValidate('Age: ', 'int')
    address = inputValidate('Address: ')
    number  = inputValidate('Contact number: ')
    course  = inputValidate('Course: ')

    # Next, store the data into a dictionary (JSON)
    data = {
        'name'   : name,
        'age'    : age,
        'address': address,
        'number' : number,
        'course' : course
    }

    # Store the data
    addStudent(data)

    input('Press Enter key to go back to menu.')

# ========================================
# Prompts the user to edit a student's info
# ========================================
def promptEditStudent():
    # Passcode required.
    authenticate()

    clear()
    pad = 50
    print("Edit student's information. Enter [C]/[c] to cancel.")
    print('=' * pad)

    studentToEdit = ''
    
    while True:
        studentToEdit = inputValidate('Enter the full name of the student you want to edit: ')

        if studentToEdit.lower() == 'c': return

        # Do a quick search here to check if the student already existed
        if not isStudentExists(studentToEdit):
            print('Student not found.')
        else: break

    # The user can skip editing some values.
    name    = inputValidate('Enter new name. [S]/[s] to skip: ')
    age     = inputValidate('Enter new age. [0] to skip: ', 'int')
    address = inputValidate('Enter new address. [S]/[s] to skip: ')
    number  = inputValidate('Enter new number. [S]/[s] to skip: ')
    course  = inputValidate('Enter new course. [S]/[s] to skip: ')

    # Next, store the data into a dictionary (JSON)
    data = {
        'name'   : name,
        'age'    : age,
        'address': address,
        'number' : number,
        'course' : course
    }

    # Update the data
    editStudent(studentToEdit, data)

    input('Press Enter key to go back to menu.')

# ========================================
# Prompts the user to delete a student
# Returns a Boolean
# ========================================
def promptDeleteStudent():
    # Passcode required.
    authenticate()

    clear()
    pad = 50
    print('Delete a student in the record. Enter [C]/[c] to cancel.')
    print('=' * pad)

    while True:
        studentToDelete = ''
        while True:
            studentToDelete = inputValidate('Enter the full name to delete in record: ')

            if studentToDelete.lower() == 'c': return

            # Do a quick search here to check if the student already existed
            if not isStudentExists(studentToDelete):
                print('Student not found.')
            else: break

        # Confirm
        print(f'Are you sure you want to delete "{studentToDelete}" in record?')
        confirm = input('[Y]/[y] - Yes [N]/[n] - No?: ')

        if confirm.lower() == 'y':
            deleteStudent(studentToDelete)
            break

    input('Press Enter key to go back to menu.')

# ========================================
# Displays the table of student records
# Returns a Boolean
# ========================================
def displayData():
    clear()
    # Retrieve the data from the file
    records = getRecords()

    # Check if there are any records
    if not records:
        print('There are no records.')
    else:
        # Create a new table instance
        table = Table(records, CONFIG['columnPadding'])
        # Display the table
        table.tabulate()

    input('Press Enter to go back to menu.')

# ========================================
# Displays the developers' info
# Returns a Boolean
# ========================================
def displayCredits():
    clear()
    pad = 70
    print('=' * pad)
    print(f'{"THE DEVELOPERS":^{pad}}')
    print(f'{"STUDENT RECORD MANAGEMENT SYSTEM v 1.0":^{pad}}')
    print(f'{"(c) 2022. All rights reserved.":^{pad}}')
    print('=' * pad)
    print()
    print(f'=> DESIGNER             : {AUTHORS["designer"]}')
    print(f'=> LEAD PROGRAMMER      : {AUTHORS["lead_prog"]}')
    print(f'=> ASSISTANT PROGRAMMER : {AUTHORS["assist_prog"]}')
    print(f'=> TESTER               : {AUTHORS["tester"]}')
    print()
    input('Press Enter to go back to menu.')

# ========================================
# TABLE CLASS
# We're not using any third-party libraries for the table formatting.
# We're gonna do everything from scratch ;)
# ========================================
class Table:
    # Table margin.
    # Access: private
    __startSpacing = 3
    
    # ========================================
    # Class constructor
    # Data should be a list
    # ========================================
    def __init__(self, data, padding = 0, separator = '|'):
        # Data to be displayed
        self.data = data
        # Table cell separator
        self.separator = separator
        # Table padding
        self.padding = padding

    # ========================================
    # Displays the table
    # Access: public
    # ========================================
    def tabulate(self):
        self.__printHeaders()
        self.__printRows()

    # ========================================
    # Prints the table headers
    # Access: private
    # ========================================
    def __printHeaders(self):
        # Make the first row as reference
        reference = self.data[0]
        row = self.separator
        left = f'{"":<{self.__startSpacing}}'
        maxTableWidth = self.__getMaxTableWidth()

        print('=' * maxTableWidth)
        print(f'{"STUDENT RECORDS":^{maxTableWidth}}')
        print('=' * maxTableWidth)
        
        # Iterate through a dictionary (columns)
        for key, value in reference.items():
            maxWidth = self.__getMaxColumnWidth(0, key)
            # Adjust the margin on the first column
            if next(iter(reference.keys())) == key:
                row += ' ' * len(left)
                        
            row += f' {key.upper():^{maxWidth}}{self.separator} '

        print(row)

    # ========================================
    # Prints the table rows
    # Access: private
    # ========================================
    def __printRows(self, test = False):
        # Iterate through the list (rows)
        for count, item in enumerate(self.data, 1):
            row = self.separator
            row += f'{str(count) + ".":<{self.__startSpacing}}'
            
            # Iterate through a dictionary (columns)
            for key, value in item.items():
                maxWidth = self.__getMaxColumnWidth(count -1, key)
                row += f' {value:<{maxWidth}}{self.separator} '
            
            if test:
                return len(row)
            else:
                print('-' * len(row))
                print(row)

                # If this is the last row, print another separator
                if count == len(self.data):
                    print('-' * len(row))

        return 0

    # ========================================
    # Returns the max table width possible
    # Access: private
    # ========================================
    def __getMaxTableWidth(self):
        return self.__printRows(True)

    # ========================================
    # Determines the max width for each column
    # Access: private
    # The max width is dependent on the text with the most number of characters
    # so we don't need to hardcode the padding, making each column width flexible
    # ========================================
    def __getMaxColumnWidth(self, rowIndex, columnName):
        # Look for the other cells of other rows if there are
        # any values that has the most number of characters.
        # If so, it will be the reference for the max column width
        maxWidth = len(str(self.data[rowIndex][columnName]))

        for item in self.data:
            toCompare = len(str(item[columnName]))
            if toCompare > maxWidth:
                maxWidth = toCompare
        
        return maxWidth + self.padding # add the padding

# ========================================
# Adds a student info to the record
# ========================================
def addStudent(data):
    records = getRecords()
    # append the new data into the end of the list and store the newly updated list back into the file
    records.append(data)

    # Commit the changes
    saveChanges(records)
    
    print(f"Successfully added \"{data['name']}\" in student's record!\n")

# ========================================
# Updates a student info
# ========================================
def editStudent(name, data):
    records = getRecords()
    recordToEdit = None

    # Look for the student to be edited
    index = 0
    for record in records:
        if record['name'].lower() == name.lower():
            # yes! that's the record that we're gonna edit
            recordToEdit = record
            break
        
        index += 1

    # Evaluate the skipped data (retain the old data if so)
    for key, value in data.items():
        if type(value) is str:
            value = value.lower()

        if value == 's' or value == 0:
            data[key] = recordToEdit[key]

    # Copy the contents of the new data into the record to be edited
    records[index] = data

    # Commit the changes
    saveChanges(records)

    print("Student's information in the record was updated successfully.\n")

# ========================================
# Deletes a student info
# ========================================
def deleteStudent(name):
    records = getRecords()
    recordToEdit = None

    # Look for the student to be deleted
    index = 0
    for record in records:
        if record['name'].lower() == name.lower():
            # yes! that's the record that we're gonna delete
            break
        
        index += 1

    del records[index]

    # Commit the changes
    saveChanges(records)

    print('Data was successfully deleted in records.\n')

# ========================================
# Checks if the student already exists
# Returns a Boolean
# ========================================
def isStudentExists(name):
    records = getRecords()
    
    # Check first if the student already exists
    # The "records" is a list, so we'll loop through it
    for record in records:
        if record['name'].lower() == name.lower():
            return True

    return False

# ========================================
# Writes a record into the data file
# ========================================
def saveChanges(data):
    # Open the file in write mode
    with open(CONFIG['dataFile'], 'w+') as file:
        # Convert the dictionary from JSON into string
        # indent it by 4 spaces for readability
        toStore = json.dumps(data, indent = 4)
        file.write(toStore)

# ========================================
# Retrieves all the records from the data file
# ========================================
def getRecords():
    records = None
    
    with open(CONFIG['dataFile'], 'r') as file:
        # Parse the file into objects
        records = json.loads(file.read())

    return records
    
# MAIN FUNCTION
if prepareStorage():
    displayOptions()
