# Data Analytics Activity

## Project Overview
This project performs basic data analysis on stock market data using Python and the Pandas library. It loads a CSV file containing historical stock price data and displays key information about the dataset.

## Requirements
- Python 3.x
- pandas library

## Installation

### Install Dependencies
```bash
pip install pandas
```

## Usage

### Running the Project
```bash
python main.py
```

## Project Structure
```
Data_Analytics_Activity/
├── main.py                          # Main script for data analysis
├── README.md                        # This file
└── Week-8 (4) (1)/
    ├── data.csv                     # Stock price dataset
    ├── test.csv                     # Test data
    └── PRSA2017_Data_20130301-20170228/
        └── PRSA_Data_20130301-20170228/  # Air quality data files
            ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
            ├── PRSA_Data_Changping_20130301-20170228.csv
            ├── PRSA_Data_Dingling_20130301-20170228.csv
            ├── PRSA_Data_Dongsi_20130301-20170228.csv
            ├── PRSA_Data_Guanyuan_20130301-20170228.csv
            ├── PRSA_Data_Gucheng_20130301-20170228.csv
            ├── PRSA_Data_Huairou_20130301-20170228.csv
            ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
            ├── PRSA_Data_Shunyi_20130301-20170228.csv
            ├── PRSA_Data_Tiantan_20130301-20170228.csv
            ├── PRSA_Data_Wanliu_20130301-20170228.csv
            └── PRSA_Data_Wanshouxigong_20130301-20170228.csv
```

## Code Description

### main.py
The main script performs the following operations:

1. **Import Libraries**: Imports pandas for data manipulation
2. **Load Data**: Reads the CSV file from `Week-8 (4) (1)/data.csv`
3. **Display First Rows**: Shows the first 5 rows of the dataset using `df.head()`
4. **Display Data Types**: Shows the data type of each column using `df.dtypes`

### Sample Output
```
         Date        Open        High  ...       Close   Adj Close    Volume
0  2018-07-02  183.820007  187.300003  ...  187.179993  182.199005  17731300
1  2018-07-03  187.789993  187.949997  ...  183.919998  179.025772  13954800
2  2018-07-05  185.259995  186.410004  ...  185.399994  180.466370  16604200
3  2018-07-06  185.419998  188.429993  ...  187.970001  182.967972  17485200
4  2018-07-09  189.500000  190.679993  ...  190.580002  185.508545  19756600

Date          object
Open         float64
High         float64
Low          float64
Close        float64
Adj Close    float64
Volume         int64
dtype: object
```

## Data Information

The data consists of stock price information with the following columns:
- **Date**: Trading date
- **Open**: Opening price
- **High**: Highest price of the day
- **Low**: Lowest price of the day
- **Close**: Closing price
- **Adj Close**: Adjusted closing price
- **Volume**: Trading volume

## Author
Student Assignment - Data Analytics Activity

## Date
April 2026
