# Sales Stats Dashboard

This project retrieves and analyzes sales statistics from a MySQL database and presents the results in a Pandas DataFrame. The script calculates various metrics such as actual revenue, lost revenue, total orders, total closed orders, total canceled orders, canceled value, and closed value.

## Prerequisites

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- Pandas
- MySQL Connector (install using `pip install mysql-connector-python`)

## Configuration

1. Open the script in a code editor.
2. Update the database credentials (`host`, `user`, `passwd`, and `db_name` if applicable) to match your MySQL database.
3. Save the changes.

## Running the Script

Execute the script by running the following command in your terminal:

```bash
magento_sales_data.py
```

## Output
The script will connect to the specified database, execute a SQL query to retrieve sales statistics, and display the results in a Pandas DataFrame.


