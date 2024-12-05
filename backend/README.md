# Backend Project Setup Guide

This guide helps you set up and run the backend project for development purposes.

---

## Prerequisites

- **Python**: Ensure you have Python `3.13.0` installed.
- **Virtual Environment**: Install a virtual environment manager (e.g., `venv`).

---

## Setup Instructions

### 1. Clone the Repository
Clone the project repository from GitHub:
```bash
git clone <repository_url>
cd <repository_folder>
```
### 2. Create and Activate Virtual Environment
Create and activate a virtual environment:

```bash
Copy code
python -m venv .venv
source env/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3. Install Requirements
Install the project dependencies:

```bash
pip install -r requirements.txt
```
---
## Configuration
### 1. Update settings.py
Ensure INSTALLED_APPS includes your custom apps.
```bash
INSTALLED_APPS = [
    ...
    'cruise_management',
    ...
]
```
### 2. Create a .env File
The .env file is ignored in the .gitignore. Create one in the backend folder and add the following variables:
```bash
SECRET_KEY=your_django_secret_key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```
---
## Database Setup
### 1. Generate Models from Existing Database
Run the following command to inspect your database schema and generate models:

```bash
python -Xutf8  manage.py inspectdb > cruise_management/models.py 
```
#### Common Error:
- models.py may save in UTF-16 encoding. When the file is saved in UTF-16, inspectdb command will throw an error. If this happens:
- Open the file and copy its content.
- Create a new file with UTF-8 encoding.
- Paste the content into the new file and save it as models.py under cruise_management.
- Run inspectdb again.

### 2. Apply Migrations
Run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```
### 3. Running the Server
Start the development server on a custom port:

```bash
python manage.py runserver <port_number>
```
Example:
```bash
python manage.py runserver 8080
```
---
## Additional Notes
- Ensure sensitive keys and credentials are stored securely.
