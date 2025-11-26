import json
import os

# CONSTANT for file path
DB_FILE = 'tasks.json'

# PART A - 2. Object-Oriented Programming [cite: 22]
class Task:
    def __init__(self, task_id, title, description, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    # Method to mark as completed [cite: 28]
    def mark_completed(self):
        self.status = "Completed"

    # Method to update description [cite: 29]
    def update_description(self, new_desc):
        self.description = new_desc

    # Method to display info [cite: 31]
    def display_task_info(self):
        return f"ID: {self.task_id} | {self.title} - {self.status}"

# PART A - 1. Data Handling & 3. Exception Handling [cite: 11, 35]
def load_tasks():
    if not os.path.exists(DB_FILE):
        return [] # Return empty list if file missing [cite: 37]
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return [] # Handle invalid JSON [cite: 38]

def save_tasks(tasks):
    with open(DB_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)
