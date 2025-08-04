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


    def _merged_orders(self) -> pd.DataFrame:
        """Returns a merged DataFrame of this customer's orders and product info, with line totals."""
        merged = pd.merge(self.orders_df, self.products_df, how='left', on='product_id')
        merged["total"] = merged["quantity"] * merged["price"]
        return merged

    def order_total(self, order_id=None) -> float:
        """Returns the total order value of a given order or a cusomters total orders if
        no order_id is provided"""

        # Order quantity * product price
        merged = self._merged_orders()
        if order_id is None:
            return round(merged["total"].sum(), 2)
        return round(merged[merged["order_id"] == order_id]["total"].sum(), 2)

    def avg_order_value(self) -> float:
        """Returns the average order value for a given customer"""

        # Merge the product and order dataframes
        merged = self._merged_orders()
        order_totals = merged.groupby("order_id")["total"].sum()
        # average the order totals
        avg = order_totals.mean()

        return round(avg, 2)

    def max_order(self) -> float:
        """Returns the max order for a given customer"""
        # Merge the product and order dataframes
        merged = self._merged_orders()
        # Calculate the max order
        max_order = merged.groupby("order_id")["total"].sum(
        ).sort_values(ascending=False).iloc[0]

        return max_order

    def min_order(self) -> float:
        """Returns the max order for a given customer"""
        # Merge the product and order dataframes
        merged = self._merged_orders()
        # Calculate the min order
        min_order = merged.groupby("order_id")["total"].sum(
        ).sort_values(ascending=False).iloc[-1]

        return min_order

    def most_freq(self) -> pd.DataFrame:
        """Returns a datafram of the 10 most frequently ordered products"""
        freq_df = self.orders_df["quantity"].groupby(
            "product_id").sum().sort_values(ascending=False).head(10)

        return freq_df

