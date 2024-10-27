import pandas as pd
import geopandas as gpd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the housing price CSV
housing_data = pd.read_csv('data/sp_housing_price.csv')

# Preview the data
print(housing_data.head())

# Create a geolocator object
geolocator = Nominatim(user_agent="real_estate_project")

# Rate limit to avoid overloading the geocoding service
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Apply geocoding to each address in the housing data
housing_data['location'] = housing_data['address'].apply(geocode)

# Extract latitude and longitude into separate columns
housing_data['latitude'] = housing_data['location'].apply(lambda loc: loc.latitude if loc else None)
housing_data['longitude'] = housing_data['location'].apply(lambda loc: loc.longitude if loc else None)

# Create a GeoDataFrame from the housing data
housing_gdf = gpd.GeoDataFrame(housing_data, geometry=gpd.points_from_xy(housing_data['longitude'], housing_data['latitude']))

""" 
# Load shapefiles for different types of education facilities
education_ceu_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_CEU.shp')
education_technical_public_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_ENSINO_TECNICO_PUBLICO.shp')
education_other_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_OUTROS.shp')
education_private_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_REDE_PRIVADA.shp')
education_public_fundamental_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_REDE_PUBLICA_ENSINO_FUNDAMENTAL_MEDIO.shp')
education_senai_sesi_senac_gdf = gpd.read_file('data/education/SIRGAS_SHP_TEMA_EDUCACAO_SENAI_SESI_SENAC.shp')

# Load cultural facilities data
culture_gdf = gpd.read_file('data/culture/SIRGAS_SHP_TEMA_CULTURA.shp')

# Load health facilities data
health_ambulatory_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_AMBULATORIOS_ESPECIALIZADOS.shp')
health_hospital_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_HOSPITAL.shp')
health_other_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_OUTROS_ESTABELECIMENTOS_E_SERVICOS_ESPECIALIZADOS.shp')
health_mental_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_SAUDE_MENTAL.shp')
health_ubs_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_UBS_POSTO_DE_SAUDE_CENTRO_DE_SAUDE.shp')
health_dst_aids_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_UNIDADES_DST_AIDS.shp')
health_emergency_gdf = gpd.read_file('data/health/SIRGAS_SHP_TEMA_SAUDE_URGENCIA_EMERGENCIA.shp')

# Load sports facilities data
sports_central_gdf = gpd.read_file('data/sports/SIRGAS_SHP_TEMA_ESPORTE_CENTRO ESPORTIVO.shp')
sports_club_gdf = gpd.read_file('data/sports/SIRGAS_SHP_TEMA_ESPORTE_CLUBE_DA_COMUNIDADE.shp')
sports_club_community_gdf = gpd.read_file('data/sports/SIRGAS_SHP_TEMA_ESPORTE_CLUBE.shp')
sports_stadium_gdf = gpd.read_file('data/sports/SIRGAS_SHP_TEMA_ESPORTE_ESTADIO.shp')
sports_other_gdf = gpd.read_file('data/sports/SIRGAS_SHP_TEMA_ESPORTE_OUTROS.shp')

print(education_ceu_gdf.crs)
 """
