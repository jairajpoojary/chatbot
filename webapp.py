from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, date

app = Flask(__name__)
tasks = []  # Store tasks with text, description, priority, deadline, created, completed

template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Advanced To-Do Manager</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .completed-task { text-decoration: line-through; color: gray; }
    .priority-High { background-color: #dc3545; color: white; }
    .priority-Medium { background-color: #ffc107; color: black; }
    .priority-Low { background-color: #198754; color: white; }
    .overdue { color: #dc3545; font-weight: bold; }
  </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">Advanced To-Do Manager</a>
  </div>
</nav>
<div class="container">
  <div class="card p-4 shadow-sm mb-4">
    <h2 class="mb-4">Add a New Task</h2>
    <form method="POST" action="/add" class="row g-3">
      <div class="col-md-6">
        <input type="text" name="task" class="form-control" placeholder="Task title" required>
      </div>
      <div class="col-md-6">
        <select name="priority" class="form-select" required>
          <option value="High">High Priority</option>
          <option value="Medium" selected>Medium Priority</option>
          <option value="Low">Low Priority</option>
        </select>
      </div>
      <div class="col-md-12">
        <textarea name="description" class="form-control" rows="2" placeholder="Optional description"></textarea>
      </div>
      <div class="col-md-6">
        <label for="deadline" class="form-label">Deadline (optional)</label>
        <input type="date" name="deadline" class="form-control" min="2020-01-01">
      </div>
      <div class="col-md-6 d-grid align-self-end">
        <button type="submit" class="btn btn-primary">Add Task</button>
      </div>
    </form>
  </div>

  {% if tasks %}
    <div class="mb-3">
      <label for="filter" class="form-label">Filter tasks:</label>
      <select id="filter" class="form-select" onchange="window.location.href='/?filter=' + this.value">
        <option value="all" {% if current_filter == 'all' %}selected{% endif %}>All</option>
        <option value="pending" {% if current_filter == 'pending' %}selected{% endif %}>Pending</option>
        <option value="completed" {% if current_filter == 'completed' %}selected{% endif %}>Completed</option>
      </select>
    </div>
  {% endif %}

  {% if tasks %}
    {% set completed_count = tasks|selectattr('completed')|list|length %}
    {% set progress = ((completed_count / tasks|length) * 100) | round(0) %}
    <h4>Progress</h4>
    <div class="progress mb-4">
      <div class="progress-bar" role="progressbar" style="width: {{ progress }}%;" aria-valuenow="{{ progress }}" aria-valuemin="0" aria-valuemax="100">{{ progress }}%</div>
    </div>
  {% endif %}

  <h3>Tasks</h3>
  {% if tasks %}
  <ul class="list-group">
    {% for task in tasks %}
      <li class="list-group-item">
        <div class="d-flex justify-content-between align-items-start">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" onchange="location.href='/toggle/{{ loop.index0 }}'" id="taskCheck{{ loop.index0 }}" {% if task.completed %}checked{% endif %}>
            <label class="form-check-label {% if task.completed %}completed-task{% endif %}" for="taskCheck{{ loop.index0 }}">
              <strong>{{ task.text }}</strong>
            </label>
            <br>
            <small>{{ task.description }}</small><br>
            <small>Created on: {{ task.created.strftime('%Y-%m-%d %H:%M') }}</small><br>
            <small>Priority: <span class="badge priority-{{ task.priority }}">{{ task.priority }}</span></small><br>
            {% if task.deadline %}
              {% set dead_date = task.deadline.strftime('%Y-%m-%d') %}
              <small>Deadline: 
                {% if task.deadline < today and not task.completed %}
                  <span class="overdue">{{ dead_date }} (Overdue!)</span>
                {% else %}
                  {{ dead_date }}
                {% endif %}
              </small>
            {% endif %}
          </div>
          <div class="btn-group btn-group-sm">
            <a href="/edit/{{ loop.index0 }}" class="btn btn-warning">Edit</a>
            <a href="/delete/{{ loop.index0 }}" class="btn btn-danger">Delete</a>
          </div>
        </div>
      </li>
    {% endfor %}
  </ul>
  {% else %}
  <p class="text-muted">No tasks added yet. Start by adding one above!</p>
  {% endif %}

  <hr>
  <h3>AI-Powered Task Summary</h3>
  <p>{{ summary }}</p>
</div>
<footer class="mt-5 py-3 bg-light text-center">
  <div class="container">
    <small>Advanced To-Do Manager &copy; 2025. CRUD app with AI features.</small>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    filter_param = request.args.get('filter', 'all')

    # Filter tasks based on query param
    if filter_param == 'pending':
        filtered_tasks = [t for t in tasks if not t['completed']]
    elif filter_param == 'completed':
        filtered_tasks = [t for t in tasks if t['completed']]
    else:
        filtered_tasks = tasks

    today = date.today()

    # AI feature: summary
    incomplete_tasks = [t for t in filtered_tasks if not t['completed']]
    if not tasks:
        summary = "You have no tasks. Enjoy your free time!"
    elif not incomplete_tasks:
        summary = f"All tasks are completed! Great job!"
    else:
        summary = f"You have {len(incomplete_tasks)} pending tasks. Top pending task: '{incomplete_tasks[0]['text']}'"

    return render_template_string(template, tasks=filtered_tasks, summary=summary, current_filter=filter_param, today=today)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    task_description = request.form.get('description', '')
    priority = request.form.get('priority', 'Medium')
    deadline_str = request.form.get('deadline', '')
    deadline_date = None
    if deadline_str:
        try:
            deadline_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            deadline_date = None

    if task_text:
        tasks.append({
            'text': task_text,
            'description': task_description,
            'priority': priority,
            'deadline': deadline_date,
            'created': datetime.now(),
            'completed': False
        })
    return redirect(url_for('home'))

@app.route('/toggle/<int:index>', methods=['GET'])
def toggle_complete(index):
    if 0 <= index < len(tasks):
        tasks[index]['completed'] = not tasks[index]['completed']
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['GET'])
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return redirect(url_for('home'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_task(index):
    if request.method == 'POST':
        new_task_text = request.form.get('task')
        new_task_description = request.form.get('description', '')
        new_priority = request.form.get('priority', 'Medium')
        new_deadline_str = request.form.get('deadline', '')
        new_deadline_date = None
        if new_deadline_str:
            try:
                new_deadline_date = datetime.strptime(new_deadline_str, '%Y-%m-%d').date()
            except ValueError:
                new_deadline_date = None

        if 0 <= index < len(tasks):
            tasks[index]['text'] = new_task_text
            tasks[index]['description'] = new_task_description
            tasks[index]['priority'] = new_priority
            tasks[index]['deadline'] = new_deadline_date
        return redirect(url_for('home'))
    else:
        if 0 <= index < len(tasks):
            task = tasks[index]
        else:
            task = {'text':'', 'description':'', 'priority':'Medium', 'deadline':None}
        edit_template = '''
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Edit Task</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
        <div class="container mt-4">
          <h1>Edit Task</h1>
          <form method="POST" class="row g-3">
            <div class="col-md-6">
              <input type="text" name="task" class="form-control" value="{{ task.text }}" required>
            </div>
            <div class="col-md-6">
              <select name="priority" class="form-select" required>
                <option value="High" {% if task.priority == 'High' %}selected{% endif %}>High Priority</option>
                <option value="Medium" {% if task.priority == 'Medium' %}selected{% endif %}>Medium Priority</option>
                <option value="Low" {% if task.priority == 'Low' %}selected{% endif %}>Low Priority</option>
              </select>
            </div>
            <div class="col-md-12">
              <textarea name="description" class="form-control" rows="2" placeholder="Optional description">{{ task.description }}</textarea>
            </div>
            <div class="col-md-6">
              <label for="deadline" class="form-label">Deadline (optional)</label>
              <input type="date" name="deadline" class="form-control" value="{{ task.deadline.strftime('%Y-%m-%d') if task.deadline else '' }}">
            </div>
            <div class="col-md-6 d-grid align-self-end">
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
          <a href="/" class="btn btn-secondary mt-3">Cancel</a>
        </div>
        </body>
        </html>
        '''
        return render_template_string(edit_template, task=task)

if __name__ == '__main__':
    app.run(debug=True)
