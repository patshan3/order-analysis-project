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
        merged = pd.merge(self.orders_df, self.products_df,
                          how='left', on='product_id')
        merged["line_total"] = merged["quantity"] * merged["price"]
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


class CustomerGroup:
    """
CustomerGroup

Represents a collection of customers and provides tools to analyze group-level behavior.

This class enables:
- Aggregation of customer spending and ordering patterns
- Identification of top and high-value customers
- Comparison of behavior across customer segments (e.g., region)
- Group-level metrics such as average spend, repeat order rates, etc.

Can be used to support customer segmentation, cohort analysis, and strategic insights.
"""


def __init__(self, customers_df: pd.DataFrame, orders_df: pd.DataFrame,
             events_df: pd.DataFrame, products_df: pd.DataFrame):
    self.customers_df = customers_df
    self.orders_df = orders_df
    self.events_df = events_df
    self.products_df = products_df
    self.merged = pd.merge(orders_df, products_df,
                           on="product_id", how="left")
    self.merged["line_total"] = self.merged["quantity"] * \
        self.merged["price"]

    self._customer_cache = {}


def _filter_by_date(self, df: pd.DataFrame, start_date=None, end_date=None) -> pd.DataFrame:
    """Filters a given DataFrame by optional start and end date using the 'order_date' column."""
    if start_date:
        df = df[df["order_date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["order_date"] <= pd.to_datetime(end_date)]
    return df


def cust_in_region(self, region: str) -> pd.DataFrame:
    """Returns a DataFrame of customers in a given region"""
    if region not in self.customers_df["region"].unique():
        raise ValueError(f"Region '{region}' not found in customer data.")

    # Filter customers by region
    # Returns a DataFrame of customers in the specified region
    return self.customers_df[self.customers_df["region"] == region]


def top_customers(
    self,
    n: int = 10,
    region: str = None,
    start_date=None,
    end_date=None
) -> pd.DataFrame:
    """
    Returns a DataFrame of the top n customers by total spend.
    Can be filtered by region and/or date.
    """
    # Select the base customers DataFrame
    if region is not None:
        customers_df = self.cust_in_region(region)
        merged = self.merged[self.merged["customer_id"].isin(
            customers_df["customer_id"])]
    else:
        customers_df = self.customers_df
        merged = self.merged

    # Filter by date range if provided
    merged = self._filter_by_date(
        merged, start_date=start_date, end_date=end_date)

    # Group by customer_id and sum their line totals
    top_customers_df = (
        merged.groupby("customer_id")["line_total"]
        .sum()
        .reset_index()
        .sort_values(by="line_total", ascending=False)
        .head(n)
    )

    # Merge with customer details
    return pd.merge(top_customers_df, customers_df, on="customer_id")


def top_products(
    self,
    n: int = 10,
    region: str = None,
    start_date=None,
    end_date=None
) -> pd.DataFrame:

    # Filter by region if provided
    if region is not None:
        products_df = self.cust_in_region(region)
        merged = self.merged[self.merged["product_id"].isin(
            products_df["product_id"])]
    else:
        products_df = self.products_df
        merged = self.merged

    # Filter by date range if provided
    merged = self._filter_by_date(
        merged, start_date=start_date, end_date=end_date)

    # Group by product_id and sum their line totals
    top_products_df = (
        merged.groupby("product_id")["line_total"]
        .sum()
        .reset_index()
        .sort_values(by="line_total", ascending=False)
        .head(n)
    )
    # Merge with customer details
    return pd.merge(top_products_df, products_df, on="product_id")


def avg_customer_spend(
    self,
        region: str = None,
        start_date=None,
        end_date=None) -> float:
    """Returns the average spend per customer"""

    # Start with merged orders dataframe
    orders = self.merged

    # Region filter
    if region is not None:
        customers_df = self.cust_in_region(region)
        orders = orders[orders["customer_id"].isin(
            customers_df["customer_id"])]

    orders = self._filter_by_date(
        orders, start_date=start_date, end_date=end_date)

    # Aggregate total spend per customer then calculate average
    customer_totals = orders.groupby("customer_id")["line_total"].sum().mean()

    return round(customer_totals, 2) if not pd.isna(customer_totals) else 0.0


def avg_order_value(self, start_date=None, end_date=None) -> float:
    """Returns the average order value across all customers, optionally within a date range.

    Args:
        start_date (str or pd.Timestamp, optional): Filter orders from this date forward.
        end_date (str or pd.Timestamp, optional): Filter orders up to this date.
    """
    df = self.merged.copy()

    # Filter by date if provided
    if start_date:
        df = df[df["order_date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["order_date"] <= pd.to_datetime(end_date)]

    # Calculate order-level totals
    order_totals = df.groupby("order_id")["line_total"].sum()

    # Return average across all orders
    return round(order_totals.mean(), 2) if not order_totals.empty else 0.0
