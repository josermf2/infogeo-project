import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load your CSV file
input_file_path = 'data/sp_housing_price_with_lat_long2.csv'
print(f"Loading CSV file from {input_file_path}...")
try:
    df = pd.read_csv(input_file_path)
    print(f"Loaded {len(df)} addresses from {input_file_path}")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit(1)

# Initialize the geolocator
print("Initializing geolocator...")
try:
    geolocator = Nominatim(user_agent="YourUniqueAppName")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    print("Geolocator initialized.")
except Exception as e:
    print(f"Error initializing geolocator: {e}")
    exit(1)

# Function to get latitude and longitude
def get_lat_long(address):
    if not address or pd.isna(address):
        print(f"Invalid address: {address}")
        return None, None
    print(f"Geocoding address: {address}")
    try:
        location = geocode(address, timeout=10)
        if location:
            print(f"Geocoded: {address} => (Lat: {location.latitude}, Long: {location.longitude})")
            return location.latitude, location.longitude
        else:
            print(f"Failed to geocode: {address}")
            return None, None
    except Exception as e:
        print(f"Error for {address}: {e}")
        return None, None

# Function to periodically save the dataframe to CSV
def save_partial_results(df, output_file_path):
    print(f"Saving partial results to {output_file_path}...")
    try:
        df.to_csv(output_file_path, index=False)
        print(f"Partial results saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving partial results: {e}")

# Batch geocode function
def batch_geocode(addresses, batch_size=10, output_file_path='data/sp_housing_price_with_lat_long2.csv'):
    total_addresses = len(addresses)
    remaining_addresses = total_addresses
    print("Starting batched geocoding...")
    
    # Iterate in batches
    for start_idx in range(0, total_addresses, batch_size):
        end_idx = min(start_idx + batch_size, total_addresses)
        print(f"Processing batch: {start_idx} to {end_idx-1}")
        
        for i in range(start_idx, end_idx):
            if pd.notna(df.loc[i, 'latitude']) and pd.notna(df.loc[i, 'longitude']):
                print(f"Skipping address {i} as it already has latitude and longitude.")
                remaining_addresses -= 1
                continue
            
            try:
                lat, long = get_lat_long(addresses[i])
                df.loc[i, 'latitude'] = lat
                df.loc[i, 'longitude'] = long
                remaining_addresses -= 1
                print(f"Remaining addresses: {remaining_addresses}")
            except Exception as e:
                print(f"Error processing address at index {i} ({addresses[i]}): {e}")
        
        # Save progress after each batch
        save_partial_results(df, output_file_path)
        print(f"Batch {start_idx}-{end_idx-1} processed. Pausing before next batch...")
        
        # Delay between batches to prevent rate-limiting issues
        time.sleep(15)  # Adjust the sleep time as needed

# Prepare addresses for geocoding
print("Preparing addresses for geocoding...")
try:
    addresses = [f"{address}, {district}, São Paulo, Brazil" for address, district in zip(df['address'], df['district'])]
    print(f"Prepared {len(addresses)} addresses for geocoding.")
except KeyError as e:
    print(f"Error preparing addresses: {e}")
    exit(1)

# Initialize latitude and longitude columns if they don't exist
print("Initializing latitude and longitude columns...")
if 'latitude' not in df.columns:
    df['latitude'] = None
if 'longitude' not in df.columns:
    df['longitude'] = None

# Start batch geocoding
start_time = time.time()
print("Starting geocoding process...")
try:
    batch_geocode(addresses, batch_size=10)
except Exception as e:
    print(f"Error during geocoding process: {e}")
end_time = time.time()

# Save the final DataFrame with latitudes and longitudes to a new CSV file
output_file_path = 'data/sp_housing_price_with_lat_long_3.csv'
print("Saving final results...")
save_partial_results(df, output_file_path)

print(f"Geocoding completed in {end_time - start_time:.2f} seconds.")
print(f"Final CSV file with latitudes and longitudes saved at {output_file_path}")
