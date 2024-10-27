import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load your CSV file
input_file_path = 'data/sp_housing_price_with_lat_long.csv'  # Path to your input file
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
    geolocator = Nominatim(user_agent="geoapiExercises")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=3)  # Delay between requests to avoid being blocked
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

# Sequentially geocode addresses
def sequential_geocode(addresses, output_file_path='data/sp_housing_price_with_lat_long.csv'):
    total_addresses = len(addresses)
    remaining_addresses = total_addresses
    print("Starting sequential geocoding...")
    for i, address in enumerate(addresses):
        if pd.notna(df.loc[i, 'latitude']) and pd.notna(df.loc[i, 'longitude']):
            print(f"Skipping address {i} as it already has latitude and longitude.")
            remaining_addresses -= 1
            continue
        try:
            lat, long = get_lat_long(address)
            df.loc[i, 'latitude'] = lat
            df.loc[i, 'longitude'] = long
            
            remaining_addresses -= 1  # Update the remaining count
            print(f"Remaining addresses: {remaining_addresses}")

            # Save progress to CSV after every 10 addresses (adjust the interval as needed)
            if i % 10 == 0:
                print(f"Saving progress at address index {i}...")
                save_partial_results(df, output_file_path)
                
        except Exception as e:
            print(f"Error processing address at index {i} ({address}): {e}")

# Replace 'address' with your actual address column name, appending district, São Paulo, Brazil
print("Preparing addresses for geocoding...")
try:
    addresses = [f"{address}, {district}, São Paulo, Brazil" for address, district in zip(df['address'], df['district'])]
    print(f"Prepared {len(addresses)} addresses for geocoding.")
except KeyError as e:
    print(f"Error preparing addresses: {e}")
    exit(1)

# Initialize latitude and longitude columns with None if they don't exist
print("Initializing latitude and longitude columns...")
if 'latitude' not in df.columns:
    df['latitude'] = None
if 'longitude' not in df.columns:
    df['longitude'] = None

# Start geocoding sequentially
start_time = time.time()
print("Starting geocoding process...")
try:
    sequential_geocode(addresses)
except Exception as e:
    print(f"Error during geocoding process: {e}")
end_time = time.time()

# Save the final DataFrame with latitudes and longitudes to a new CSV file
output_file_path = 'data/sp_housing_price_with_lat_long_2.csv'
print("Saving final results...")
save_partial_results(df, output_file_path)

print(f"Geocoding completed in {end_time - start_time:.2f} seconds.")
print(f"Final CSV file with latitudes and longitudes saved at {output_file_path}")