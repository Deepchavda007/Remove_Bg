
## Installation and Setup

### Step 1: Create a Virtual Environment

First, create a virtual environment to manage the dependencies separately for this project. Open your terminal and run the following command:

```bash
python3 -m venv env/remove_bg
```

### Step 2: Activate the Virtual Environment

Depending on your operating system, activate the virtual environment using one of the following commands:

#### For Windows
```bash
.\remove_bg\Scripts\activate
```

#### For Mac & Linux
```bash
source remove_bg/bin/activate
```

### Step 3: Install Required Packages

Install the necessary packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Running the Application on Linux (Optional)

If you are using Linux, you can use `screen` to run the application in a separate session.

#### Creating a New Screen Session
```bash
screen -S remove_bg
```

To return to the session:
```bash
screen -r remove_bg
```

### Step 5: Run the Flask API

Run the Flask API using the following command:

```bash
python3 app.py
```