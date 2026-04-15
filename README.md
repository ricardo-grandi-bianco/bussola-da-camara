*Português [disponível abaixo].*
*English version:*

---

# Brazilian House Compass (Bússola da Câmara) - Technical Documentation

The **Brazilian House Compass** is an interactive analytical application that maps the legislative behavior of Brazilian House Representatives onto a two-dimensional ideological Cartesian plane.

This repository hosts the complete data pipeline (ETL), scoring models, unsupervised clustering algorithms, and the source code for the dashboard built with Dash/Plotly.

While the project's Methodology page explains the core concepts, this document deep-dives into the technical architecture, mathematical choices, and statistical justifications.

## Data Pipeline & Architecture (ETL)

The pipeline was designed to be modular, reproducible, and efficient, leveraging a `.parquet` file architecture to ensure high performance when handling high-dimensional voting data. Classification spreadsheets were maintained in `.xlsx` format to facilitate manual labeling via graphical interfaces.

The logical flow is divided into the following stages located in the `etl/` directory:

* **Extraction (`extracao_votacoes.R`)**: An R script consuming the official House of Representatives Open Data API. It retrieves all roll-call votes from a given year, filtering for non-unanimous floor votes.
* **Thematic Classification (`votacoes_classificadas.py`)**: Consolidates bill labeling into axes (Economy or Social Issues) and directions (Left/Right, Progressive/Conservative, Unclassifiable, or Moderate) following manual review.
* **Transformation & Wrangling (`matriz_votacoes.py`)**: A Python script that pivots individual lawmaker votes with classified bill data, creating a **sparse matrix** where rows represent representatives and columns represent specific votes. Invalid votes (abstentions, absences) are treated as `NaN`, "Yes" as 1, and "No/Obstruction" as -1. A 40% minimum participation threshold is strictly enforced.
* **Modeling & Clustering (`scores_e_k-means.py`)**: The analytical core. It applies dissidence-based weighting, calculates final scores, and executes the clustering algorithm on the voting matrix.

## Mathematical Scoring Model (Dissidence-Weighted Score)

A lawmaker’s position on the X-axis (Economy) and Y-axis (Social Issues) is not a simple average of "Yes" or "No" votes. It is derived from a **weighted-by-scarcity (dissidence)** model.

The statistical and political premise is that voting with a large majority requires less ideological conviction than casting a minority vote. Therefore, the absolute weight of a vote on any given bill is inversely proportional to the House's overall adherence to that position.

The base formula applied is:
$$Weight = (1 - w) \times 10$$
*Where **w** is the proportion of votes in a specific direction.*

**Practical Example:** In a vote classified as "Left," if 90% of the quorum votes "Yes" and 10% votes "No":
* A **"Yes" vote (consensus)** receives a light weight: $(1 - 0.90) \times 10 = 1$. The lawmaker moves slightly to the left (-1).
* A **"No" vote (libertarian/right dissent)** receives a heavy weight: $(1 - 0.10) \times 10 = 9$. The lawmaker moves strongly to the right (+9).

### Post-Processing for "Moderate" (M) Bills

For bills classified as Moderate, the algorithm performs a centrality analysis, isolating "Yes" and "No" groups to evaluate their baseline absolute scores. The group with the lowest absolute average is identified as the "center," while the other represents the "poles":
* Votes aligned with the **center** receive a score of 0.
* Votes aligned with the **poles** receive a score proportional to that group's scarcity, with the sign determined by the identified pole (+ for right, - for left).

Finally, scores are normalized using the ratio $10 / max\_absolute$ for each axis, ensuring the visualization symmetrically fills the $[-10, 10]$ Cartesian plane.

## Unsupervised Clustering (K-Means++)

To group representatives based on their voting patterns, the **K-Means** algorithm was applied to the full voting matrix.

Instead of standard random initialization, the `init='k-means++'` parameter was utilized. This technique spreads initial centroids as far apart as possible before iterations begin, dramatically accelerating convergence and preventing the model from getting stuck in suboptimal local optima. A fixed seed was defined to ensure reproducibility.

### The Choice of K=7: A Statistical and Political Trade-off

Defining the optimal number of clusters ($K$) involved rigorous statistical analysis combined with Political Science domain expertise:

* **Inertia (Elbow Method)**: Initial tests showed a clear break at $K=3$. However, politically, dividing the House into only "Left, Center, and Right" is analytically poor and fails to capture the complexity of the brazilian "Centrão" — a group of representatives that do not have a specific or consistent ideological orientation and aim at ensuring proximity to the executive branch in order to guarantee advantages.
* **Silhouette Score**: The coefficient indicated robust mathematical optimization at $K=5$. Yet, qualitative cross-referencing revealed that $K=5$ merged distinct voting profiles into single groups.
* **The Optimal Point (K=7)**: At $K=7$, we observed a positive backlash in the Silhouette Score (improvement over $K=6$) and significantly lower inertia. Qualitatively, $K=7$ provided the best explanatory power, accurately isolating distinct legislative blocs. Models with $K > 7$ showed sharp declines in silhouette and excessive fragmentation without explanatory gain.

## Application Framework (Dash Frontend)

The interactive frontend was built in Python using **Dash**, with components from `dash-bootstrap-components` and `plotly`. To ensure a seamless user experience, strict **camera-state preservation** (Zoom/Pan) logic was implemented, ensuring that dropdown filters do not disrupt the user's free navigation across the Cartesian plane.

## License & Citation

This project is licensed under the MIT License. You are free to use the code and methodology for your own studies or applications.

When using this material or citing its data in academic works, journalistic texts, or other media, please credit the author:

**BibTeX Format:**
```bibtex
@misc{bussolacamara2026,
  author = {Bianco, Ricardo Grandi},
  title = {Brazilian House Compass (Bússola da Câmara): Ideological Mapping of Brazilian Federal Representatives},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{[https://github.com/ricardo-grandi-bianco/bussola-da-camara](https://github.com/ricardo-grandi-bianco/bussola-da-camara)}}
}
```
# Bússola da Câmara - Documentação Técnica

A Bússola da Câmara é uma aplicação analítica interativa que mapeia o comportamento legislativo dos deputados federais brasileiros em um plano cartesiano ideológico bidimensional.

Este repositório contém todo o pipeline de dados (ETL), os modelos de cálculo de scores, o algoritmo de clusterização não supervisionada e o código-fonte do dashboard construído em Dash/Plotly.

A página de Metodologia já explica as principais etapas e raciocínios por trás da construção do projeto, mas este documento detalha a arquitetura técnica, as escolhas matemáticas e as justificativas estatísticas.

## Arquitetura e Pipeline de Dados (ETL)

O pipeline foi desenhado para ser modular, reprodutível e eficiente, utilizando uma arquitetura baseada em arquivos `.parquet` para garantir alta performance durante a manipulação dos dados bidimensionais de votações. Apenas as planilhas de classificação foram mantidas no formato `.xlsx`, pois a interface gráfica de editores de planilha facilita muito essa etapa do trabalho. 

O processo é dividido nas seguintes etapas lógicas presentes na pasta `etl/`:

* **Extração (`extracao_votacoes.R`)**: um script em R consome da API oficial de Dados Abertos da Câmara dos Deputados todas as votações realizadas em um determinado ano e realiza a limpeza para filtrar apenas as de Plenário não unânimes.
* **Classificação Temática (`votacoes_classificadas.py`)**: consolida a rotulação das ementas em eixos (Economia ou Costumes) e direções (Esquerda/Liberal, Progressista/Conservador, Inclassificável ou Moderado), após o trabalho de classificação nos arquivos `.xlsx`.
* **Transformação e Limpeza (`matriz_votacoes.py`)**: script Python responsável por baixar os dados dos votos individuais de cada deputado e pivotá-lo com o dataframe de votações classificadas, criando uma matriz esparsa onde as linhas são deputados e as colunas são as votações. Votos não válidos (abstenções, ausências) são tratados e transformados em `NaN`, votos "Sim" em 1, votos "Não" ou "Obstrução" em -1 e a regra de corte de 40% de participação é aplicada.
* **Modelagem e Agrupamento (`scores_e_k-means.py`)**: coração analítico do projeto. Aplica os pesos por dissidência, calcula os scores finais e roda o algoritmo de clusterização sobre a matriz de votos.

## O Modelo Matemático de Pontuação (Score por Dissidência)

A posição de um deputado nos eixos x (Economia) e y (Costumes/Outros temas) não deriva de uma média simples de "Sim" ou "Não", mas de um modelo de pesos ponderados por escassez (dissidência).

A premissa estatística e política é de que votar acompanhando a grande maioria exige menos convicção ideológica do que proferir um voto minoritário. Portanto, o peso absoluto de um voto em determinada pauta é inversamente proporcional à adesão da Casa àquele posicionamento.

A fórmula base aplicada é:
$$Peso=(1- w)\times10$$, em que $$w$$ é a proporção de votos em determinada direção.

Exemplo prático: em uma votação classificada como "Esquerda", se 90% do quórum vota "Sim" e 10% vota "Não":
* o voto "Sim" (consenso) recebe peso absoluto leve: (1 - 0.90) x 10 = 1. O deputado move-se suavemente para a esquerda (-1);
* o voto "Não" (dissidência liberal) recebe peso forte: (1 - 0.10) x 10 = 9. O deputado move-se fortemente para a direita (+9).

### Pós-processamento de Pautas "Moderadas" (M)

Para pautas classificadas como Moderadas, o algoritmo realiza uma análise de centralidade, isolando os grupos do "Sim" e do "Não" e avaliando o score base prévio (absoluto, em módulo) de cada grupo. O grupo com a menor média absoluta é identificado como o "centro", enquanto o outro é o dos "polos":
* votos alinhados ao "centro" recebem score 0;
* votos alinhados aos "polos" recebem pontuação proporcional à escassez daquele grupo, com sinal determinado de acordo com o polo (+ para a direita e - para a esquerda).

Ao final, os scores são normalizados utilizando a razão 10 / max_absoluto de cada eixo, garantindo que a visualização preencha simetricamente o plano cartesiano [-10, 10].

## Clusterização Não Supervisionada (K-Means++)



Para agrupar os deputados, foi utilizado o algoritmo K-Means, alimentado pela matriz completa de votos.

Em vez da inicialização aleatória padrão, foi utilizado o parâmetro `init='k-means++'`. Essa técnica distribui os centroides iniciais da forma mais espaçada possível antes do início das iterações, acelerando dramaticamente a convergência do algoritmo e evitando que o modelo fique preso em ótimos locais subideais. Além disso, foi definida uma seed para garantir a reprodutibilidade fiel do modelo. 

### A Escolha de K=7: um trade-off matemático e político

A definição do número ideal de clusters (K) foi objeto de rigorosa análise estatística, aliada ao domínio temático da política:

* **Inércia (Elbow Method)**: ao realizar os testes, foi observada a primeira grande "quebra" no cotovelo em K=3. Contudo, politicamente, dividir a Câmara apenas em esquerda, centro e direita é analiticamente pobre, falhando em capturar as dissidências internas e a complexidade de outros grupos, como o chamado centrão;
* **Silhouette Score**: o coeficiente apontou uma otimização matemática robusta em K=5. Porém, ao tabular qualitativamente esse resultado, notou-se que ele englobava perfis de votação distintos no mesmo grupo;
* **O Ponto Ótimo (K=7)**: ao testar K=7, foi observado um "backlash" positivo no Silhouette Score (uma melhora em relação a K=6) e uma inércia significativamente mais baixa. Qualitativamente, K=7 apresentou o melhor poder explicativo, isolando com precisão grupos distintos e capturando nuances importantes. Já modelos com K>7 apresentavam quedas acentuadas na silhueta e pulverização excessiva sem ganho explicativo.

## Estrutura da Aplicação (Frontend em Dash)

O frontend interativo foi construído em Python utilizando Dash, com componentes do `dash-bootstrap-components` e `plotly`. Para garantir a melhor experiência de usuário, foram implementadas lógicas estritas de preservação de estado da câmera (Zoom/Pan), garantindo que filtros de dropdown não afetem a livre navegação do usuário pelos pontos do plano cartesiano.

## Licença e Citação

Este projeto está sob a licença MIT. Sinta-se livre para utilizar o código e a metodologia em seus estudos ou aplicações.

Ao utilizar este material ou citar seus dados em trabalhos acadêmicos, textos jornalísticos ou quaisquer outros materiais, atribua os créditos ao autor:

**Formato BibTeX:**
```bibtex
@misc{bussolacamara2026,
  author = {Bianco, Ricardo Grandi},
  title = {Brazilian House Compass (Bússola da Câmara): Ideological Mapping of Brazilian Federal Representatives},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{[https://github.com/ricardo-grandi-bianco/bussola-da-camara](https://github.com/ricardo-grandi-bianco/bussola-da-camara)}}
}
```
