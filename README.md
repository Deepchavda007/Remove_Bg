<p>
  <div align="center">
  <h1>
<br >
    Remove_BG - Setup Guide<br /> <br />
    <a href="https://github.com/psf/black">
      <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="The Uncompromising Code Formatter"
      />
    </a>
      <a>
      <img
        src="https://img.shields.io/badge/python-3.9%20%7C%203.10-blue"
        alt="Python Versions"
      />
    </a>
  </h1>
      
  </div>
  <h3>Welcome to the setup guide for the Remove_BG Module. Follow these steps to get your environment ready and run the application.</h3>
</p>

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

## API Endpoints:
  - The application provides the following endpoints:
### /remove_bg
- **Method**: POST
- **Description**: This endpoint removes the background from an image provided via a public URL and returns a URL to the processed image stored in Amazon S3 along with a unique identifier.
- **Request Body**:
  ```json
   {
      "image_url": "https://example.com/path/to/image.jpg"
   }
  ```
- **Response**:
  - **Success**:
     ```json
     {
        "data": {
            "remove_bg_url": "https://s3.amazonaws.com/bucketname/path/to/processed_image.png",
            "unique_id": "2520b722-140f-497e-ad5d-b637d180da59"
        },
        "message": "Background removed successfully",
        "status": true
       }
    ```
