import pandas as pd
import requests
import time

# Geoapify API Key
apiKey = "feeaa35b140345698b2be71e5d646ea8"  # Replace with your actual Geoapify API Key

# File paths
failed_addresses_file = 'data/without_lat_long.csv'  # File containing addresses that failed with geopy
geoapify_results_file = 'geocoded_failed_addresses.csv'
input_file_path = 'data/sp_housing_price_with_lat_long.csv'
output_file_path = 'data/sp_housing_price_with_lat_long_complete.csv'

# Parameters for batch geocoding
timeout = 1  # seconds between checks for job completion
maxAttempt = 10  # Maximum attempts to get Geoapify results

# Geoapify batch geocoding function
def getLocations(locations):
    url = f"https://api.geoapify.com/v1/batch/geocode/search?apiKey={apiKey}"
    response = requests.post(url, json=locations)
    result = response.json()

    if response.status_code != 202:
        print("Failed to create a job. Check if the input data is correct.")
        return None

    jobId = result['id']
    getResultsUrl = f"{url}&id={jobId}"
    time.sleep(timeout)
    
    return getLocationJobs(getResultsUrl, 0)

def getLocationJobs(url, attemptCount):
    response = requests.get(url)
    result = response.json()

    if response.status_code == 200:
        return result
    elif attemptCount >= maxAttempt:
        return None
    elif response.status_code == 202:
        print("Job pending...")
        time.sleep(timeout)
        return getLocationJobs(url, attemptCount + 1)

# Load failed addresses
failed_df = pd.read_csv(failed_addresses_file)
data = [{"id": str(i), "text": address} for i, address in enumerate(failed_df["address"])]

# Batch geocode with Geoapify
results = getLocations(data)

# Save results if successful
if results and "features" in results:
    geocoded_data = [
        {
            "address": failed_df["address"][int(feature["properties"]["id"])],
            "latitude": feature["properties"].get("lat"),
            "longitude": feature["properties"].get("lon")
        }
        for feature in results["features"]
    ]
    geocoded_failed_df = pd.DataFrame(geocoded_data)
    geocoded_failed_df.to_csv(geoapify_results_file, index=False)
    print(f"Saved Geoapify geocoding results to {geoapify_results_file}")
else:
    print("No results received from Geoapify.")

# Load original and Geoapify results, then merge
df = pd.read_csv(input_file_path)
geoapify_results = pd.read_csv(geoapify_results_file)

df = df.merge(geoapify_results, on="address", how="left", suffixes=("", "_geoapify"))
df["latitude"].fillna(df["latitude_geoapify"], inplace=True)
df["longitude"].fillna(df["longitude_geoapify"], inplace=True)
df.drop(columns=["latitude_geoapify", "longitude_geoapify"], inplace=True)

# Save final result
df.to_csv(output_file_path, index=False)
print(f"Saved final dataset with complete geocoding to {output_file_path}")
