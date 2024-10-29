import pandas as pd

# Load the dataset
file_path = 'data\sp_housing_price_with_lat_long.csv'
df = pd.read_csv(file_path)

# Separate rows with and without latitude and longitude
df_with_lat_long = df.dropna(subset=['latitude', 'longitude'])
df_without_lat_long = df[df[['latitude', 'longitude']].isnull().any(axis=1)]

# Save the separated datasets to new files (optional)
df_with_lat_long.to_csv('data/with_lat_long.csv', index=False)
df_without_lat_long.to_csv('data/without_lat_long.csv', index=False)

print("Datasets separated successfully!")