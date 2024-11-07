
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

As seguintes visualizações ajudam a ilustrar os principais pontos e conclusões da análise:

1. **Gráficos de Distância vs. Aluguel**:
   - Os gráficos de dispersão para **escolas**, **hospitais** e **parques** mostram a relação entre o aluguel e a distância de cada tipo de serviço. Exibidos como `distance_vs_price_hospital.png`, `distance_vs_price_parks.png`, e `distance_vs_price_schools.png`, esses gráficos ajudam a confirmar a fraca correlação observada:
     - ![Distance vs Price - Hospital](outputs/distance_vs_price_hospital.png)
     - ![Distance vs Price - Parks](outputs/distance_vs_price_parks.png)
     - ![Distance vs Price - Schools](outputs/distance_vs_price_schools.png)
   - Cada gráfico mostra uma leve tendência de aumento no aluguel para imóveis próximos a serviços, mas a relação não é forte o suficiente para ser conclusiva.

2. **Mapas de Calor**:
   - **`heatmap_combined_services.png`**: Este mapa de calor agrega todos os serviços (escolas, hospitais e parques) para mostrar áreas de maior concentração de serviços. É útil para observar se há coincidência entre áreas de alta concentração de serviços e áreas de alto aluguel.
     - ![Heatmap Combined Services](outputs/heatmap_combined_services.png)
   - **`heatmap_distance_to_schools_parks.png`**: Este mapa de calor destaca especificamente a proximidade a escolas e parques, com áreas coloridas que indicam onde estão concentrados esses serviços em relação aos imóveis. Isso ajuda a ver se a proximidade a múltiplos serviços afeta os preços de aluguel.
     - ![Heatmap Distance to Schools and Parks](outputs/heatmap_distance_to_schools_parks.png)

3. **Mapa Interativo**: O arquivo HTML `sao_paulo_property_services_distance_map_with_alpha_legend.html` é uma ferramenta dinâmica de exploração visual. Ele inclui camadas interativas que permitem alternar a visualização de serviços específicos e a densidade de preços de aluguel:
   - <a href="outputs/sao_paulo_property_services_distance_map_with_alpha_legend.html" target="_blank">Mapa Interativo de Proximidade e Aluguel</a>
   - **Funcionalidades**:
     - Alternância entre camadas de escolas, hospitais e parques para observar a distribuição de serviços e a proximidade dos imóveis.
     - Mapa de calor de preços de aluguel que permite ao usuário ver áreas de alto e baixo aluguel e sua relação com os serviços.

Essas visualizações combinadas oferecem uma visão completa da distribuição de serviços e preços de aluguel em São Paulo e reforçam as conclusões obtidas na análise estatística.

---

### Principais Resultados

#### 1. Análise de Correlação
   - **Correlação Fraca**: A análise revelou uma relação mínima entre o aluguel e a distância para serviços individuais:
     - Escolas: -0,06
     - Hospitais: -0,05
     - Parques: -0,09
   - Essas correlações negativas sugerem que, em média, imóveis mais próximos desses serviços podem ter preços de aluguel ligeiramente mais altos. No entanto, a fraqueza da correlação indica que a proximidade a esses serviços não é um fator significativo na determinação dos preços de aluguel. Outros fatores, como características específicas do imóvel ou localização em bairros desejados, podem ter mais influência.

#### 2. Coeficiente Composto Proximidade-Aluguel
   - Um coeficiente composto proximidade-aluguel foi calculado para capturar o efeito combinado da proximidade com os três tipos de serviços sobre os preços de aluguel. Com um valor final de **0,08**, esse coeficiente confirma que a influência da proximidade com esses serviços sobre o preço do aluguel é mínima, sugerindo que esses serviços têm pouca relevância prática na definição dos preços.

#### 3. Análise Espacial com Mapas de Calor
   - **Mapas de Calor** revelam a concentração espacial dos serviços em certas regiões de São Paulo. Embora certas áreas exibam uma alta densidade de serviços, não há uma relação visível e significativa entre essas concentrações e os preços de aluguel, o que reforça a conclusão de que a proximidade a serviços não é um fator primário para o custo dos aluguéis.
   - **Distribuição de Aluguéis**: A visualização dos preços em áreas com diferentes densidades de serviços permite observar que altos preços de aluguel estão espalhados em diversas regiões, independentemente da concentração de serviços.

#### 4. Outliers e Observações Adicionais
   - **Outliers Identificados**: Durante a análise, foram identificados imóveis com aluguéis elevados, mesmo quando situados longe dos serviços analisados. Isso indica que o preço do aluguel é potencialmente mais influenciado pelas características do imóvel, como área útil e número de quartos, ou pelo apelo específico de certos bairros.

---

### Conclusão

Esta análise conclui que a proximidade de escolas, hospitais e parques tem um efeito insignificante nos preços de aluguel em São Paulo. Abaixo estão as principais conclusões detalhadas e recomendações para análises futuras:

1. **Impacto Mínimo da Proximidade aos Serviços**: Os resultados mostram coeficientes de correlação fracos para a proximidade de serviços, e o coeficiente composto de proximidade-aluguel de 0,08 indica que esses serviços específicos (escolas, hospitais, e parques) não exercem uma influência significativa nos preços de aluguel. Esse resultado sugere que a proximidade a esses serviços não é um fator essencial na definição dos preços de aluguel para a maioria dos locatários.

2. **Fatores Alternativos Potencialmente Mais Relevantes**:
   A análise indica que fatores além da proximidade aos serviços, como características do bairro e atributos do imóvel, provavelmente desempenham um papel mais importante na determinação do valor do aluguel.
   - **Características do Bairro**: Variáveis como segurança, qualidade do transporte público, e renda média da vizinhança podem ter uma influência maior nos preços dos aluguéis. Bairros com boa infraestrutura e conveniências adicionais tendem a ser mais valorizados.
   - **Especificações do Imóvel**: O tamanho do imóvel, número de quartos, vagas de garagem e estado de conservação do edifício são fatores conhecidos por afetar significativamente o valor do aluguel. É recomendável que estudos futuros incorporem essas variáveis para uma análise mais abrangente.

3. **Recomendações para Análises Futuras**:
   - **Incorporar Análise Multivariada**: Recomenda-se o uso de modelos de regressão multivariada para investigar como diferentes fatores (além da proximidade a serviços) influenciam os preços de aluguel. Isso permitiria controlar as variáveis ao mesmo tempo e identificar quais fatores têm o maior impacto.
   - **Explorar Outros Serviços e Infraestruturas**: Para entender melhor os interesses dos locatários, análises futuras poderiam incluir outras amenidades, como a proximidade de shoppings, transporte público, academias, e áreas de lazer, além de indicadores de qualidade de vida no bairro.
Este estudo fornece insights sobre a insignificância relativa desses serviços na determinação do aluguel, com recomendações para futuras análises que considerem fatores mais amplos ou alternativos.
   - **Mapeamento Interativo para Padrões Espaciais**: O uso de mapas interativos que incluam camadas adicionais, como índices de criminalidade e de acesso a transporte, poderia facilitar uma análise mais rica e personalizada dos padrões de aluguel em São Paulo.

Este estudo fornece uma base para futuras análises de habitação na cidade de São Paulo, sugerindo que, para compreender o mercado de aluguel, é essencial considerar uma gama mais ampla de fatores além da proximidade a escolas, hospitais e parques.

---

### Apêndices e Referências
- **Scripts**: Veja `scripts/` para detalhes sobre o processamento de dados e análise.
- **Saídas**: Visualizações e mapas interativos estão em `outputs/`.
- **Dados**: Dados geográficos originais e conjuntos de dados de aluguel estão localizados no diretório `data/`.

--- 

Este relatório resume as descobertas da Análise de Habitação e Serviços em São Paulo. Para mais detalhes, consulte o código-fonte e as visualizações incluídas no repositório.