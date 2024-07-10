# Muji Database Project

Welcome to the Muji Database Project! This project is part of a database class and focuses on building a database for Muji, a Japanese brand known for its high-quality products. The project involves setting up a database with MySQL, connecting it with Python, and working with various Python packages to manage and display data.

## Project Overview

Muji, originally founded in Japan in 1980, offers a wide variety of high-quality products, including household goods, apparel, and food. The name "Muji" is derived from the Japanese term "Mujirushi Ryohin," which translates to "no-brand quality goods." The brand is anchored on three core principles:

1. Selection of materials
2. Streamlining of processes
3. Simplification of packaging

The objective of this project is to create a database that stores information about Muji's products, customers, and sales, allowing efficient data management and insightful analysis.

## Installation

To set up the project, you need to have Python and `pip` installed. Then run this command to install all required packages.

```bash
   pip install -r requirements. txt
```

Alternatively, you can install the following packages by yourself:

1. **mysql-connector-python**: A package used to connect Python with MySQL databases.
   ```bash
   pip install mysql-connector-python
   ```
2. **python-dotenv**: A package to load environment variables from a `.env` file.
   ```bash
   pip install python-dotenv
   ```

## Getting Started

### Clone the repository

To get started, clone the repository:

```bash
git clone https://github.com/utran0612/Muji-Database.git
cd Muji-Database
```

### Set Up the Environment

Create a `.env` file in the project directory and add your MySQL credentials:

```bash
USERNAME = your_mysql_username
PASSWORD = your_mysql_password
```
### Run the program

Run **main.py** to start interacting with the database!

```bash
python main.py
```

## Usage guide

After running the `main.py` program, you are in the main menu with 3 options:

```
1. View performance
2. Restock or Remove inventory
3. Make online purchase
```

Enter your choice (`1`, `2` or `3`) and hit `Enter` to proceed. After choosing an option, you can return to main menu at any time by choosing `q`. After each operation, you can review sub-menu by choosing `#`. Exit program at any time using key combinations `CRTL+C`.

### 1. View performance
You are presented with our 10 questions to explore the database. 

```
1. What is the current inventory of a particular store?
2. What are the top-selling products at a particular store?
3. Which store has the highest total sales revenue?
4. What are the 5 stores with the most sales so far this month?
5. How many customers are currently enrolled in the frequent-shopper program?
6. What is the average order value for online orders compared to in-store purchases?
7. Which products have the highest profit margin across all stores?
8. How does the sales performance of a particular product compare between different store locations?
9. Which store locations have the highest percentage of repeat customers?
10. What are the most popular product combinations purchased together by customers?
```

Enter your choice and hit `Enter` to proceed. Note that some queries require you entering more info. Refer to this table to enter appropiate data.

| Entity   | Smallest ID | Largest ID |
| -------- | ------- | ------- |
| Store    | `S000` | `S010` |
| Product  | `P001` | `P015` |

> Note: `S000` is our online store

### 2. Restock or Remove inventory

Again, you are presented with a sub-menu of inventory operations.

```
1. Restock inventory to the warehouse
2. Restock inventory to a store
3. Remove inventory
4. Shift inventory
```

Enter your choice and hit `Enter` to proceed. 

1. Restock inventory to the warehouse

Enter product details as directed. Note that some fields cannot be left empty: `product_id`, `name`, `quantity` and `cost`. Other fields, if left empty, is saved into database as `NA`.

2. Restock inventory to a store

You are required to enter `product_id` and `store_id`. Refer to Entity-ID table to enter appropiate data.

3. Remove inventory

This operation is equivalent to discontinue a product.

4. Shift inventory

Before this operation, it is a good idea to go back to `main menu -> 1. View performance -> 1st query` to review a specific store inventory. 

This operation requires you to enter `product_id`, `quantity_moved`, `source_store_id` and `target_store_id`. 

### 3. Make online purchase

Sign up if this is your first time interacting with the database. After signing up or logging in, you are presented with the online store, including their IDs, names and price. Choose `s` to keep adding products to cart, or `p` to view total bill and return to main menu.

You made it to the end 🎉 Hopefully this guide is useful!
