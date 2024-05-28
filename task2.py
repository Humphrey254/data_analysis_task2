import pandas as pd
import numpy as np

data = pd.read_csv('QVI_data.csv')
data.head(5)# Convert transaction_date to datetime
data['transaction_date'] = pd.to_datetime(data['DATE'])
# Add a new month ID column in the format yyyymm
data['month_ID'] = data['transaction_date'].dt.strftime('%Y-%m')

data['month_ID']
grouped_data = data.groupby(['STORE_NBR', 'month_ID'])
# Calculate measures
measures = grouped_data.agg({
    'LYLTY_CARD_NBR': 'count',  # Count of transactions
    'TOT_SALES': 'sum',          # Total sales
    'PROD_QTY': 'sum',           # Total quantity sold
    'PACK_SIZE': 'mean'          # Average pack size
})

# Rename columns for clarity
measures.columns = ['Transaction Count', 'Total Sales', 'Total Quantity Sold', 'Average Pack Size']

# Optionally, calculate additional measures
measures['Average Sales per Transaction'] = measures['Total Sales'] / measures['Transaction Count']

# Reset index to flatten the multi-index
measures.reset_index(inplace=True)

# Print the resulting measures
measures
# Define the pre-trial period (example: from start date until 2019-01-01)
pre_trial_end_date = pd.to_datetime('2019-01')

# Filter data to the pre-trial period
pre_trial_data = data[data['month_ID'] < pre_trial_end_date.strftime('%Y-%m')]

# Group by STORE_NBR and count the number of months each store has data for in the pre-trial period
store_observation_periods = pre_trial_data.groupby('STORE_NBR')['DATE'].agg('nunique')

# Find stores with full observation periods (i.e., data for all months in the pre-trial period)
stores_with_full_observation = store_observation_periods[store_observation_periods == store_observation_periods.max()].index

# Filter data to stores with full observation periods
pre_trial_full_data = pre_trial_data[pre_trial_data['STORE_NBR'].isin(stores_with_full_observation)]

# Print the filtered data
pre_trial_full_data
# Define trial period (example: from 2019-02-01 to 2019-04-01)
trial_start_date = pd.to_datetime('2019-02-01')
trial_end_date = pd.to_datetime('2019-04-01')

# Convert the 'DATE' column to a Timestamp datatype
data['DATE'] = pd.to_datetime(data['DATE'])

# Filter data to the trial period
trial_data = data[(data['DATE'] >= trial_start_date) & (data['DATE'] < trial_end_date)]

# Count the number of unique customers in the trial period
trial_customers = trial_data['LYLTY_CARD_NBR'].nunique()

# Define pre-trial period (example: from start date until 2019-01-01)
pre_trial_end_date = pd.to_datetime('2019-01-01')

# Filter data to the pre-trial period
pre_trial_data = data[data['DATE'] < pre_trial_end_date]

# Count the number of unique customers in the pre-trial period
pre_trial_customers = pre_trial_data['LYLTY_CARD_NBR'].nunique()

# Calculate scaling factor for customer counts
scaling_factor = trial_customers / pre_trial_customers

print("Scaling Factor for Customer Counts:", scaling_factor)
# Identify control stores
control_stores = [77, 86,233]

# Apply scaling factor to control store customer counts
for store in control_stores:
    # Filter data for the control store
    control_store_data = data[data['STORE_NBR'] == store]

    # Count the number of unique customers for the control store
    control_store_customers = control_store_data['LYLTY_CARD_NBR'].nunique()

    # Adjust the customer count using the scaling factor
    adjusted_customers = int(control_store_customers * scaling_factor)

    print(f"Store {store}: Adjusted Customers = {adjusted_customers}")
