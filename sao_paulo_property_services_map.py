import folium
import pandas as pd
from folium.plugins import HeatMap

# Carregar os dados de habitação com as distâncias já calculadas
housing_data = pd.read_csv('data/final_housing_analysis.csv')

# Inicializar o mapa centrado em São Paulo
m = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)

# Etapa 1: Adicionar o mapa de calor de preços de propriedades com base nos valores de aluguel
heat_data = [[row['latitude'], row['longitude'], row['rent']] for index, row in housing_data.iterrows()]
HeatMap(heat_data, radius=15, max_zoom=13).add_to(m)

# Etapa 2: Adicionar camadas de distância transparentes e não selecionadas para cada tipo de serviço
def add_distance_layer(data, distance_column, map_object, color, layer_name, opacity=0.3):
    layer = folium.FeatureGroup(name=layer_name, show=False)  # 'show=False' deixa a camada não selecionada por padrão
    for _, row in data.iterrows():
        # Criar informações de popup e tooltip
        popup_info = f"{layer_name} Distância: {row[distance_column]:.2f} metros"
        tooltip_info = f"Aluguel: R${row['rent']:.2f}\nDistância: {row[distance_column]:.2f} metros"
        
        # Criar um marcador circular com transparência
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=opacity,  # Aplicar transparência
            popup=popup_info,  # Popup clicável
            tooltip=tooltip_info  # Tooltip ao passar o mouse
        ).add_to(layer)
    layer.add_to(map_object)

# Adicionar camadas de distância com transparência para escolas, hospitais e parques
add_distance_layer(housing_data, 'distance_to_schools', m, 'blue', 'Distância para Escolas')
add_distance_layer(housing_data, 'distance_to_hospitals', m, 'red', 'Distância para Hospitais')
add_distance_layer(housing_data, 'distance_to_parks', m, 'green', 'Distância para Parques')

# Etapa 3: Adicionar controle de camadas para alternar cada camada de distância
folium.LayerControl().add_to(m)

# Etapa 4: Adicionar uma legenda estática para a escala de cores do mapa de calor
legend_html = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 150px; 
     background-color: white; z-index:1000; font-size:14px;
     border:2px solid grey; padding: 10px;">
     <b>Legenda de Preço de Aluguel</b><br>
     <i style="background: blue; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Baixo<br>
     <i style="background: lightblue; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Médio-Baixo<br>
     <i style="background: orange; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Médio-Alto<br>
     <i style="background: red; width: 10px; height: 10px; float: left; margin-right: 5px;"></i> Alto<br>
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Salvar o mapa como um arquivo HTML
m.save("sao_paulo_property_services_distance_map_with_alpha_legend.html")
print("Mapa interativo com camadas de distância não selecionadas, transparência e legenda estática criado e salvo como 'sao_paulo_property_services_distance_map_with_alpha_legend.html'")
