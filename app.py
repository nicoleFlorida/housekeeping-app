 

import sqlite3

def record_task():
    room = input("Enter room number: ")
    task = input("Enter task  completed: ")

    conn = sqlite3.connect("housekeeping.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (room, task) VALUES (?, ?)",
        (room, task)
    )

    conn.commit()
    conn.close()

    print("Task completed and saved!")

def view_room():
    room = input("Enter room number to view: ")

    conn = sqlite3.connect("housekeeping.db")
    cursor = conn.cursor()

    cursor.execute(
       "SELECT task, completed_at FROM tasks WHERE room = ?",
       (room,)
    )

    tasks = cursor.fetchall()
    conn.close()

    if tasks:
       print(f"\nTask history for room {room}")
       print("--------------------------")

       for task, date in tasks:
           print(task, "-", date)

    else:
       print("No tasks found for this room.")

while True:
    print("\nHOUSEKEEPING TASK TRACKER")
    print("--------------------------")
    print("1. Record completed task")
    print("2. View room history")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        record_task()
    elif choice == "2":
        view_room()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
		

