import os
from datetime import datetime
from collections import defaultdict

def create_report(user_id, username, company, email, tasks):
    report_filename = f'tasks/{username}.txt'

    # Check if the file already exists
    try:
        if os.path.exists(report_filename):
            # Rename the existing file with the old timestamp
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M')
            os.rename(report_filename, f'tasks/old_{username}_{timestamp}.txt')
    except FileNotFoundError as e:
        print(f'File not found: {e}')

    # Count completed and uncompleted tasks
    completed_tasks = sum(1 for task in tasks if task['completed'])
    uncompleted_tasks = len(tasks) - completed_tasks

    # Create the report content
    report_content = [
        f"# Отчёт для {company}.",
        f"{username} <{email}> {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"Всего задач: {len(tasks)}",
        "",
        f"## Актуальные задачи ({uncompleted_tasks}):",
    ]

    # Add uncompleted tasks to the report
    for task in tasks:
        if not task['completed']:
            task_title = task['title'][:46] + '...' if len(task['title']) > 46 else task['title']
            report_content.append(f"- {task_title}")

    # Add completed tasks to the report
    report_content.extend([
        "",
        f"## Завершённые задачи ({completed_tasks}):",
    ])

    for task in tasks:
        if task['completed']:
            task_title = task['title'][:46] + '...' if len(task['title']) > 46 else task['title']
            report_content.append(f"- {task_title}")

    # Write the report to the file
    try:
        with open(report_filename, 'w') as report_file:
            report_file.write('\n'.join(report_content))
    except PermissionError as e:
        print(f'Permission error: {e}')
