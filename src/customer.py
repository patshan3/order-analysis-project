"""
customer.py

Defines the Customer class, which represents a single customer
and provides methods to analyze their order patterns, behaviors,
and overall contribution to the business.
"""

import pandas as pd


class Customer:
    """
 Represents an individual customer and their associated orders.

 This class provides analysis tools for:
 - Counting total and completed orders
 - Calculating average order value and fulfillment time
 - Identifying order delays or drop-offs
 - Aggregating order history from order and event data

 Attributes:
     customer_id (int | str): The unique ID of the customer
     orders_df (pd.DataFrame): Filtered DataFrame of this customer's orders
     events_df (pd.DataFrame): Filtered event history for this customer's orders
 """

    def __init__(self, customer_id: int | str, orders_df: pd.DataFrame,
                 events_df: pd.DataFrame, products_df: pd.DataFrame):

        self.customer_id = customer_id
        self.orders_df = orders_df[orders_df['customer_id'] == customer_id]
        self.order_ids = self.orders_df["order_id"].unique()
        self.events_df = events_df[events_df["order_id"].isin(self.order_ids)]
        self.products_df = products_df

    def order_count(self) -> int:
        """Returns the count of all unique orders that a customer has placed"""
        count = len(self.order_ids)
        return count

    def order_total(self, order_id=None) -> float:
        """Returns the total order value of a given order or a cusomters total orders if
        no order_id is provided"""

        # Order quantity * product price
        # Merge the product and order dataframes
        merged = pd.merge(self.orders_df, self.products_df,
                          how='left', on='product_id')
        # Calculate the product totals
        merged["total"] = merged["quantity"]*merged["price"]

        if order_id is None:
            total = merged["total"].sum()
        else:
            total = merged[merged["order_id"] == order_id]["total"].sum()
        return total

    def avg_order(self) -> float:
        """Returns the average order value for a given customer"""

        # Merge the product and order dataframes
        merged = pd.merge(self.orders_df, self.products_df,
                          how='left', on='product_id')
        # Calculate the product totals
        merged["total"] = merged["quantity"]*merged["price"]
        # Calculate the order totals
        order_totals = merged.groupby("order_id")["total"].sum()
        # average the order totals
        avg = order_totals.mean()

        return round(avg, 2)
