# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# reads tasks from "tasks.txt"
def read_tasks():
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    return task_list
# reads the passwords from "user.txt"
def read_users():
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
    return username_password
# prompts user to enter username and password - logs into system if correct
def login(username_password):
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
    return curr_user
# registers new user and writes it to "user.txt"
def register_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
        return
    else:
        print("Passwords do not match")
# prompts user to assign the person to named task, if valid user writes to "tasks.txt"
def add_task(task_list, username_password):
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")
# displays all tasks assigned to all users
def view_all_tasks(task_list):
    for t in task_list:
        print("_"*90)
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("_"*90)
# displays own tasks assigned to self and allows user to complete or edit
# if user choice is complete locks editing
# if user choice is edit allows to assign task to another user and edit due date
def view_my_tasks(task_list, curr_user):
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    if not user_tasks:
        print("You have no tasks assigned.")
        return
    for i, t in enumerate(user_tasks):
        print("_"*90 +"\n")
        disp_str = f"{i + 1}. Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("_"*90)
    while True:
        task_choice = int(input("Enter the task number to select a specific task or enter -1 to return to the main menu: "))
        if task_choice == -1:
            break
        elif 1 <= task_choice <= len(user_tasks):
            selected_task = user_tasks[task_choice - 1]
            if selected_task['completed']:
                print("This task is already completed and cannot be edited.")
                continue
            print("1. Mark task as complete")
            print("2. Edit task")
            action_choice = int(input("Enter your choice (1 or 2): "))
            if action_choice == 1:
                selected_task['completed'] = True
                print("Task marked as complete.")
            elif action_choice == 2:
                print("1. Edit assigned username")
                print("2. Edit due date")
                edit_choice = int(input("Enter your choice (1 or 2): "))
                if edit_choice == 1:
                    new_username = input("Enter new username: ")
                    if new_username in username_password:
                        selected_task['username'] = new_username
                        print("Username updated.")
                    else:
                        print("User does not exist. Please enter a valid username.")
                elif edit_choice == 2:
                    while True:
                        try:
                            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                            new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            selected_task['due_date'] = new_due_date_time
                            print("Due date updated.")
                            break
                        except ValueError:
                            print("Invalid datetime format. Please use the format specified.")
                else:
                    print("Invalid choice, please try again.")
# generates report files and "task_overview.txt" and "user_overview.txt", prompts user when succesful
def generate_reports(task_list, username_password):
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < datetime.now().date())
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Incomplete tasks percentage: {uncompleted_tasks / total_tasks * 100:.2f}%\n")
        task_overview_file.write(f"Overdue tasks percentage: {overdue_tasks / total_tasks * 100:.2f}%\n")
    total_users = len(username_password.keys())
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")
        for username in username_password:
            user_tasks = [t for t in task_list if t['username'] == username]
            user_task_count = len(user_tasks)
            user_completed_tasks = sum(1 for t in user_tasks if t['completed'])
            user_uncompleted_tasks = user_task_count - user_completed_tasks
            user_overdue_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < date.today())
            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Tasks assigned: {user_task_count}\n")
            if user_task_count > 0:
                user_overview_file.write(f"Task percentage: {user_task_count / total_tasks * 100:.2f}%\n")
                user_overview_file.write(f"Completed tasks percentage: {user_completed_tasks / user_task_count * 100:.2f}%\n")
                user_overview_file.write(f"Incomplete tasks percentage: {user_uncompleted_tasks / user_task_count * 100:.2f}%\n")
                user_overview_file.write(f"Overdue tasks percentage: {user_overdue_tasks / user_task_count * 100:.2f}%\n")
    print("Reports generated successfully.")
# displays to the user the generated report files "task_overview.txt" and "user_overview.txt"
def display_statistics(username_password, task_list):
    if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
        generate_reports(task_list, username_password)

    print("_"*92 + "\nTask Overview:")
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())

    print("_"*92 + "\nUser Overview:")
    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())
# main loop to call functions and execute task management system
# if user is admin allows to register users, generate reports and display statistics
def main_menu(username):
    is_admin = username == "admin"
    while True:
        print("\nMENU")
        print("r - Register user" if is_admin else "")
        print("a - Add task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("gr - Generate reports" if is_admin else "")
        print("ds - Display statistics" if is_admin else "")
        print("e - Exit\n")
        user_choice = input("Enter your choice: ").lower()
        if user_choice == "r" and is_admin:
            register_user(username_password)
        if user_choice == "a":
            add_task(task_list, username_password)
        elif user_choice == "va":
            view_all_tasks(task_list)
        elif user_choice == "vm":
            view_my_tasks(task_list, username)
        elif user_choice == "gr" and is_admin:
            generate_reports(task_list, username_password)
        elif user_choice == "ds" and is_admin:
            display_statistics(username_password, task_list)
        elif user_choice == "e":
            print("Goodbye!")
            exit()
        else:
            print("You have made a wrong choice, please try again.")
if __name__ == "__main__":
    task_list = read_tasks()
    username_password = read_users()
    curr_user = login(username_password)
    main_menu(curr_user)
# For this task I used my previous knowledge from HyperionDev Bootcamp, freecodecamp, CodeAcademy and Udemy Course by Angela Yu on Python to complete.