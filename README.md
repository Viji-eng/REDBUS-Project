# Assignment_1
REDBUS Data Scraping Project Documentation
Table of Contents
Introduction
Prerequisites
Project Setu
Scraping Logic
Database Management
Streamlit Application
Running the Application
Conclusion
1. Introduction
This project aims to scrape bus data from the REDBUS website using Selenium, store the information in a MySQL database using PyMySQL, and create a user-friendly interface using Streamlit. The project will help in gathering data on bus schedules, prices, and availability.

2. Prerequisites
Before starting the project, ensure you have the following installed:

Python 3.x
MySQL Server
Required Python libraries:
Selenium
PyMySQL
Streamlit
Install the libraries using pip:
pip install selenium, pymysql, streamlit
Additionally, you will need a compatible WebDriver for Selenium (e.g., ChromeDriver for Google Chrome).

3. Project Setup
3.1 Directory Structure
redbus_scraper/
│
├── scraper.py           # Main scraping script
├── database.py          # Database interaction functions
├── app.py               # Streamlit app
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation




3.2 Configuration
Create a configuration file to store database credentials:

python
Copy code
# config.py
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'redbus_data'
4. Scraping Logic
  4.1 Initializing Selenium
Use Selenium to launch a browser and navigate to the REDBUS site.

python
Copy code
from selenium import webdriver

def initialize_driver():
    driver = webdriver.Chrome(executable_path='path/to/chromedriver')
    driver.get('https://www.redbus.in/')
    return driver
  4.2 Scraping Data
Implement the scraping logic to gather bus data (e.g., origin, destination, date, price, etc.).

python
Copy code
def scrape_bus_data(driver):
    # Example: Locate elements on the page and extract text
    buses = driver.find_elements_by_class_name('bus-item')
    bus_data = []
    
    for bus in buses:
        name = bus.find_element_by_class_name('name').text
        price = bus.find_element_by_class_name('price').text
        # Add other fields as needed
        bus_data.append({'name': name, 'price': price})

    return bus_data





5. Database Management
5.1 Connecting to MySQL
Use PyMySQL to connect to the MySQL database and insert the scraped data.

python
Copy code
import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def connect_db():
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return connection
5.2 Inserting Data
Create a function to insert the scraped data into the database.

python
Copy code
def insert_bus_data(connection, bus_data):
    with connection.cursor() as cursor:
        for bus in bus_data:
            cursor.execute("INSERT INTO buses (name, price) VALUES (%s, %s)", (bus['name'], bus['price']))
        connection.commit()
6. Streamlit Application
Create a Streamlit app to display the data from the database.

python
Copy code
import streamlit as st
import pymysql

def fetch_data(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buses")
        return cursor.fetchall()

def main():
    st.title('REDBUS Data')
    
    connection = connect_db()
    data = fetch_data(connection)

    for row in data:
        st.write(row)

if __name__ == '__main__':
    main()
7. Running the Application
7.1 Scraping Data
Run the scraping script to gather and store data:
bash
Copy code
python scraper.py
7.2 Launching Streamlit
Start the Streamlit app:
bash
Copy code
streamlit run app.py
8. Conclusion
This documentation provides an overview of the REDBUS data scraping project. It covers the prerequisites, setup, scraping logic, database management, and how to run the application. 



