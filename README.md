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
$$Peso=(1-Propor\text{\c{c}}\tilde{a}o\_do\_Voto)\times10$$

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
  title = {Bússola da Câmara: Mapeamento Ideológico dos Deputados Federais},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{[https://github.com/ricardo-grandi-bianco/bussola-da-camara](https://github.com/ricardo-grandi-bianco/bussola-da-camara)}}
}