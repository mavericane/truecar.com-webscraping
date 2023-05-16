# https://truecar.com - Web Scraping Project
## [`Version 1.0`](v1.0)
### Release note:
> Version 1.0 was released on May 16, 2023
>
> This version creates a CSV file and saves data in that CSV file and a MySQL database
### Requirements:
#### Virtual Environment:
> I recommend creating a virtual environment for any of the Python programs so that if a program caused a problem your main Python binary files will be safe.
>
> To create a virtual environment you can use the code below in the directory in which you want to create your virtual environment:
> ```
> python -m venv <Your-Virtual-Enviornment-Name>
> ```
#### MySQL:
> You need to be MySQL installed in your system up and running.
#### Required modules:
> Required modules list are listed in [`requirements.txt`](v1.0/requirements.txt)
>
> You can simply install the required modules by typing the code below in the project directory:
> ```
> pip install -r requirements.txt
> ```
### How to use:
> #### Step 1:
> Run [`Create-Database.py`](v1.0/Create-Database.py) to create a MySQL database and table. This file creates [`Database.py`](v1.0/Database.py) that already exists in the project directory and is included with test system database information.
>
> #### Step 2:
> Run [`Fetch_Used_Cars.py`](v1.0/Fetch_Used_Cars.py) to fetch and store the list of the used cars by entering the car brand, car name, and the number of pages that you want to fetch and store from https://www.truecar.com/used-cars-for-sale/listings/.
>
> [`Fetch_Used_Cars.py`](v1.0/Fetch_Used_Cars.py) uses [`Database.py`](v1.0/Database.py) information to connect and store data in your database so make sure you have done [`Step 1`](README.md#step-1).
>
> [`Fetch_Used_Cars.py`](v1.0/Fetch_Used_Cars.py) creates a CSV file named [`fetch_log.csv`](v1.0/fetch_log.csv) that already exists in the project directory filled with 50 pages of fetched data from cars that are available at [`cars_list.txt`](v1.0/cars_list.txt) total data: 19445 cars until [`Mon 15 May 06:46:08 +0330 2023`](v1.0/fetch_data_date.txt)

Enjoy Data & Program

👨‍💻 Author: Amin (Mavericane)

🔗 Github Link: https://github.com/mavericane/

🔗 Website Link: https://mavericane.ir
