import json

TASKS_FILE = "tasks.json"


# load and save tasks
def load_tasks(filename=TASKS_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []  # first run: no file yet, start with an empty list
    except json.JSONDecodeError:
        print("Warning: tasks.json was unreadable/corrupted. Starting fresh.")
        tasks = []
    else:
        print(f"Loaded {len(tasks)} task(s) from {filename}.")
    return tasks


def save_tasks(tasks, filename=TASKS_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"Error: could not save tasks ({e}).")


# helper function
def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# display menu
def display_menu():
    print("\n===== TASK MANAGER =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Update task")
    print("4. Delete task")
    print("5. Complete task")
    print("6. Exit")
    print("=========================")


# add task
def add_task(tasks):
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    task = {
        "id": next_id(tasks),
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks) 
    print(f"Task added (id={task['id']}).")


# view tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    print("\n-- Your Tasks --")
    for t in tasks:
        status = "✔ done" if t["completed"] else "  open"
        print(f"[{t['id']:>3}] {status}  {t['title']}")


# helper function
def prompt_for_task(tasks, action_word):
    try:
        task_id = int(input(f"ID of task to {action_word}: "))
    except ValueError:
        print("Please enter a number.")
        return None
    
    print(f"Looking for id={task_id!r}, tasks currently = {tasks}")
    task = find_task(tasks, task_id)
    if task is None:
        print("No task with that ID.")
    return task


# update task
def update_task(tasks):
    task = prompt_for_task(tasks, "update")
    if task is None:
        return

    new_title = input(f"New title (leave blank to keep '{task['title']}'): ").strip()
    if new_title:
        task["title"] = new_title
        save_tasks(tasks)
        print("Task updated.")
    else:
        print("No change made (empty title).")


# delete task
def delete_task(tasks):
    task = prompt_for_task(tasks, "delete")
    if task is None:
        return

    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted.")


# complete task
def complete_task(tasks):
    task = prompt_for_task(tasks, "complete")
    if task is None:
        return

    if task["completed"]:
        print("That task is already marked complete.")
    else:
        task["completed"] = True
        save_tasks(tasks)
        print("Task marked complete.")


# main menu
def main():
    tasks = load_tasks()
    running = True

    while running:
        display_menu()
        choice = input("> ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            complete_task(tasks)
        elif choice == "6":
            running = False
            print("Goodbye!")
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()