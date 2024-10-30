import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load your dataset (ensure latitude and longitude columns are named appropriately)
df = pd.read_csv('data/sp_housing_price_completed.csv')

# Define São Paulo city bounding box coordinates (approximate)
SP_LAT_MIN, SP_LAT_MAX = -24.00, -23.36
SP_LON_MIN, SP_LON_MAX = -46.84, -46.36

# Filter addresses within São Paulo bounding box
df = df[(df['latitude'] >= SP_LAT_MIN) & (df['latitude'] <= SP_LAT_MAX) &
           (df['longitude'] >= SP_LON_MIN) & (df['longitude'] <= SP_LON_MAX)]

# Convert latitude and longitude to a GeoDataFrame
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf_addresses = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Load São Paulo city boundaries shapefile
# Replace 'sao_paulo_shapefile.shp' with the path to your shapefile
gdf_sp = gpd.read_file('data/sao_paulo_boundaries/35MEE250GC_SIR.shp')

# Ensure both datasets use the same coordinate reference system (CRS)
gdf_sp = gdf_sp.to_crs(gdf_addresses.crs)

# Filter to keep only the "Metropolitana de São Paulo" region
# Replace 'region_column_name' with the actual column name that identifies the region
gdf_sp = gdf_sp[gdf_sp['NM_MESO'] == 'METROPOLITANA DE SÃO PAULO']

# Perform a spatial join to keep only points within São Paulo boundaries
gdf_addresses_sp = gpd.sjoin(gdf_addresses, gdf_sp, predicate='within')

# Drop the extra spatial join columns if needed
gdf_addresses_sp = gdf_addresses_sp.drop(columns=['index_right'])

# Save the filtered data
gdf_addresses_sp.to_csv('data/filtered_addresses_sao_paulo.csv', index=False)
