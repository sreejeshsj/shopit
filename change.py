import json
import os
import datetime

DATA_DIR = "todo_data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

class Task:
    def __init__(self, title, description="", category="General", deadline=None, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.deadline = deadline  # string YYYY-MM-DD or None
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "deadline": self.deadline,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data.get('description', ""),
            data.get('category', "General"),
            data.get('deadline', None),
            data.get('completed', False)
        )

    def __str__(self):
        status = "✓" if self.completed else "✗"
        deadline = self.deadline if self.deadline else "No deadline"
        return f"[{status}] {self.title} (Category: {self.category}, Deadline: {deadline})"

class User:
    def __init__(self, username):
        self.username = username
        self.tasks = []
        self.load_tasks()

    def get_tasks_file(self):
        return os.path.join(DATA_DIR, f"{self.username}_tasks.json")

    def load_tasks(self):
        file = self.get_tasks_file()
        if os.path.exists(file):
            with open(file, "r") as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in tasks_data]
        else:
            self.tasks = []

    def save_tasks(self):
        file = self.get_tasks_file()
        with open(file, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
            return True
        return False

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()
            return True
        return False

    def list_tasks(self, filter_status=None, filter_category=None):
        filtered = self.tasks
        if filter_status is not None:
            filtered = [t for t in filtered if t.completed == filter_status]
        if filter_category:
            filtered = [t for t in filtered if t.category.lower() == filter_category.lower()]
        return filtered

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username):
    users = load_users()
    if username in users:
        return False
    users.append(username)
    save_users(users)
    return True

def login_user(username):
    users = load_users()
    return username if username in users else None

def input_date(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD or leave blank): ").strip()
        if not date_str:
            return None
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD.")

def main_menu(user):
    print(f"\nWelcome, {user.username}!")
    while True:
        print("\nTo-Do List Menu:")
        print("1. View all tasks")
        print("2. View completed tasks")
        print("3. View pending tasks")
        print("4. Add new task")
        print("5. Mark task as completed")
        print("6. Delete a task")
        print("7. View tasks by category")
        print("8. Logout")

        choice = input("Choose an option (1-8): ").strip()

        if choice == '1':
            tasks = user.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nAll Tasks:")
                for idx, task in enumerate(tasks, 1):
                    print(f"{idx}. {task}")

        elif choice == '2':
            tasks = user.list_tasks(filter_status=True)
            if not tasks:
                print("No completed tasks.")
            else:
                print("\nCompleted Tasks:")
                for idx, task in enumerate(tasks, 1):
                    print(f"{idx}. {task}")

        elif choice == '3':
            tasks = user.list_tasks(filter_status=False)
            if not tasks:
                print("No pending tasks.")
            else:
                print("\nPending Tasks:")
                for idx, task in enumerate(tasks, 1):
                    print(f"{idx}. {task}")

        elif choice == '4':
            title = input("Task title: ").strip()
            description = input("Description (optional): ").strip()
            category = input("Category (default 'General'): ").strip() or "General"
            deadline = input_date("Deadline")
            if not title:
                print("Title is required!")
                continue
            task = Task(title, description, category, deadline)
            user.add_task(task)
            print("Task added successfully.")

        elif choice == '5':
            tasks = user.list_tasks(filter_status=False)
            if not tasks:
                print("No pending tasks to mark completed.")
                continue
            print("\nPending Tasks:")
            for idx, task in enumerate(tasks, 1):
                print(f"{idx}. {task}")
            idx_str = input("Enter task number to mark completed: ").strip()
            if idx_str.isdigit():
                idx_num = int(idx_str) - 1
                # we need to get the correct task index from full task list
                pending_tasks = [i for i, t in enumerate(user.tasks) if not t.completed]
                if 0 <= idx_num < len(pending_tasks):
                    user.mark_completed(pending_tasks[idx_num])
                    print("Task marked as completed.")
                else:
                    print("Invalid task number.")
            else:
                print("Invalid input.")

        elif choice == '6':
            if not user.tasks:
                print("No tasks to delete.")
                continue
            print("\nAll Tasks:")
            for idx, task in enumerate(user.tasks, 1):
                print(f"{idx}. {task}")
            idx_str = input("Enter task number to delete: ").strip()
            if idx_str.isdigit():
                idx_num = int(idx_str) - 1
                if user.delete_task(idx_num):
                    print("Task deleted.")
                else:
                    print("Invalid task number.")
            else:
                print("Invalid input.")

        elif choice == '7':
            category = input("Enter category name to filter: ").strip()
            if category:
                tasks = user.list_tasks(filter_category=category)
                if not tasks:
                    print(f"No tasks found in category '{category}'.")
                else:
                    print(f"\nTasks in category '{category}':")
                    for idx, task in enumerate(tasks, 1):
                        print(f"{idx}. {task}")
            else:
                print("Category cannot be empty.")

        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

def main():
    ensure_data_dir()
    print("=== Welcome to the To-Do List Manager ===")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            username = input("Choose a username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            if register_user(username):
                print(f"User '{username}' registered successfully.")
            else:
                print(f"Username '{username}' is already taken.")

        elif choice == '2':
            username = input("Enter username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            user = login_user(username)
            if user:
                user_obj = User(user)
                main_menu(user_obj)
            else:
                print("User not found. Please register first.")

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
