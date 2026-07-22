import numpy as np
import pandas as pd 
from datetime import datetime
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "PASSWORD",
    database = "retail_sales"
)
cursor = conn.cursor()

def view_customers():
    df = pd.read_sql("SELECT * FROM customers", conn)
    print(df) 
view_customers()

def view_product():
    df = pd.read_sql("SELECT * FROM products", conn)
    print(df)
view_product()

def view_orders():
    df = pd.read_sql("SELECT * FROM orders", conn)
    print(df)
view_orders()

def view_region():
    df = pd.read_sql("SELECT * FROM regions", conn)
    print(df)
view_region()

def check_duplicates():
    Tables = ["customers", "products", "orders", "regions"]
    
    for table in Tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        duplicates_count = df.duplicated().sum()
        
        print(f"Tables : {table}")
        print(f"Duplicates : {duplicates_count}")
check_duplicates()

def null_values():
    Tables = ["customers", "products", "orders", "regions"]
    for table in Tables:
         df = pd.read_sql(f"SELECT * FROM {table}", conn)
         
         null_values = df.isnull().sum().sum()
         
         print(f"null_value : {table}")
         print(f"null_values : {null_values}")
null_values()
         
def negative_sales():
    df = pd.read_sql("SELECT * FROM orders", conn)
    negative_sales = df[df["sales"] < 0]
    print("negative_sales:", len(negative_sales))
    
    if not negative_sales.empty:
        print(negative_sales)
negative_sales()

def blank_column():
    Tables = ["customers", "products", "orders", "regions"]
    
    for table in Tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        blank_column = df.isnull().sum().sum()
        
        print("table:", (table))
        print("blank_column:", (blank_column))
blank_column()

def invalid_ages():
    query = "SELECT * FROM customers WHERE age < 0 OR age > 30"
    
    df = pd.read_sql(query, conn)
    print("invalid_age: ", len(df))
    
    if not df.empty:
        print(df)
    else:
        "age not found"
invalid_ages()

def selling_price():
    query = "SELECT * FROM products WHERE selling_price < cost_price"
    df = pd.read_sql(query, conn)
    print("product sold below cost price:", len(df))
    
    if not df.empty:
        print(df)
    else:
        print("only profit")
selling_price()

def order_date():
    df = pd.read_sql("SELECT * FROM orders", conn)
    df["order_date"] = pd.to_datetime(df["order_date"])
    today = pd.Timestamp.today().normalize()
    future = df[df["order_date"] < today]
    print(len(future))
order_date()

def total_sales():
    df = pd.read_sql("SELECT * FROM orders", conn)
    total_sale = df["sales"].sum()
    print("total_sales: ", total_sale)
total_sales()

def total_profit():
    df = pd.read_sql("SELECT * FROM orders", conn)
    total_profit = df["profit"].sum()
    print("total_profit: ", total_profit)
total_profit()

def total_loss():
    df = pd.read_sql("SELECT * FROM products", conn)
    loss = df[df["selling_price"] < df["cost_price"]]
    total_loss = (loss["cost_price"] - loss["selling_price"]).sum()
    print("total_loss: ", total_loss)
total_loss()

def total_order():
    df = pd.read_sql("SELECT * FROM orders", conn)
    total_order = df["order_id"].count()
    print(total_order)
total_order()

def average_sales():
    df = pd.read_sql("SELECT * FROM orders", conn)
    average_sales = df["sales"].mean()
    print(average_sales)
average_sales()

def region_wise_sales():
    query = """
    SELECT o.order_id,  
    r.region_name, 
    r.manager,
    o.sales
    FROM orders o
    INNER JOIN regions r 
    ON o.region = r.region_name
    """
    df = pd.read_sql(query, conn)
    region_wise = df.groupby("region_name")["sales"].sum()
    print(region_wise)
region_wise_sales()
    
def product_wise_sales():
    query = """
    SELECT p.product_id,
    p.product_name,
    o.sales
    FROM products p
    INNER JOIN orders o 
    ON p.product_id = o.product_id 
    """
    df = pd.read_sql(query, conn)
    product_wise = df.groupby("product_name")["sales"].sum()
    print(product_wise)
product_wise_sales()
    
def customer_wise_sale():
    query = """
    SELECT c.customer_id,
    c.customer_name,
    o.sales
    FROM customers c
    INNER JOIN orders o
    ON o.customer_id = c.customer_id
    """
    df = pd.read_sql(query, conn)
    customer_wise = df.groupby("customer_name", as_index=False)["sales"].sum()
    print(customer_wise)
    
    top_customer = customer_wise.loc[customer_wise["sales"].idxmax()]
    print(top_customer["customer_name"], top_customer["sales"])
customer_wise_sale()

def category_wise_sales():
    query = """
    SELECT p.product_id,
    p.category,
    o.sales
    FROM products p 
    INNER JOIN orders o
    ON p.product_id = o.product_id
    """
    df = pd.read_sql(query, conn)
    category_wise = df.groupby("category")["sales"].sum()
    print(category_wise)
category_wise_sales()

def monthly_sales():
    query = """
    SELECT order_date, sales FROM orders
    """
    df = pd.read_sql(query, conn)
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    df["month"] = df["order_date"].dt.strftime("%b")
    
    monthly = df.groupby("month")["sales"].sum()
    
    print(monthly)
monthly_sales()
    
def monthly_profit():
    query = "SELECT order_date, profit FROM orders"
    
    df = pd.read_sql(query, conn)
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    
    df["month"] = df["order_date"].dt.strftime("%b")
    
    monthly = df.groupby("month")["profit"].sum()
    print(monthly)
monthly_profit()
    
def top_product():
    query = """
    SELECT p.product_id,
    p.product_name,
    o.sales
    FROM products p
    INNER JOIN orders o
    ON p.product_id = o.product_id
    """
    df = pd.read_sql(query, conn)
    high_sales = df.groupby("product_name")["sales"].max().sort_values(ascending=False).head(10)
    print(high_sales)
top_product()

def lowest_sales():
    query = """
    SELECT p.product_id,
    p.product_name,
    o.sales
    FROM products p
    INNER JOIN orders o
    ON p.product_id = o.product_id
    """
    df = pd.read_sql(query, conn)
    lowest_sales = df.groupby("product_name")["sales"].min().sort_values().head(10)
    print(lowest_sales)
lowest_sales()

def top_customer():
    query = """
    SELECT c.customer_id,
    c.customer_name,
    o.sales
    FROM customers c
    INNER JOIN orders o
    ON c.customer_id = o.customer_id
    """
    df = pd.read_sql(query, conn)
    
    top_customer = df.groupby("customer_name")["sales"].max().sort_values(ascending=False).head()
    print(top_customer)
top_customer()
    
def export_csv_file():
    Tables = ["customers", "products", "orders", "regions"]
    
    for table in Tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        df.to_csv(f"{table}.csv", index=False)
        print(f"{table}.csv exported")
export_csv_file()
