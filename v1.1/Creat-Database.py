# Author: Amin (Mavericane)
# Github Link: https://github.com/mavericane/
# Website Link: https://mavericane.ir
# Description: This file creates a database with a table to receive and store used cars on the https://truecar.com website
# Importing required modules
# mysql.connector module for connecting to the database and saving fetched data from the web
import mysql.connector

# re(regex) module for exact search of phrases in texts
import re

# termcolor module for colorizing outputs
import termcolor


# Checking the presence or absence of database
def does_database_exists(database_name):
    mycursor.execute("SHOW DATABASES")
    database_exists = False
    for item in mycursor:
        result = re.search(r"(\w+)", str(item))
        if result.group(0) == database_name:
            database_exists = True
    return database_exists


# Creating database with checking presence or absence of database
def create_database(database_name):
    if does_database_exists(database_name):
        print(
            termcolor.colored(
                f'Database named with "{database_name}" is already exist',
                "red",
                "on_black",
            )
        )
        return False
    else:
        mycursor.execute(f"CREATE DATABASE {database_name}")
        print(
            termcolor.colored(
                f'The database named "{database_name}" was created', "green", "on_black"
            )
        )
        return True


# Checking the presence or absence of table in database
def does_table_exists(database_name, table_name):
    mycursor.execute(f"USE {database_name}")
    mycursor.execute("SHOW TABLES")
    table_exists = False
    for item in mycursor:
        result = re.search(r"(\w+)", str(item))
        if result.group(0) == table_name:
            table_exists = True
    return table_exists


# Creating table with checking presence or absence of table in database
def create_table(database_name, table_name):
    if does_table_exists(database_name, table_name):
        print(
            termcolor.colored(
                f'Table named with "{table_name}" is already exist in "{database_name}"',
                "red",
                "on_black",
            )
        )
        return False
    else:
        mycursor.execute(f"USE {database_name}")
        mycursor.execute(
            f"CREATE TABLE {table_name} (car_brand varchar(255), car_name varchar(255), car_model varchar(255), car_options varchar(255), car_price varchar(255), car_worked varchar(255), car_color varchar(255), car_condition varchar(255), car_vin varchar(255))"
        )
        print(
            termcolor.colored(
                f'The table named "{table_name}" was created in "{database_name}"',
                "green",
                "on_black",
            )
        )
        return True


# Get database information from the user
print('Using "localhost" for database host')
while True:
    try:
        database_user = input("Please enter your database username: ")
        database_pass = input("Please enter your database password: ")
        mydb = mysql.connector.connect(
            host="localhost", user=database_user, password=database_pass
        )
        break
    except:
        print(
            "Cant connect to mysql database\nplease enter your database information correctly"
        )
mycursor = mydb.cursor()
# Selecting database name to create
print('The default name for database is "truecar"')
while True:
    use_default_name = input(
        "Do you want to use default name for database? (y for Yes / n for No): "
    )
    if use_default_name.casefold() == "y":
        database_name = "truecar"
        create_database(database_name)
        break
    elif use_default_name.casefold() == "n":
        database_name = input("Please enter database name you wish to create for: ")
        if database_name.casefold() == "truecar":
            print("You are using default database name")
            create_database(database_name)
            break
        else:
            create_database(database_name)
            break
    else:
        print("The input is not correct")
# Selecting table name to create in database
print('The default name for table is "used_cars"')
while True:
    use_default_name = input(
        "Do you want to use default name for table in your database? (y for Yes / n for No): "
    )
    if use_default_name.casefold() == "y":
        table_name = "used_cars"
        create_table(database_name, table_name)
        break
    elif use_default_name.casefold() == "n":
        table_name = input(
            "Please enter table name you wish to create for in your database: "
        )
        if table_name.casefold() == "used_cars":
            print("You are using default table name")
            create_table(database_name, table_name)
            break
        else:
            create_table(database_name, table_name)
            break
    else:
        print("The input is not correct")
mydb.close()
# Finding running file location
file_location = __file__.split("/")
file_location_string = "/"
for i in range(len(file_location)):
    if i == 0 or file_location[i] == file_location[-1]:
        None
    else:
        file_location_string += file_location[i] + "/"
# Saving Database name and Table name in Database.py to use in Fetch_Used_Cars.py
with open(f"{file_location_string}" + "Database.py", "w") as Database:
    Database.write("# Author: Amin (Mavericane)")
    Database.write("\n")
    Database.write("# Github Link: https://github.com/mavericane/")
    Database.write("\n")
    Database.write("# Website Link: https://mavericane.ir")
    Database.write("\n")
    Database.write(
        "# Description: This file created by Create-Database.py to be used in Fetch_Used_Cars.py"
    )
    Database.write("\n")
    Database.write(f'database_user = "{database_user}"')
    Database.write("\n")
    Database.write(f'database_pass = "{database_pass}"')
    Database.write("\n")
    Database.write(f'database_name = "{database_name}"')
    Database.write("\n")
    Database.write(f'table_name = "{table_name}"')
    Database.write("\n")
    Database.close()
