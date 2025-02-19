import pandas as pd
from sqlalchemy import create_engine
from database import engine2

def excel_to_mysql():
    # Load the Excel file
    excel_path = r'C:\Users\Oladimeji Oladepo\Desktop\Projects\Fast-Bitfumes\sms.xlsx'
    db_name = "SMS"
    table_name = "sms"
    mysql_user = "oladimeji"
    mysql_password = "mysqlpass"
    mysql_host='localhost'
    mysql_port=3306

    try:
        df = pd.read_excel(excel_path)
        print(f"Loaded data from {excel_path} successfully.")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Create the MySQL engine
    # try:
    #     engine = create_engine("mysql+mysqlconnector://oladimeji:mysqlpass@localhost:3307/SMS")
    #     print("MySQL connection successful.")
    # except Exception as e:
    #     print(f"Error creating MySQL engine: {e}")
    #     return

    # Write DataFrame to MySQL
    try:
        df.to_sql(name=table_name, con=engine2, if_exists='append', index=False)
        print(f"Data successfully inserted into `{table_name}` table.")
    except Exception as e:
        print(f"Error inserting data into MySQL table: {e}")

# Usage
# excel_path = 'your_excel_file.xlsx'
# db_name = 'your_database'
# table_name = 'your_table'
# mysql_user = 'your_username'
# mysql_password = 'your_password'
# excel_path = r'C:\Users\Oladimeji Oladepo\Desktop\Projects\Fast-Bitfumes\sms.xlsx'
# db_name = "SMS"
# table_name = "sms"
# mysql_user = "oladimeji"
# mysql_password = "mysqlpass"
#excel_to_mysql(excel_path, db_name, table_name, mysql_user, mysql_password)
