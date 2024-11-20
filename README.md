# House Price Analysis

This project aims to scrape, clean, and analyze real estate data to understand property trends, including price, number of bedrooms, bathrooms, and property locations. The primary focus is on analyzing the data collected from Zoopla and visualizing key insights using Tableau.

## Project Overview

The project involves scraping housing data from Zoopla, cleaning and preparing the data for analysis, and performing exploratory data analysis to identify trends and patterns in the housing market.

## Workflow

1. **Data Scraping**:  
   Data is collected from Zoopla using the Playwright library to extract property details such as price, address, number of bedrooms, bathrooms, and tenure type.

2. **Data Cleaning**:  
   The scraped data is cleaned using pandas to remove duplicates, format columns, and extract useful features like postal codes. This ensures the data is structured and ready for analysis.

3. **Data Analysis**:  
   Key insights such as the average price by postal code, property distribution by number of bedrooms, and price ranges are calculated. This analysis provides a clear understanding of the housing market trends.

4. **Visualization**:  
   Tableau is used to create visualizations, including scatter plots and bar charts, to display trends and distributions in the dataset effectively.

## Key Features

- Scrapes property details like price, address, and features (e.g., bedrooms, bathrooms) from Zoopla.
- Cleans and preprocesses the data for analysis.
- Provides insights into housing market trends.
- Visualizes data using Tableau for better understanding and presentation.

## Requirements

- Python 3.x
- Required Libraries:
  - `pandas` for data cleaning and analysis
  - `playwright` for web scraping
  - `json` for handling scraped data
  - Tableau for visualization

## Install the required dependencies:
bash
pip install -r requirements.txt
playwright install

## Usage
Run the Scraper:
Use the scraper script to collect data from Zoopla. This script navigates through property listings and saves the results to a JSON file.

python clean.py
Visualize the Data:
Load the cleaned data into Tableau to create visualizations like scatter plots, bar charts, and dashboards.

## Results
The analysis highlights trends in the housing market, such as:

## Average prices by postal code.
Distribution of properties based on the number of bedrooms and bathrooms.
Insights into the types of properties available in different areas.
## Future Work
Enhance the scraper to include additional features such as property types or square footage.
Implement advanced machine learning models to predict property prices based on features.
Automate the Tableau visualization process for real-time updates.
## Acknowledgments
Special thanks to the Playwright and pandas libraries for enabling web scraping and data cleaning, and Tableau for visualization.
