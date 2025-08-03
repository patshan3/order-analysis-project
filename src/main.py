import pandas as pd
from datetime import datetime

# -------------------------
# Event-level data (status changes per order)
# -------------------------
events_df = pd.DataFrame([
    {"order_id": 1, "stage": "placed",             "start_time": datetime(
        2024, 7, 1, 10, 0, 0),  "end_time": datetime(2024, 7, 1, 10, 1, 3)},
    {"order_id": 1, "stage": "inventory_checked",  "start_time": datetime(
        2024, 7, 1, 10, 1, 3), "end_time": datetime(2024, 7, 1, 10, 3, 40)},
    {"order_id": 1, "stage": "processing_started", "start_time": datetime(
        2024, 7, 1, 10, 3, 40), "end_time": datetime(2024, 7, 1, 10, 10, 55)},
    {"order_id": 1, "stage": "packed",             "start_time": datetime(
        2024, 7, 1, 10, 10, 55), "end_time": datetime(2024, 7, 1, 10, 22, 1)},
    {"order_id": 1, "stage": "shipped",            "start_time": datetime(
        2024, 7, 1, 10, 22, 1), "end_time": datetime(2024, 7, 1, 10, 48, 1)},

    {"order_id": 2, "stage": "placed",             "start_time": datetime(
        2024, 7, 1, 10, 5, 0),  "end_time": datetime(2024, 7, 1, 10, 6, 0)},
    {"order_id": 2, "stage": "inventory_checked",  "start_time": datetime(
        2024, 7, 1, 10, 6, 0),  "end_time": datetime(2024, 7, 1, 10, 20, 0)},
    {"order_id": 2, "stage": "processing_started", "start_time": datetime(
        2024, 7, 1, 10, 20, 0), "end_time": datetime(2024, 7, 1, 10, 35, 0)},
    {"order_id": 2, "stage": "packed",             "start_time": datetime(
        2024, 7, 1, 10, 35, 0), "end_time": datetime(2024, 7, 1, 11, 0, 0)},
    {"order_id": 2, "stage": "shipped",            "start_time": datetime(
        2024, 7, 1, 11, 0, 0),  "end_time": datetime(2024, 7, 1, 11, 15, 0)},
])

# -------------------------
# Orders summary
# -------------------------
orders_df = pd.DataFrame([
    {"order_id": 1, "customer_id": 101, "product_id": "A1",
        "quantity": 2, "order_date": datetime(2024, 7, 1, 10, 0)},
    {"order_id": 2, "customer_id": 102, "product_id": "B2",
        "quantity": 1, "order_date": datetime(2024, 7, 1, 10, 5)},
    {"order_id": 3, "customer_id": 101, "product_id": "C3",
        "quantity": 5, "order_date": datetime(2024, 7, 2, 9, 15)},
])

# -------------------------
# Customers
# -------------------------
customers_df = pd.DataFrame([
    {"customer_id": 101, "name": "Alice",
        "region": "West", "customer_type": "Business"},
    {"customer_id": 102, "name": "Bob",
        "region": "East", "customer_type": "Individual"},
])

# -------------------------
# Products
# -------------------------
products_df = pd.DataFrame([
    {"product_id": "A1", "name": "Gadget",
        "category": "Electronics", "price": 99.99},
    {"product_id": "B2", "name": "Shoes",
        "category": "Apparel",     "price": 49.95},
    {"product_id": "C3", "name": "Notebook",
        "category": "Stationery",  "price": 5.50},
])

# -------------------------
# Preview all tables
# -------------------------
print("Events:\n", events_df, "\n")
print("Orders:\n", orders_df, "\n")
print("Customers:\n", customers_df, "\n")
print("Products:\n", products_df)
