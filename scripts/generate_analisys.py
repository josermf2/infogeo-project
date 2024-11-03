import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the housing data
housing_data = pd.read_csv('data/final_housing_analysis.csv')

# Scatter plot: Distance to Schools vs. Real Estate Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=housing_data, x='distance_to_schools', y='total')
plt.title('Distance to Schools vs Real Estate Price')
plt.xlabel('Distance to Nearest School (meters)')
plt.ylabel('Real Estate Price')
plt.savefig('distance_vs_price_schools.png')
plt.close()

# Scatter plot: Distance to Parks vs. Real Estate Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=housing_data, x='distance_to_parks', y='total')
plt.title('Distance to Parks vs Real Estate Price')
plt.xlabel('Distance to Nearest Park (meters)')
plt.ylabel('Real Estate Price')
plt.savefig('distance_vs_price_parks.png')
plt.close()

# Scatter plot: Distance to Hospitals vs. Real Estate Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=housing_data, x='distance_to_hospitals', y='total')
plt.title('Distance to Hospitals vs Real Estate Price')
plt.xlabel('Distance to Nearest Hospital (meters)')
plt.ylabel('Real Estate Price')
plt.savefig('distance_vs_price_hospital.png')
plt.close()

# Combined scatter plot: Distance to Services vs. Real Estate Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=housing_data, x='distance_to_schools', y='total', label='Schools')
sns.scatterplot(data=housing_data, x='distance_to_parks', y='total', label='Parks')
sns.scatterplot(data=housing_data, x='distance_to_hospitals', y='total', label='Hospitals')
plt.title('Distance to Services vs Real Estate Price')
plt.xlabel('Distance to Nearest Service (meters)')
plt.ylabel('Real Estate Price')
plt.savefig('distance_vs_price_services.png')
plt.close()

bins = [0, 3000, 8000, 12000, float('inf')] 
labels = ['0-3km', '3-8km', '8-12km', '12+km']

# Ensure the columns exist by reapplying binning for each service
housing_data['schools_distance_bin'] = pd.cut(housing_data['distance_to_schools'], bins=bins, labels=labels)
housing_data['parks_distance_bin'] = pd.cut(housing_data['distance_to_parks'], bins=bins, labels=labels)
housing_data['hospitals_distance_bin'] = pd.cut(housing_data['distance_to_hospitals'], bins=bins, labels=labels)

# Calculate the average distance to any service (combined average for schools, parks, hospitals)
housing_data['avg_distance_to_services'] = housing_data[['distance_to_schools', 'distance_to_parks', 'distance_to_hospitals']].mean(axis=1)

# Add a binned column for the combined distance to services
housing_data['services_distance_bin'] = pd.cut(housing_data['avg_distance_to_services'], bins=bins, labels=labels)

# Calculate the average property price per bin for combined distance to services
avg_price_services = housing_data.groupby('services_distance_bin', observed=False)['total'].mean()

# Plot average prices for each unified distance bin
plt.figure(figsize=(10, 6))
avg_price_services.plot(kind='bar', color='steelblue')
plt.title("Average Property Price by Combined Distance to Services")
plt.xlabel("Distance to Services (bins)")
plt.ylabel("Average Property Price")
plt.xticks(rotation=45)
plt.savefig('avg_price_by_combined_distance_bins.png')
plt.close()

# Heatmap of average property price by distance bins
# Creating pivot table with services binned data (using schools and parks as primary dimensions)
heatmap_data = housing_data.pivot_table(index='schools_distance_bin', columns='parks_distance_bin', values='total', aggfunc='mean')

plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".0f")
plt.title("Average Property Price by Distance to Schools and Parks")
plt.xlabel("Distance to Parks")
plt.ylabel("Distance to Schools")
plt.savefig('heatmap_combined_services.png')
plt.close()