import json
import os

# Colors
RESET = '\033[0m'
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'

FILE = "todos.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(todos):
    with open(FILE, "w") as f:
        json.dump(todos, f, indent=4)

def priority_color(priority):
    return {"Low": GREEN, "Medium": YELLOW, "High": RED}.get(priority, RESET)

def progress_bar(todos, length=30):
    if not todos:
        return "[No tasks]"
    done_count = sum(1 for t in todos if t["done"])
    total = len(todos)
    filled = int(length * done_count / total)
    return f"[{'#'*filled}{'-'*(length-filled)}] {done_count}/{total} done"

def list_todos(todos):
    if not todos:
        print("No tasks found.\n")
        return
    print("\nYour Tasks:")
    for i, todo in enumerate(todos, 1):
        status = f"{GREEN}✅{RESET}" if todo["done"] else f"{RED}❌{RESET}"
        color = priority_color(todo["priority"])
        print(f"{i}. [{status}] {todo['task']} (Priority: {color}{todo['priority']}{RESET})")
    print(progress_bar(todos), "\n")

def add_todo(todos):
    task = input("Task: ").strip()
    priority = input("Priority (Low/Medium/High): ").strip().capitalize()
    todos.append({"task": task, "priority": priority, "done": False})
    save_data(todos)
    print(f"{CYAN}Task added.{RESET}\n")

def delete_todo(todos):
    list_todos(todos)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(todos):
            removed = todos.pop(index)
            save_data(todos)
            print(f"{MAGENTA}Deleted task:{RESET} {removed['task']}\n")
        else:
            print("Invalid number.\n")
    except ValueError:
        print("Invalid input.\n")

def mark_done(todos):
    list_todos(todos)
    try:
        index = int(input("Enter task number to mark as done: ")) - 1
        if 0 <= index < len(todos):
            todos[index]["done"] = True
            save_data(todos)
            print(f"{GREEN}Marked as done:{RESET} {todos[index]['task']}\n")
        else:
            print("Invalid number.\n")
    except ValueError:
        print("Invalid input.\n")

def main():
    todos = load_data()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{CYAN}CLI Notes / Todo Manager{RESET}")
        print(f"{GREEN}1.{RESET} List tasks")
        print(f"{GREEN}2.{RESET} Add task")
        print(f"{GREEN}3.{RESET} Delete task")
        print(f"{GREEN}4.{RESET} Mark task as done")
        print(f"{GREEN}5.{RESET} Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            list_todos(todos)
            input("Press Enter to continue...")
        elif choice == "2":
            add_todo(todos)
        elif choice == "3":
            delete_todo(todos)
        elif choice == "4":
            mark_done(todos)
        elif choice == "5":
            break
        else:
            print("Invalid choice.\n")
            time.sleep(1)

if __name__ == "__main__":
    main()
