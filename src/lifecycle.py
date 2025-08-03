"""
order_lifecycle.py

Defines the OrderLifecycle class, which provides methods for analyzing
stage-level durations and transitions for a single order.
"""

import pandas as pd

class OrderLifecycle:
    """
    Represents the state transitions of a single order.
    Provides methods to analyze timing between stage changes.
    """

    def __init__(self, order_id, events_df):
        # Step 1: store the order_id
        # Step 2: filter events_df to rows matching this order_id
        # Step 3: sort those rows by timestamp
        # Step 4: store the result as self.events

        self.order_id = order_id
        self.sorted_events_df = (
            # Filter for the selected id
            events_df[events_df['order_id'] == self.order_id]
            .sort_values('timestamp')  # Sort rows by timestamp
        )

    def total_duration(self):
        """ Calculates the time between when a given order is placed and when it is shipped"""

        # Since the dataframe is filtered for our order_id and sorted we only need the first
        # and last rows of the orders dataframe to calculate the time delta
        start_time = self.sorted_events_df['start_time'].iloc[0]
        end_time = self.sorted_events_df['end_time'].iloc[-1]

        # Return the time difference
        return end_time - start_time

    def time_between(self, stage1: str, stage2: str) -> pd.Timedelta:
        """Calculate the time difference between any two states for a given order"""

        # Creates a valid list of stage strings
        valid = list(self.sorted_events_df['stage'].unique())

        if stage1 not in valid or stage2 not in valid:
            raise ValueError(
                f"Both stages must be one of {valid}. "
                f"Got '{stage1}' and '{stage2}'."
            )

        start_time = self.sorted_events_df[self.sorted_events_df['stage']
                                           == stage1]['start_time'].iloc[0]

        end_time = self.sorted_events_df[self.sorted_events_df['stage']
                                         == stage2]['end_time'].iloc[0]

        return end_time - start_time

    def stage_duration(self, stage: str) -> pd.Timedelta:
        """Calculates the time a given in order was in a given stage"""

        # Creates a valid list of stage strings
        valid = list(self.sorted_events_df['stage'].unique())

        # Determines if the supplied stage is valid
        if stage not in valid:
            raise ValueError(
                f"Stages must be one of {valid}."
            )
        start_time = self.sorted_events_df[self.sorted_events_df['stage']
                                           == stage]['start_time'].iloc[0]
        end_time = self.sorted_events_df[self.sorted_events_df['stage']
                                         == stage]['end_time'].iloc[-1]

        return end_time - start_time

    def stage_prcnt(self, stage: str) -> float:
        """Returns the percent of total time an order was in a given stage"""
        # Creates a valid list of stage strings
        valid = list(self.sorted_events_df['stage'].unique())

        # Determines if the supplied stage is valid
        if stage not in valid:
            raise ValueError(
                f"Stages must be one of {valid}."
            )

        stage_time = self.stage_duration(stage)

        total_time = self.total_duration()

        return round((stage_time / total_time) * 100, 2)
