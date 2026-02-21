# Página explicando os objetivos do projeto e apresentando a equipe

# Importações
import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout da página
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Quem Somos", className="display-4 text-primary fw-bold mb-4"),
            dcc.Markdown('''

A **Bússola da Câmara** é um projeto de extensão acadêmica desenvolvido por estudantes de Jornalismo da Faculdade Cásper Líbero. A iniciativa nasce de um paradoxo da política brasileira atual: embora o Congresso Nacional tenha assumido um protagonismo inédito nos últimos anos, a conexão entre o representante e o representado permanece frágil.

Segundo pesquisa do IPEC divulgada pelo portal Jota em outubro de 2024, [69% dos eleitores não se lembram em quem votaram](https://www.jota.info/opiniao-e-analise/colunas/coluna-daniel-marcelino/voto-passado-69-nao-lembram-escolha-para-deputado-federal-em-2022-aponta-pesquisa) para deputado federal na última eleição. Diante desse cenário, nosso objetivo é oferecer clareza. Acreditamos que a escolha para o Legislativo é tão decisiva quanto a disputa presidencial e que o cidadão merece ferramentas acessíveis para monitorar seus representantes.

Nossa plataforma permite que qualquer pessoa verifique, de forma intuitiva, se um deputado realmente atua de acordo com as ideias que diz defender. Aqui, você pode explorar dados, comparar posicionamentos e fiscalizar bancadas estaduais ou partidárias com total liberdade.

Para garantir a confiabilidade das informações, operamos com transparência absoluta. O site é gratuito e de código aberto. Nossa metodologia e arquitetura técnica podem ser auditadas por qualquer interessado. Basta acessar o código-fonte neste [repositório GitHub](https://github.com/ricardo-grandi-bianco/bussola-da-camara).

Somos uma equipe independente, sem filiação partidária ou vínculo com grupos políticos. Mais do que isso, somos plurais. O grupo é composto por estudantes com visões de mundo distintas, incluindo membros de esquerda, centro e direita unidos pelo rigor jornalístico. Nossa metodologia combina Ciência Política, matemática e análise de dados para entregar um retrato fiel e imparcial do debate legislativo, empoderando o eleitor com informação de qualidade.

### Nossa Equipe

**Coordenação Geral e Desenvolvimento: Ricardo Grandi Bianco** ([LinkedIn](https://www.linkedin.com/in/ricardo-grandi-bianco-897b3a180/))

Idealização do projeto e da metodologia. Responsável pela liderança da equipe, desenvolvimento do código (full stack), extração e análise de dados, elaboração de manuais e supervisão da classificação das votações.

**Design e Identidade Visual: Gabriel de Campos** ([LinkedIn](https://www.linkedin.com/in/gabriel-de-campos-313672214/))

Criação da marca, idealização da identidade visual e da interface do usuário (UI/UX).

**Relações Públicas e Institucionais: Felipe Ockner** ([LinkedIn](https://www.linkedin.com/in/felipe-ockner-352420267/))

Responsável pela divulgação estratégica, pelos relatórios acadêmicos de extensão e pelo relacionamento com stakeholders.

**Social Media e Conteúdo: Evelyn Dantas** ([LinkedIn](https://www.linkedin.com/in/evelyn-dantas-gomes-ferreira?utm_source=share_via&utm_content=profile&utm_medium=member_ios))

Gestão das redes sociais e criação de conteúdo digital para engajamento do público.

**Análise e Classificação Legislativa:**
                         
* **Alexandre Mansano** ([LinkedIn](https://www.linkedin.com/in/alexandre-mansano-b70832273?utm_source=share_via&utm_content=profile&utm_medium=member_android))
* **Lucas Marra** ([LinkedIn](https://www.linkedin.com/in/lucas-saragiotto-marra?utm_source=share_via&utm_content=profile&utm_medium=member_ios))
* **Maria Eduarda Matarazzo** ([LinkedIn](https://www.linkedin.com/in/maria-eduarda-dutra-monteiro-matarazzo-1b8716242?utm_source=share_via&utm_content=profile&utm_medium=member_ios))                     
* **Matheus Sartori** ([LinkedIn](https://www.linkedin.com/in/matheus-dumat-sartori-89985b291/))
* **Raphael Miras** ([LinkedIn](https://www.linkedin.com/in/raphael-miras-264219266/))
* **Thiago Silva** ([LinkedIn](https://www.linkedin.com/in/thiago-emanoel-flor%C3%AAncio-soares-da-silva-6bb265297?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app))
* **Victor Castro** ([LinkedIn](https://www.linkedin.com/in/victorcastro21/))
* **Vinicius Rossi** ([LinkedIn](https://www.linkedin.com/in/vinicius-diniz-rossi?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app))
* **Yan Lima** ([LinkedIn](https://www.linkedin.com/in/yan-augusto-vannucchi-lima-7a245b261?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app))

Responsáveis pela triagem e classificação temática das votações em Plenário, aplicando a metodologia do projeto para garantir a precisão dos eixos ideológicos.               

            ''', className="markdown-texto", link_target="_blank")

        ], width=12, lg=8) 
    ], justify="center") 
], fluid=True, className="py-5 px-4")