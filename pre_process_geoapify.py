import pandas as pd
import requests
import time
import math

# Geoapify API Key
apiKey = "feeaa35b140345698b2be71e5d646ea8"  # Replace with your actual Geoapify API Key

# File paths
failed_addresses_file = 'data/without_lat_long.csv'  # File containing addresses that failed with geopy
geoapify_results_file = 'data/geocoded_failed_addresses.csv'
input_file_path = 'data/sp_housing_price_with_lat_long.csv'
output_file_path = 'data/sp_housing_price_with_lat_long_complete.csv'

# Function to geocode address sequentially using Geoapify
def geocode_address(address):
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["features"]:
            location = data["features"][0]["properties"]
            print(f"Geocoded: {address} => (Lat: {location['lat']}, Lon: {location['lon']})")
            return location["lat"], location["lon"]
        else:
            print(f"Address not found: {address}")
            return None, None
    else:
        print(f"Error geocoding address {address}: {response.status_code}")
        return None, None

# Load failed addresses
failed_df = pd.read_csv(failed_addresses_file)
geocoded_data = []

# Geocode each address sequentially
for address in failed_df["address"]:
    lat, lon = geocode_address(address)
    geocoded_data.append({"address": address, "latitude": lat, "longitude": lon})
    time.sleep(1)  # Delay to respect rate limits

# Save geocoded data to file
geocoded_failed_df = pd.DataFrame(geocoded_data)
geocoded_failed_df.to_csv(geoapify_results_file, index=False)
print(f"Geoapify geocoding results saved to {geoapify_results_file}")

# Load original and Geoapify results, then merge
df = pd.read_csv(input_file_path)
geoapify_results = pd.read_csv(geoapify_results_file)

df = df.merge(geoapify_results, on="address", how="left", suffixes=("", "_geoapify"))
df["latitude"].fillna(df["latitude_geoapify"], inplace=True)
df["longitude"].fillna(df["longitude_geoapify"], inplace=True)
df.drop(columns=["latitude_geoapify", "longitude_geoapify"], inplace=True)

# Save final result
df.to_csv(output_file_path, index=False)
print(f"Final dataset with complete geocoding saved to {output_file_path}")
