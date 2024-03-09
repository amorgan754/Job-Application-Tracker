"""This application is a CLI menu driven application to track jobs that are applied for and their status using SQL"""

# imports
from datetime import datetime
import sqlite3 as sql
import sys
from tabulate import tabulate

#Create table
connection = sql.connect('jobTracker.db')
cur = connection.cursor()

createTable = '''CREATE TABLE IF NOT EXISTS jobs ([jobTitle] VARCHAR(50), [companyname] VARCHAR(50), [jobStatus] VARCHAR(50), [appliedDate] VARCHAR(12), [updatedDate] VARCHAR(12))'''
cur.execute(createTable)

CURRENTDATE = datetime.today().date()


# functions

# function for inputting the job applied for
def inputJob():
    """This function is to input into the table"""
    company = input("What is the company name?\n")
    jobTitle = input("What is the job title?\n")
    jobStatus = input("What is the current application status?\n")

    statement = f"INSERT INTO jobs VALUES ('{jobTitle}', '{company}', '{jobStatus}', '{CURRENTDATE}', '{CURRENTDATE}')"

    cur.execute(statement)
    connection.commit()
    print()

# function for updating the job status applied for
def updateJob():
    """This function is to update one job based on company"""
    currentJobs()
    company = input("What is the company that you would like to update job status at?\n")
    jobStatus = input("What is the current job status?\n")

    parameters = (jobStatus, company)

    statement = f"UPDATE jobs SET jobStatus = ?, updatedDate = '{CURRENTDATE}' WHERE companyname = ?"

    cur.execute(statement, parameters)
    connection.commit()
    print()

# function to mass update jobs
def massUpdate():
    """This function is to do a mass update based on job status"""
    currentJobs()
    jobStatus = input("What is the status you would like to update?\n")
    newStatus = input("What is the new status of the jobs?\n")

    parameters = (newStatus, jobStatus)

    statement = f"UPDATE jobs SET jobStatus = ?, updatedDate = '{CURRENTDATE}' WHERE jobStatus = ?"

    cur.execute(statement, parameters)
    connection.commit()
    print()

# function to see current standings
def currentJobs():
    count = 0
    """This function is to display all the jobs that are not denied"""
    statement = f"SELECT * FROM jobs WHERE jobStatus = 'In Progress' OR jobStatus = 'Submitted'"
    cur.execute(statement)
    display = cur.fetchall()
    connection.commit()
    print(tabulate(display, headers=['Job Title', 'Company', 'Job Status', 'Date Applied', 'Date Updated'], tablefmt='psql'))
    for results in display:
        count+=1
    print("There is currently", count, "applications that you have submitted")
    
    print()


# function to see current standings
def allJobs():
    """This function is to show all jobs"""
    count = 0

    statement = f"SELECT * FROM jobs"
    cur.execute(statement)
    display = cur.fetchall()
    connection.commit()
    print(tabulate(display, headers=['Job Title', 'Company', 'Job Status', 'Date Applied', 'Date Updated'], tablefmt='psql'))

    for results in display:
        count+=1

    print("There is currently", count, "applications that you have submitted")

    print()


#function to show based on job status
def selectSome():
    """This function is to select jobs based on status"""
    status = input("What job status are you wanting to see?\n")

    parameters = (status)

    statement = f"SELECT * FROM jobs WHERE jobStatus = ?;"
    cur.execute(statement, parameters)
    display = cur.fetchall()
    connection.commit()
    print(tabulate(display, headers=['Job Title', 'Company', 'Job Status', 'Date Applied', 'Date Updated'], tablefmt='psql'))
    
    print()

#function to delete job
def deleteJob():
    """This function is to delete jobs based on company and job title"""
    currentJobs()
    company = input("What is the company that you would like to delete the job from?\n")
    jobTitle = input("What is the job title that you would like to delete?\n")

    parameters = (company, jobTitle)

    statement = f"DELETE FROM jobs WHERE companyname = '{company}' AND jobTitle = '{jobTitle}'"

    cur.execute(statement, parameters)

    connection.commit()
    print()

# function to delete all
def deleteAll():
    """This function is to delete the entire table"""
    statement = f"DELETE FROM jobs"
    cur.execute(statement)
    connection.commit()
    currentJobs()
    print()


# exit application
def exit_program():
    """This function is to exit the program"""
    print("Thank you for using our program!")
    sys.exit(0)

# main menu
def mainMenu():
    """This function is to display the main menu"""
    print("Option 1: Update table information")
    print("Option 2: Display table information")
    print("Option 0: Exit the program")

# updates menu
def updateMenu():
    """This function is to run through the options of updating the table"""
    CHOICE = None
    while CHOICE != 0:
        print("Current Options:")
        print("Option 1: Input a job applied for")
        print("Option 2: Update a job applied for")
        print("Option 3: Mass update a status")
        print("Option 4: Delete a job applied for")
        print("Option 5: Delete the whole table")
        print("Option 0: Return to the main menu")

        print()

        CHOICE = int(input("Please select a menu option number: \n"))

        if CHOICE == 1:
            inputJob()
        elif CHOICE == 2:
            updateJob()
        elif CHOICE == 3:
            massUpdate()
        elif CHOICE == 4:
            deleteJob()
        elif CHOICE == 5:
            deleteAll()



# Display menu
def displayMenu():
    """This function is to run through the options of displaying the table"""
    CHOICE = None
    while CHOICE != 0:
        print("Current Options:")
        print("Option 1: Display all current jobs")
        print("Option 2: Display all jobs")
        print("Option 3: Display specific jobs")
        print("Option 0: Return to the main menu")

        print()

        CHOICE = int(input("Please select a menu option number: \n"))
        if CHOICE == 1:
            currentJobs()
        elif CHOICE == 2:
            allJobs()
        elif CHOICE == 3:
            selectSome()


#use while loop
CHOICE = None

#keeps running the while loop until selected to exit the program
while CHOICE != 0:
    mainMenu()

    CHOICE = int(input("Please select a menu option number: \n"))

    if CHOICE == 1:
        updateMenu()
    elif CHOICE == 2:
        displayMenu()
    elif CHOICE == 0:
        exit_program()
    else:
        print("\nPlease make a valid choice\n")
