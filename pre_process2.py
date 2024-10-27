import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Load your CSV file
input_file_path = 'data/sp_housing_price.csv'  # Path to your input file
df = pd.read_csv(input_file_path)

print(f"Loaded {len(df)} addresses from {input_file_path}")

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)  # Delay between requests to avoid being blocked

# Function to get latitude and longitude
def get_lat_long(address):
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
    df.to_csv(output_file_path, index=False)
    print(f"Partial results saved to {output_file_path}")

# Parallelize geocoding with ThreadPoolExecutor
def parallel_geocode(addresses, max_workers=10, output_file_path='data/sp_housing_price_with_lat_long.csv'):
    total_addresses = len(addresses)
    remaining_addresses = total_addresses
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_address = {executor.submit(get_lat_long, address): i for i, address in enumerate(addresses)}
        for future in as_completed(future_to_address):
            i = future_to_address[future]
            address = addresses[i]
            try:
                lat, long = future.result()
                df.loc[i, 'latitude'] = lat
                df.loc[i, 'longitude'] = long
                
                remaining_addresses -= 1  # Update the remaining count
                print(f"Remaining addresses: {remaining_addresses}")

                # Save progress to CSV after every 100 addresses (adjust the interval as needed)
                if i % 10 == 0:
                    save_partial_results(df, output_file_path)
                    
            except Exception as e:
                print(f"Error processing {address}: {e}")

# Replace 'address' with your actual address column name
addresses = df['address'].tolist()

# Initialize latitude and longitude columns with None
df['latitude'] = None
df['longitude'] = None

# Start geocoding in parallel
start_time = time.time()
print("Starting geocoding process...")
parallel_geocode(addresses, max_workers=10)
end_time = time.time()

# Save the final DataFrame with latitudes and longitudes to a new CSV file
output_file_path = 'data/sp_housing_price_with_lat_long.csv'
save_partial_results(df, output_file_path)

print(f"Geocoding completed in {end_time - start_time:.2f} seconds.")
print(f"Final CSV file with latitudes and longitudes saved at {output_file_path}")
