
# Análise de Habitação e Serviços em São Paulo

## Índice
1. [Introdução](#introdução)
2. [Preparação dos Dados](#preparação-dos-dados)
3. [Análise e Visualização](#análise-e-visualização)
4. [Principais Resultados](#principais-resultados)
5. [Conclusão](#conclusão)

---

### Introdução
Este projeto explora a relação entre preços de aluguel de imóveis e a proximidade de serviços essenciais em São Paulo, como escolas, hospitais e parques. O principal objetivo é determinar se estar próximo desses serviços afeta os preços de aluguel e visualizar possíveis padrões resultantes.

---

### Preparação dos Dados
O projeto utiliza várias fontes de dados, incluindo informações geográficas sobre serviços e moradia em São Paulo. Aqui está uma visão geral das etapas de preparação:

- **Fontes de Dados**: 
  - Diversos arquivos `.shp` contêm dados espaciais sobre serviços, agrupados em categorias como **educação**, **saúde**, **cultura**, **esportes** e **limites da cidade**.
  - Conjuntos de dados principais sobre propriedades de aluguel incluem informações como latitude, longitude e preço de aluguel.

- **Scripts**: Os seguintes scripts foram desenvolvidos para processar e filtrar os dados:
  - **`pre_process_geoapify.py` e `pre_process_geopy.py`**: Lidam com enriquecimento inicial de dados e mapeamento de coordenadas usando APIs Geoapify e Geopy.
  - **`filter_data.py`**: Filtra os dados das propriedades para incluir apenas informações relevantes dentro dos limites de São Paulo.

- **Dados Finais Preparados**: Após a filtragem, os dados incluem preços de aluguel, localização dos imóveis e distâncias calculadas para as escolas, hospitais e parques mais próximos.

---

### Análise e Visualização

A análise foi realizada com uma combinação de notebooks Jupyter e scripts Python para gerar insights. Visualizações importantes foram salvas no diretório `outputs`.

#### Notebooks e Scripts Principais
- **`initialAnalysis.ipynb`**: Este notebook inclui exploração inicial de dados, resumos estatísticos e visualizações preliminares para entender a distribuição do aluguel e identificar outliers.
- **Scripts de Análise**:
  - **`generate_analisys.py`**: Contém funções principais de análise para correlacionar os preços de aluguel com as métricas de proximidade.
  - **`sao_paulo_property_services_map.py`**: Cria mapas interativos para exibir a localização dos aluguéis e serviços próximos.

#### Visualizações Geradas
1. **Distância vs. Aluguel**: Gráficos do aluguel em função da distância para **escolas**, **hospitais** e **parques**.
   - ![Distance vs Price - Hospital](outputs/distance_vs_price_hospital.png)
   - ![Distance vs Price - Parks](outputs/distance_vs_price_parks.png)
   - ![Distance vs Price - Schools](outputs/distance_vs_price_schools.png)

2. **Mapas de Calor**:
   - `heatmap_combined_services.png` mostra as áreas agregadas de serviços.
     ![Heatmap Combined Services](outputs/heatmap_combined_services.png)
   - `heatmap_distance_to_schools_parks.png` exibe as áreas de proximidade para escolas e parques.
     ![Heatmap Distance to Schools and Parks](outputs/heatmap_distance_to_schools_parks.png)

3. **Mapa Interativo**: O arquivo `sao_paulo_property_services_distance_map_with_alpha_legend.html` fornece uma ferramenta de exploração visual, permitindo que os usuários alternem camadas de serviços e examinem pontos de aluguel.
- <a href="outputs/sao_paulo_property_services_distance_map_with_alpha_legend.html" target="_blank">Mapa Interativo de Proximidade e Aluguel</a>

---

### Principais Resultados

#### 1. Análise de Correlação
   - **Correlação Fraca**: A análise revelou uma relação mínima entre o aluguel e a distância para serviços individuais:
     - Escolas: -0.06
     - Hospitais: -0.05
     - Parques: -0.09
   - As correlações negativas sugerem que imóveis mais próximos desses serviços podem ter aluguéis ligeiramente mais altos, mas a relação é fraca.

#### 2. Coeficiente Composto Proximidade-Aluguel
   - Um **coeficiente composto proximidade-aluguel** foi calculado para resumir a relação geral entre o aluguel e a proximidade aos serviços. Com um valor de **0.08**, esse coeficiente reforça que o efeito da proximidade com os serviços sobre o aluguel é mínimo.

#### 3. Análise Espacial
   - **Mapas de Calor** mostram o agrupamento espacial de serviços, com maior densidade em certas áreas. No entanto, esses clusters não impactam significativamente os padrões de aluguel, indicando que outros fatores podem influenciar os preços dos aluguéis.

#### 4. Observações Adicionais
   - **Outliers**: Vários imóveis com aluguel alto e distantes dos serviços foram identificados, sugerindo que o aluguel é mais influenciado pelas características dos imóveis ou pelo apelo específico do bairro.

---

### Conclusão

Esta análise conclui que a proximidade de escolas, hospitais e parques tem um efeito negligenciável nos preços de aluguel em São Paulo:

1. **Impacto Mínimo**: As correlações fracas e o coeficiente composto sugerem que os locatários não priorizam esses serviços ao decidir sobre aluguéis.
2. **Influência de Outros Fatores**: Análises futuras poderiam examinar influências adicionais sobre o aluguel, como:
   - **Características do bairro**: Segurança, níveis de renda ou acessibilidade.
   - **Especificidades do imóvel**: Tamanho, número de quartos ou idade do edifício.

Este estudo fornece insights sobre a insignificância relativa desses serviços na determinação do aluguel, com recomendações para futuras análises que considerem fatores mais amplos ou alternativos.

---

### Apêndices e Referências
- **Scripts**: Veja `scripts/` para detalhes sobre o processamento de dados e análise.
- **Saídas**: Visualizações e mapas interativos estão em `outputs/`.
- **Dados**: Dados geográficos originais e conjuntos de dados de aluguel estão localizados no diretório `data/`.

--- 

Este relatório resume as descobertas da Análise de Habitação e Serviços em São Paulo. Para mais detalhes, consulte o código-fonte e as visualizações incluídas no repositório.
