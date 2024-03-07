# ChatApp

ChatApp is a simple chat application built with Flask, a lightweight web framework for Python. This README provides instructions on how to set up and run ChatApp on your local machine.

## Prerequisites

Make sure you have the following installed on your system:

- Python (version 3.6 or higher)
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Getting Started

### 1. Clone the Repository

If you haven't already, clone the ChatApp repository to your local machine using Git:

```bash
git clone https://github.com/andrenguyening/ChatApp.git
```

### 2. Create Virtual Environment and install requirements.txt
Open a command prompt and cd to the location of which you cloned the project. Create a virtual environment:

 ``` python3 -m venv .venv```
 
 Activate the environment with:
 
 ```. .venv/bin/activate```
 
 Install all the requirements using pip:
 
 ```pip install -r requirements.txt```

### 3. Initialize the DB and start the application:
Set the FLASK_APP environment variable:
```export FLASK_APP=chat.py```

To initialize the database:
```flask initdb```

Start the flask server:
flask run
