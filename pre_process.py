import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# Load your CSV file
input_file_path = 'data/sp_housing_price.csv'  # Path to your input file
df = pd.read_csv(input_file_path)

# Initialize the geolocator with a user agent
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get latitude and longitude
def get_lat_long(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# Apply the function to the address column
df['latitude'], df['longitude'] = zip(*df['address'].apply(get_lat_long))

# Save the updated DataFrame with latitudes and longitudes to a new CSV file
output_file_path = '/data/sp_housing_price_with_lat_long.csv'
df.to_csv(output_file_path, index=False)

print(f"New CSV file with latitudes and longitudes saved at {output_file_path}")
