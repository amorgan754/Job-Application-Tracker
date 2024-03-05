"""This application is a CLI menu driven application to track jobs that are applied for and their status using SQL"""

# imports
from datetime import datetime
import sqlite3 as sql
import sys

#Create table
connection = sql.connect('jobTracker.db')
cur = connection.cursor()

createTable = '''CREATE TABLE IF NOT EXISTS jobs ([jobTitle] VARCHAR(50), [companyname] VARCHAR(50), [jobStatus] VARCHAR(50), [appliedDate] VARCHAR(12), [updatedDate] VARCHAR(12))'''
cur.execute(createTable)

CURRENTDATE = datetime.today().date()


# functions

# function for inputting the job applied for
def inputJob():
    company = input("What is the company name?\n")
    jobTitle = input("What is the job title?\n")
    jobStatus = input("What is the current application status?\n")

    statement = f"INSERT INTO jobs VALUES ('{jobTitle}', '{company}', '{jobStatus}', '{CURRENTDATE}', '{CURRENTDATE}')"

    cur.execute(statement)
    connection.commit()
    print()

# function for updating the job status applied for
def updateJob():
    currentJobs()
    company = input("What is the company that you would like to update job status at?\n")
    jobStatus = input("What is the current job status?\n")

    statement = f"UPDATE jobs SET jobStatus = '{jobStatus}', updatedDate = '{CURRENTDATE}' WHERE companyname = '{company}'"

    cur.execute(statement)
    connection.commit()
    print()

# function to see current standings
def currentJobs():
    statement = """SELECT * FROM jobs;"""
    cur.execute(statement)
    display = cur.fetchall()
    connection.commit()
    print(tabulate(display, headers=['Job Title', 'Company', 'Job Status', 'Date Applied', 'Date Updated'], tablefmt='psql'))
    
    print()

#function to show based on job status
def selectSome():
    status = input("What job status are you wanting to see?\n")
    statement = f"SELECT * FROM jobs WHERE jobStatus = '{status}';"
    cur.execute(statement)
    display = cur.fetchall()
    connection.commit()
    print(tabulate(display, headers=['Job Title', 'Company', 'Job Status', 'Date Applied', 'Date Updated'], tablefmt='psql'))
    
    print()

#function to delete job
def deleteJob():
    currentJobs()
    company = input("What is the company that you would like to delete the job from?\n")
    jobTitle = input("What is the job title that you would like to delete?\n")
    statement = f"DELETE FROM jobs WHERE companyname = '{company}' AND jobTitle = '{jobTitle}'"

    cur.execute(statement)

    connection.commit()
    print()

# function to delete all
def deleteAll():
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

# menu
def menu():
    print("Option 1: Input a job that was applied for")
    print("Option 2: Update a job that was applied for")
    print("Option 3: Delete a job that was applied for")
    print("Option 4: Display current jobs")
    print("Option 5: Display jobs by status")
    print("Option 9: Delete the whole darn thing")
    print("Option 0: Exit the program")


#use while loop
CHOICE = None

#keeps running the while loop until selected to exit the program
while CHOICE != 0:
    menu()

    CHOICE = input("Please select a menu option number: \n")

    if CHOICE == "1":
        inputJob()
    elif CHOICE == "2":
        updateJob()
    elif CHOICE == "3":
        deleteJob()
    elif CHOICE == "4":
        currentJobs()
    elif CHOICE == "5":
        selectSome()
    elif CHOICE == "9":
        deleteAll()
    elif CHOICE == "0":
        exit_program()
    else:
        print("\nPlease make a valid choice\n")
