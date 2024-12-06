# Seed MySQL Database with Python Script

This Python script (`seed.py`) is designed to set up and populate a MySQL database named `ALX_prodev`. It creates a table named `user_data` with predefined fields, and populates it with sample data from a CSV file (`user_data.csv`).

---

## **Features**
1. Connects to a MySQL server.
2. Creates the `ALX_prodev` database if it doesn't exist.
3. Creates the `user_data` table with the following fields:
   - `user_id`: UUID (Primary Key, Indexed)
   - `name`: `VARCHAR`, Not NULL
   - `email`: `VARCHAR`, Not NULL
   - `age`: `DECIMAL`, Not NULL
4. Reads data from `user_data.csv`.
5. Inserts data into the `user_data` table, ensuring no duplicate entries.

---

## **Requirements**
- Python 3.x
- MySQL Server
- Required Python packages:
  - `mysql-connector-python`

---

## **Setup Instructions**

### **1. Clone or Download the Repository**
Download the script and CSV file to your local machine.

### **2. Install Python and Required Packages**
Ensure Python 3 is installed on your system. Then, install the `mysql-connector-python` package:
```bash
pip install mysql-connector-python
3. Configure MySQL
Start your MySQL server and ensure you have access credentials (e.g., username and password).

Usage Instructions
1. Prepare the CSV File
Ensure the user_data.csv file is in the same directory as the seed.py script. The CSV file should have the following structure:

csv
Copy code
name,email,age
John Doe,john@example.com,30
Jane Doe,jane@example.com,25
...
2. Run the Script
Open your terminal, navigate to the script's directory, and execute:

bash
Copy code
python seed.py

