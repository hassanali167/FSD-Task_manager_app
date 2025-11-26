import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_FILE = 'tasks.json'

# --- PART A: Backend Logic & OOP ---

class Task:
    """
    Task class as required by Assignment Part A - 2. OOP [cite: 23]
    """
    def __init__(self, task_id, title, description, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    def to_dict(self):
        """Helper to convert object to dictionary for JSON storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }

def load_tasks():
    """
    Reads tasks from JSON file. Handles exceptions. [cite: 11, 36]
    """
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return [] # Return empty list if JSON structure is invalid [cite: 38]

def save_tasks(tasks):
    """
    Writes list of tasks to JSON file.
    """
    with open(DB_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# --- PART B: Flask Web Application ---

# 1. Home Page 
@app.route('/')
def index():
    return render_template('index.html')

# 2. Add Task Page 
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        tasks = load_tasks()
        
        # Auto-generate ID [cite: 57]
        # Using max ID + 1 to avoid conflicts if tasks are deleted
        if tasks:
            new_id = max(t['task_id'] for t in tasks) + 1
        else:
            new_id = 1
            
        # Create Task Object
        new_task_obj = Task(new_id, title, description)
        
        # Save to list and write to file
        tasks.append(new_task_obj.to_dict())
        save_tasks(tasks) # [cite: 58]
        
        return redirect(url_for('view_tasks'))
    return render_template('add.html')

# 3. View Tasks Page [cite: 59]
@app.route('/tasks')
def view_tasks():
    tasks = load_tasks()
    
    # Bonus: Filter Feature [cite: 79]
    filter_status = request.args.get('filter')
    if filter_status == 'Pending':
        tasks = [t for t in tasks if t['status'] == 'Pending']
    elif filter_status == 'Completed':
        tasks = [t for t in tasks if t['status'] == 'Completed']
        
    return render_template('tasks.html', tasks=tasks)

# 4. Update Task Page [cite: 68]
@app.route('/update', methods=['GET', 'POST'])
def update_task():
    message = None
    search_id = request.args.get('search_id')
    task_found = None
    
    tasks = load_tasks()

    # If we are searching for a task to populate the form
    if search_id:
        for task in tasks:
            if task['task_id'] == int(search_id):
                task_found = task
                break
        if not task_found:
            message = "Task not found" # [cite: 73]

    # If we are submitting the update
    if request.method == 'POST':
        task_id = int(request.form['task_id'])
        new_desc = request.form['description']
        is_completed = 'completed' in request.form # Checkbox logic
        
        updated = False
        for task in tasks:
            if task['task_id'] == task_id:
                task['description'] = new_desc
                if is_completed:
                    task['status'] = "Completed"
                updated = True
                break
        
        if updated:
            save_tasks(tasks)
            return redirect(url_for('view_tasks'))
        else:
            message = "Task not found"

    return render_template('update.html', task=task_found, message=message)

# 5. Delete Task Page 
@app.route('/delete', methods=['GET', 'POST'])
def delete_task():
    message = None
    if request.method == 'POST':
        try:
            task_id = int(request.form['task_id'])
            tasks = load_tasks()
            
            # Filter out the task with the matching ID
            initial_count = len(tasks)
            tasks = [t for t in tasks if t['task_id'] != task_id]
            
            if len(tasks) < initial_count:
                save_tasks(tasks)
                return redirect(url_for('view_tasks')) # Redirect on success [cite: 76]
            else:
                message = "Task not found" # [cite: 77]
        except ValueError:
            message = "Invalid ID"

    return render_template('delete.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
