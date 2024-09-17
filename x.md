# Project Summary: Food Log App

## Overview
The Food Log App is a web application designed to help users track their daily and weekly nutritional intake. It allows users to add meals, view summaries of their nutritional data, and manage a database of food items. The application is built using Flask, a Python web framework, and integrates with a MySQL database to store and retrieve data.

## Key Features
1. **Meal Entry**: Users can add meals with detailed nutritional information.
2. **Daily and Weekly Summaries**: Users can view summaries of their nutritional intake on a daily and weekly basis.
3. **Nutritional Database**: A comprehensive database of food items that users can filter and sort.
4. **Food Management**: Users can add, edit, delete, and restore food items in the database.
5. **Filters and Sorting**: Users can save and apply filters to the nutritional database and sort the data based on various criteria.
6. **Autocomplete and Nutritional Details**: Provides autocomplete suggestions for food items and detailed nutritional information.

## File Structure
- **app.py**: The main application file containing the Flask routes and database interactions.
- **templates/**: Directory containing HTML templates for rendering the web pages.
- **static/css/**: Directory containing CSS files for styling the web pages.
- **requirements.txt**: File listing the dependencies required to run the application.

## Detailed Description

### app.py
- **Imports**: The file imports necessary libraries including Flask, Pandas, MySQL connector, and others.
- **Database Connection**: Establishes a connection to the MySQL database and initializes a cursor for executing queries.
- **Table Creation**: Contains commented-out code for creating necessary tables in the database.
- **Data Loading**: Loads data from the `nutritional_table` into a Pandas DataFrame for easy manipulation.
- **Routes**:
  - `/`: Renders the home page.
  - `/meal_entry`: Handles meal entry form submissions and saves the data to the database.
  - `/daily_summary`: Displays a summary of daily nutritional intake.
  - `/weekly_summary`: Displays a summary of weekly nutritional intake.
  - `/nutritional_table`: Displays the nutritional database with filtering and sorting options.
  - `/add_food`: Handles the addition of new food items to the database.
  - `/edit_food/<int:index>`: Handles editing of existing food items.
  - `/delete_food/<int:index>`: Deletes a food item from the database.
  - `/restore_food/<int:index>`: Restores a deleted food item.
  - `/get_nutritional_details`: Provides detailed nutritional information for a specific food item.
  - `/autocomplete_food`: Provides autocomplete suggestions for food items.
  - `/get_filter_data`: Retrieves saved filter data.
- **Testing**: Contains a `run_tests` function that tests various routes and functionalities of the application.

### Templates
- **base.html**: The base template that includes the navigation bar and a block for content.
- **index.html**: The home page template welcoming users to the app.
- **meal_entry.html**: The template for the meal entry form.
- **daily_summary.html**: The template for displaying the daily summary of nutritional intake.
- **weekly_summary.html**: The template for displaying the weekly summary of nutritional intake.
- **nutritional_table.html**: The template for displaying the nutritional database with filtering and sorting options.
- **add_food.html**: The template for adding new food items.
- **edit_food.html**: The template for editing existing food items.

### Static Files
- **styles.css**: Contains the CSS styles for the application, including styles for the navigation bar, forms, and tables.

### Requirements
- **requirements.txt**: Lists the dependencies required to run the application, including Flask and Pandas.


## Conclusion
The Food Log App is a comprehensive tool for tracking and managing nutritional intake. It leverages Flask for web development, Pandas for data manipulation, and MySQL for data storage. The application provides a user-friendly interface for adding meals, viewing summaries, and managing a nutritional database. The codebase is well-organized, with clear separation of concerns and extensive use of templates for rendering HTML pages.
