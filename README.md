🐍 Pokémon API — Projeto Final EBAC

API REST desenvolvida em Python com FastAPI como projeto final do curso de Backend da EBAC.

A aplicação utiliza a PokéAPI como fonte de dados e disponibiliza endpoints para consultar e listar Pokémon. Para melhorar o desempenho das consultas individuais, os dados são armazenados temporariamente em Redis.

O projeto também utiliza Docker, Docker Compose e Poetry, além de possuir testes automatizados.

🚀 Tecnologias

Python 3.14

FastAPI

Pydantic

Requests

Redis

Poetry

Pytest

Docker

Docker Compose

PokéAPI

📋 Funcionalidades

A API disponibiliza as seguintes funcionalidades:

Verificação do funcionamento da API.

Listagem de Pokémon.

Paginação da lista de Pokémon.

Consulta de um Pokémon específico através do ID.

Retorno de informações como nome, ID, altura, peso, tipos e sprites.

Cache das consultas individuais utilizando Redis.

Expiração automática do cache após 5 minutos.

Tratamento de Pokémon inexistentes.

Documentação interativa através do Swagger.

Documentação através do ReDoc.

Testes automatizados.

📦 Pré-requisitos

Para executar o projeto utilizando Docker, é necessário ter instalado:

Docker

Docker Compose

Não é necessário instalar Python, Redis ou Poetry na máquina quando a aplicação for executada através do Docker.

🔽 Clonando o projeto

Clone o repositório:

git clone https://github.com/iuriolv/projeto-final-ebac-backend.git


Entre no diretório do projeto:

cd projeto-final-ebac-backend

🐳 Executando o projeto com Docker

A forma recomendada de executar a aplicação é utilizando o Docker Compose.

Execute:

docker compose up --build


Esse comando irá:

Construir a imagem da API.

Instalar as dependências do projeto.

Criar o container da aplicação.

Criar o container do Redis.

Configurar a comunicação entre a API e o Redis.

Iniciar o servidor FastAPI.

Após a inicialização, a API estará disponível em:

http://localhost:8000

Executando em segundo plano

Caso não queira manter o terminal ocupado:

docker compose up --build -d

Verificando os containers

Para verificar os containers em execução:

docker compose ps


Você deverá encontrar os serviços:

pokemon-api
pokemon-redis

Visualizando os logs

Para visualizar os logs da aplicação:

docker compose logs api


Para acompanhar os logs em tempo real:

docker compose logs -f api

Parando a aplicação

Para parar e remover os containers:

docker compose down

📚 Utilizando a API

Depois de iniciar o projeto, existem duas formas principais de utilizar a API:

Através dos endpoints diretamente.

Através da documentação interativa do FastAPI.

📖 Swagger

O FastAPI disponibiliza uma interface gráfica para testar os endpoints.

Acesse no navegador:

http://localhost:8000/docs


Na interface do Swagger é possível:

Visualizar todos os endpoints.

Informar parâmetros.

Executar requisições.

Visualizar as respostas.

Ver os códigos HTTP retornados pela API.

Essa é a forma mais simples de testar a aplicação.

📘 ReDoc

Também é possível acessar a documentação através do ReDoc:

http://localhost:8000/redoc

🔗 Endpoints disponíveis
GET /

Verifica se a aplicação está funcionando.

Requisição
GET http://localhost:8000/

Resposta
{
  "Hello": "World"
}

GET /pokemons

Retorna uma lista de Pokémon.

O endpoint possui paginação através dos parâmetros page e limit.

Parâmetros
Parâmetro	Tipo	Padrão	Descrição
page	integer	1	Número da página
limit	integer	20	Quantidade de Pokémon por página
Exemplo

Para buscar os primeiros 20 Pokémon:

GET http://localhost:8000/pokemons


Ou:

GET http://localhost:8000/pokemons?page=1&limit=20


Para buscar 10 Pokémon da segunda página:

GET http://localhost:8000/pokemons?page=2&limit=10

Exemplo de resposta
{
  "pagina": 1,
  "total": 1302,
  "limite": 20,
  "offset": 0,
  "next": "https://pokeapi.co/api/v2/pokemon?offset=20&limit=20",
  "previous": null,
  "Pokemons": [
    {
      "name": "bulbasaur",
      "url": "https://pokeapi.co/api/v2/pokemon/1/"
    },
    {
      "name": "ivysaur",
      "url": "https://pokeapi.co/api/v2/pokemon/2/"
    }
  ]
}


O offset é calculado automaticamente pela aplicação através da página e do limite informado:

offset = (page - 1) * limit

GET /pokemons/{id}

Retorna informações detalhadas de um Pokémon através do seu ID.

Exemplo

Para consultar o Pikachu:

GET http://localhost:8000/pokemons/25

Resposta
{
  "name": "pikachu",
  "id": 25,
  "height": 4,
  "weight": 60,
  "types": [
    "electric"
  ],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png"
  }
}


As informações retornadas são:

name — nome do Pokémon.

id — identificador do Pokémon.

height — altura.

weight — peso.

types — tipos do Pokémon.

sprites.front_default — imagem frontal.

sprites.back_default — imagem traseira.

Pokémon inexistente

Caso seja informado um ID que não exista na PokéAPI:

GET http://localhost:8000/pokemons/999999


A aplicação retorna:

{
  "detail": "Pokemon não encontrado"
}


com status HTTP:

404 Not Found

⚡ Cache com Redis

O endpoint de consulta individual utiliza Redis para armazenar os dados dos Pokémon.

Quando um Pokémon é consultado, a aplicação primeiro verifica se ele já está armazenado no cache.

O funcionamento é:

              GET /pokemons/25
                      │
                      ▼
               ┌─────────────┐
               │    Redis    │
               │ Existe no   │
               │   cache?    │
               └──────┬──────┘
                      │
             ┌────────┴────────┐
             │                 │
            SIM               NÃO
             │                 │
             ▼                 ▼
       Retorna cache      Consulta PokéAPI
                               │
                               ▼
                         Salva no Redis
                               │
                               ▼
                         Retorna dados


O cache possui duração de 300 segundos (5 minutos).

Isso significa que, após consultar um Pokémon, novas consultas ao mesmo Pokémon dentro dos próximos 5 minutos podem utilizar os dados armazenados no Redis em vez de realizar uma nova chamada à PokéAPI.

🌐 PokéAPI

A aplicação utiliza a PokéAPI
 como fonte externa dos dados.

A listagem utiliza:

https://pokeapi.co/api/v2/pokemon


A consulta individual utiliza:

https://pokeapi.co/api/v2/pokemon/{id}


A aplicação recebe os dados da PokéAPI e transforma a resposta antes de disponibilizá-la ao usuário.

🧪 Executando os testes

O projeto possui testes automatizados utilizando Pytest.

Caso as dependências estejam instaladas através do Poetry:

poetry run pytest


Para visualizar mais detalhes durante a execução:

poetry run pytest -v


Para executar os testes dentro do ambiente virtual:

pytest

💻 Executando sem Docker

Também é possível executar o projeto diretamente através do Python e Poetry.

1. Instale o Poetry

Instale o Poetry de acordo com seu sistema operacional.

2. Instale as dependências

Dentro do diretório do projeto:

poetry install

3. Configure o Redis

Para execução local, o Redis deve estar disponível na máquina.

A aplicação utiliza por padrão:

REDIS_HOST=localhost
REDIS_PORT=6379

4. Execute a aplicação
poetry run uvicorn app.main:app --reload


A API ficará disponível em:

http://localhost:8000

🛑 Encerrando o projeto

Se estiver utilizando Docker Compose:

docker compose down


Caso queira remover também os volumes associados:

docker compose down -v


Atenção: utilize -v apenas se quiser remover os volumes criados pelo Docker Compose.

📌 Resumo dos principais comandos
Ação	Comando
Construir e iniciar	docker compose up --build
Iniciar em segundo plano	docker compose up --build -d
Ver containers	docker compose ps
Ver logs	docker compose logs -f api
Parar aplicação	docker compose down
Executar testes	poetry run pytest
Executar testes detalhados	poetry run pytest -v
Executar localmente	poetry run uvicorn app.main:app --reload
🔗 Links úteis

Repositório: https://github.com/iuriolv/projeto-final-ebac-backend

PokéAPI: https://pokeapi.co/

Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

👨‍💻 Autor

Iuri Oliveira

Projeto desenvolvido como parte do Projeto Final — EBAC Backend.