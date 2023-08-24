# Author: Amin (Mavericane)
# Github Link: https://github.com/mavericane/
# Website Link: https://mavericane.ir
# Description: This file fetches the list of used cars from truecar.com according to the brand and name of the entered car and stores it in the database and table already created in the Create-Database.py program and saved on Database.py.
# Importing required modules
# requests module for fetching web contents into the program
import requests

# termcolor module for colorizing outputs
import termcolor

# mysql.connector module for connecting to the database and saving fetched data from the web
import mysql.connector

# re(regex) module for exact search of phrases in texts
import re

# bs4 module for classifying phrases fetched from websites
from bs4 import BeautifulSoup

# Checking if Database.py exists
try:
    import Database
except:
    print(
        termcolor.colored(
            "Database.py doesn't exist please run Create-Database.py to create a database and table",
            "red",
            "on_black",
        )
    )
    exit()

# Connecting to database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user=Database.database_user,
        password=Database.database_pass,
        database=Database.database_name,
    )
except:
    print(
        "There is an error in connecting the database check your Database.py file and run Create-Database.py if that does not work contact the developer"
    )
# Finding running file location
file_location = __file__.split("/")
file_location_string = "/"
for i in range(len(file_location)):
    if i == 0 or file_location[i] == file_location[-1]:
        None
    else:
        file_location_string += file_location[i] + "/"


# Function to check if fetched car exists in the database via VIN
def car_exists_in_database(vin):
    query = f'SELECT car_vin FROM {Database.table_name} WHERE car_vin = "{vin}"'
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    car_exists_in_database = False
    for item in myresult:
        result = re.search(r"(\w+)", str(item))
        if result.group(0) == vin:
            car_exists_in_database = True
    return car_exists_in_database


# Function to retry loading pages
def retry_loading_pages(number):
    print(termcolor.colored(f"Error loading page {counter}", "red", "on_black"))
    print(termcolor.colored(f"Attempt {number+1}. Retrying...", "green", "on_black"))


# Request brand name and car name from the user
car_brand = input(
    "Please enter brand of car you looking for (for example: Toyota): "
).casefold()
car_name = input(
    "Please enter name of car you looking for (for example: Camry): "
).casefold()
# Default URL
url = "https://www.truecar.com/used-cars-for-sale/listings/"
# Trying to send a request for the default URL
while True:
    try:
        request = requests.get(url + car_brand + "/" + car_name + "/", timeout=10)
        break
    except:
        print(
            termcolor.colored(
                "Error loading default URL please run the program again",
                "red",
                "on_black",
            )
        )
        while True:
            retry = input(
                "Do you want to retry loading the default URL? (y for yes | n for no): "
            )
            if retry.casefold() == "n":
                exit()
            elif retry.casefold() == "y":
                print(termcolor.colored("Retrying...", "green", "on_black"))
                break
            else:
                print("The input is not correct")
soup = BeautifulSoup(request.text, "html.parser")
# Checking available pages to fetch
available_pages = soup.find_all(
    "li", attrs={"data-test": "paginationItem", "class": "hidden-sm-down page-item"}
)
if len(available_pages) != 0:
    for i in range(len(available_pages)):
        if i == len(available_pages) - 1:
            available_pages_number = available_pages[i].text
else:
    print(f"There is no used car with brand_name: {car_brand} and car_name: {car_name}")
    print("This might be a network error please try again a few times")
    exit()
print(f"There is {available_pages_number} pages available")
# Requesting how many pages user want to fetch
while True:
    pages_user_want = input(
        f"Enter how many pages you want to fetch from website (number between 1 and {available_pages_number}): "
    )
    if pages_user_want.isdigit():
        if int(pages_user_want) <= 0 or int(pages_user_want) > int(
            available_pages_number
        ):
            print(f"Enter number between 1 and {available_pages_number}")
        else:
            break
    else:
        print("The input is not correct")
print(
    termcolor.colored(
        "Note: if VIN is printed in green color it means it doesn't exist in the database and it will be added if it's printed in red it means it's been already in the database.",
        "yellow",
        "on_black",
    )
)
# Fetching data and writing to database and CSV file
request_retry_error_counter = 0
data_process_retry_error_counter = 0
counter = 1
while counter <= int(pages_user_want):
    # Loading URL with page number
    print(f"Loading page {counter}")
    # Trying to send request
    try:
        request = requests.get(
            url + car_brand + "/" + car_name + "/" + "?page=" + str(counter), timeout=1
        )
    except:
        if request_retry_error_counter < 3:
            retry_loading_pages(request_retry_error_counter)
            request_retry_error_counter += 1
            continue
        else:
            print(
                termcolor.colored(
                    f"3 try attempts to load page {counter} are not effective.",
                    "red",
                    "on_black",
                )
            )
            print(
                termcolor.colored(
                    f"Skipping page number {counter}", "yellow", "on_black"
                )
            )
            request_retry_error_counter = 0
            counter += 1
            continue
    # Trying to process data from request
    try:
        soup = BeautifulSoup(request.text, "html.parser")
        cars_vin = soup.find_all(
            "div", attrs={"class": "vehicle-card-vin-carousel mt-1 text-xs"}
        )
        cars_model = soup.find_all("span", attrs={"class": "vehicle-card-year text-xs"})
        cars_options = soup.find_all(
            "div", attrs={"class": "truncate text-xs", "data-test": "vehicleCardTrim"}
        )
        cars_worked = soup.find_all(
            "div", attrs={"class": "truncate text-xs", "data-test": "vehicleMileage"}
        )
        cars_color = soup.find_all(
            "div",
            attrs={
                "class": "vehicle-card-location mt-1 truncate text-xs",
                "data-test": "vehicleCardColors",
            },
        )
        cars_condition = soup.find_all(
            "div",
            attrs={
                "class": "vehicle-card-location mt-1 text-xs",
                "data-test": "vehicleCardCondition",
            },
        )
        cars_price = soup.find_all(
            "div",
            attrs={
                "class": "heading-3 my-1 font-bold",
                "data-qa": "Heading",
                "data-test": "vehicleCardPricingBlockPrice",
            },
        )
        # Check if page loaded correctly
        if (
            len(cars_vin) == 0
            or len(cars_model) == 0
            or len(cars_options) == 0
            or len(cars_worked) == 0
            or len(cars_color) == 0
            or len(cars_condition) == 0
            or len(cars_price) == 0
        ):
            if request_retry_error_counter < 3:
                retry_loading_pages(request_retry_error_counter)
                request_retry_error_counter += 1
                continue
            else:
                print(
                    termcolor.colored(
                        f"3 try attempts to load page {counter} are not effective.",
                        "red",
                        "on_black",
                    )
                )
                print(
                    termcolor.colored(
                        f"Skipping page number {counter}", "yellow", "on_black"
                    )
                )
                request_retry_error_counter = 0
                counter += 1
                continue
        mycursor = mydb.cursor()
        query = f"INSERT INTO {Database.table_name} (car_brand, car_name, car_model, car_options, car_price, car_worked, car_color, car_condition, car_vin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in range(len(cars_vin)):
            if car_exists_in_database(cars_vin[i].text):
                print("VIN: " + termcolor.colored(cars_vin[i].text, "red"))
            else:
                print("VIN: " + termcolor.colored(cars_vin[i].text, "green"))
                val = (
                    car_brand.capitalize(),
                    car_name.capitalize(),
                    cars_model[i].text,
                    cars_options[i].text,
                    cars_price[i].text,
                    cars_worked[i].text,
                    cars_color[i].text,
                    cars_condition[i].text,
                    cars_vin[i].text,
                )
                mycursor.execute(query, val)
                mydb.commit()
                car = (
                    car_brand.capitalize()
                    + ","
                    + car_name.capitalize()
                    + ","
                    + cars_model[i].text
                    + ","
                    + cars_options[i].text
                    + ","
                    + '"'
                    + cars_price[i].text
                    + '"'
                    + ","
                    + '"'
                    + cars_worked[i].text
                    + '"'
                    + ","
                    + cars_color[i].text
                    + ","
                    + cars_condition[i].text
                    + ","
                    + cars_vin[i].text
                )
                with open(
                    f"{file_location_string}" + "fetch_log.csv", "a"
                ) as fetch_log:
                    fetch_log.write(f"{car}")
                    fetch_log.write("\n")
                    fetch_log.close()
    except:
        print(
            termcolor.colored(
                f"An error occurred while processing the data on page {counter}",
                "red",
                "on_black",
            )
        )
        if data_process_retry_error_counter < 3:
            data_process_error_retry = True
            print(
                termcolor.colored(
                    f"Attempt {data_process_retry_error_counter+1}. Retrying...",
                    "green",
                    "on_black",
                )
            )
            data_process_retry_error_counter += 1
        else:
            data_process_retry_error_counter = 0
            data_process_error_retry = False
            print(
                termcolor.colored(
                    f"Skipping page number {counter}. This happens after 4 times error in processing data",
                    "yellow",
                    "on_black",
                )
            )
        if data_process_error_retry:
            continue
    request_retry_error_counter = 0
    counter += 1
print(
    termcolor.colored(
        f'You have successfully fetched {pages_user_want} pages for "{car_brand.capitalize()}" "{car_name.capitalize()}" from the used cars list on https://truecar.com',
        "green",
        "on_black",
    )
)
