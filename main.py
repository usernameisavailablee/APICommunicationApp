import os
import requests
from datetime import datetime
from collections import defaultdict
from configuration.api_configuration import ApiConfiguration
from reports.create_report import create_report

try:
    if not os.path.exists('tasks'):
        os.mkdir('tasks')
except OSError as e:
    print(f'Failed to create directory: {e}')
    exit(1)


try:
    # Fetch data from the APIs
    tasks_response = requests.get(ApiConfiguration.TASKS_API)
    users_response = requests.get(ApiConfiguration.USERS_API)

    # Check for successful API responses
    tasks_response.raise_for_status()
    users_response.raise_for_status()

    tasks_data = tasks_response.json()
    users_data = users_response.json()
except requests.exceptions.RequestException as e:
    print(f'Failed to fetch data from the APIs: {e}')
    exit(1)
except json.JSONDecodeError as e:
    print(f'Error decoding JSON data: {e}')
    exit(1)


# Create a dictionary to store tasks for each user
user_tasks = defaultdict(list)

for task in tasks_data:
    user_id = task['userId']
    user_tasks[user_id].append(task)

# Create reports for each user
for user in users_data:
    user_id = user['id']
    username = user['username']
    company = user['company']['name']
    email = user['email']
    tasks = user_tasks[user_id]
    create_report(user_id, username, company, email, tasks)

print('Reports have been generated.')
