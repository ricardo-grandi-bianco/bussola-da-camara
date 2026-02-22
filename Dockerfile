# 1. IMAGEM BASE
# Puxa uma versão oficial, minimalista e segura do Linux já com o Python 3.12 instalado.
# O sufixo 'slim' garante que ferramentas desnecessárias do sistema operacional fiquem de fora, mantendo o contêiner leve.
FROM python:3.12-slim

# 2. DIRETÓRIO DE TRABALHO
# Cria uma pasta chamada /app dentro do Linux do contêiner e define que todos os próximos comandos acontecerão lá dentro.
WORKDIR /app

# 3. CACHE DE DEPENDÊNCIAS (Boas práticas)
# Copia APENAS o requirements.txt primeiro. 
# Isso é um truque do Docker: se o código do seu app mudar, mas as bibliotecas não, 
# ele não precisa baixar o Pandas e o Plotly tudo de novo, economizando tempo no build.
COPY requirements.txt .

# 4. INSTALAÇÃO DE PACOTES
# Instala as bibliotecas listadas. O parâmetro '--no-cache-dir' diz ao pip para não guardar 
# os arquivos de instalação temporários, deixando o contêiner ainda menor.
RUN pip install --no-cache-dir -r requirements.txt

# 5. CÓPIA DO CÓDIGO FONTE
# Agora sim, copia todo o resto do seu projeto (respeitando o .dockerignore) para dentro do contêiner.
COPY . .

# 6. EXPOSIÇÃO DE PORTAS
# O Google Cloud Run injeta automaticamente uma variável chamada PORT no contêiner (geralmente a 8080).
# Essas linhas preparam o contêiner para escutar o tráfego que chegará por ela.
ENV PORT 8080
EXPOSE $PORT

# 7. COMANDO DE INICIALIZAÇÃO
# É o gatilho final. Usa o Gunicorn (servidor web robusto) para rodar o app.
# --workers 1: Define 1 processo principal (ideal para o limite de memória do Cloud Run gratuito).
# --threads 8: Permite que esse processo atenda até 8 requisições simultâneas.
# --timeout 0: Desativa o timeout interno do Gunicorn, deixando que o próprio Cloud Run gerencie isso.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.app.app:server