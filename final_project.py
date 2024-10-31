import pandas as pd
import geopandas as gpd
from geopy.distance import geodesic
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load housing data from filtered addresses
housing_data = pd.read_csv('data/filtered_addresses_sao_paulo.csv')

# Function to load .shp files, set an initial CRS, and reproject to WGS84
def load_service_shapefiles(folder_path, initial_crs="EPSG:31983"):
    service_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.shp')]
    dataframes = []
    for file in service_files:
        gdf = gpd.read_file(file)
        if gdf.crs is None:
            gdf.set_crs(initial_crs, inplace=True)
        gdf = gdf.to_crs("EPSG:4326")
        dataframes.append(gdf)
    return pd.concat(dataframes, ignore_index=True) if dataframes else None

# Load public services data from subdirectories
schools_gdf = load_service_shapefiles('data/education')
hospitals_gdf = load_service_shapefiles('data/health')
parks_gdf = load_service_shapefiles('data/culture')

# Define function to calculate nearest distance to public services in batches
def calculate_nearest_distances_in_batches(housing, services, service_type, batch_size=100):
    batch_results = []  # List to store each batch's result

    for i in range(0, len(housing), batch_size):
        batch = housing.iloc[i:i + batch_size].copy()
        distances = []
        for _, row in batch.iterrows():
            house_location = (row['latitude'], row['longitude'])
            nearest_distance = min(
                geodesic(house_location, (service.geometry.y, service.geometry.x)).meters
                for service in services.itertuples()
            )
            distances.append(nearest_distance)

        batch[f'distance_to_{service_type}'] = distances
        batch.to_csv(f'data/intermediate_{service_type}_batch_{i}.csv', index=False)  # Save each batch
        batch_results.append(batch)  # Store for final concatenation

    return pd.concat(batch_results)  # Combine all batches

# Apply distance calculations in batches for each type of public service
housing_data = calculate_nearest_distances_in_batches(housing_data, schools_gdf, 'schools')
housing_data = calculate_nearest_distances_in_batches(housing_data, hospitals_gdf, 'hospitals')
housing_data = calculate_nearest_distances_in_batches(housing_data, parks_gdf, 'parks')

# Save final dataset
housing_data.to_csv('data/final_housing_analysis.csv', index=False)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=housing_data, x='distance_to_schools', y='total')
plt.title('Distance to Schools vs Real Estate Price')
plt.xlabel('Distance to Nearest School (meters)')
plt.ylabel('Real Estate Price')
plt.savefig('distance_vs_price_schools.png')
