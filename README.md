# 🐍 Pokémon API — Projeto Final EBAC

API REST desenvolvida em Python com FastAPI como projeto final do curso de Backend Python da EBAC.

A aplicação integra a [PokéAPI](https://pokeapi.co/) para consultar informações de Pokémon e também disponibiliza um CRUD próprio com persistência em SQLite, utilizando SQLAlchemy como ORM. O Redis é utilizado para armazenar temporariamente os resultados das consultas individuais à API externa, reduzindo requisições repetidas.

O projeto conta com testes automatizados, documentação interativa, configuração por variáveis de ambiente e suporte à execução com Docker Compose.

## 🚀 Tecnologias

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Redis
- Requests
- Poetry
- Pytest
- pytest-cov
- Docker
- Docker Compose
- PokéAPI

## 📋 Funcionalidades

- Consulta e listagem de Pokémon através da PokéAPI.
- Paginação dos resultados externos.
- Consulta individual com cache Redis e expiração de 5 minutos.
- Cadastro de Pokémon no banco SQLite.
- Listagem dos Pokémon cadastrados localmente.
- Consulta de registros por ID.
- Atualização e exclusão de registros.
- Validação de dados com Pydantic.
- Tratamento de erros e registros inexistentes.
- Persistência de dados com SQLAlchemy.
- Documentação automática com Swagger e ReDoc.
- Testes automatizados com Pytest e medição de cobertura.

## 📦 Pré-requisitos

Para executar com Docker:

- Docker
- Docker Compose

Para executar localmente:

- Python 3.14
- Poetry
- Redis em execução

## 🔽 Clonando o projeto

```bash
git clone https://github.com/iuriolv/projeto-final-ebac-backend.git
cd projeto-final-ebac-backend
```

## 🐳 Executando com Docker Compose

Na raiz do projeto, execute:

```bash
docker compose up --build -d
```

O Compose irá construir a imagem da API, instalar as dependências, iniciar o Redis e executar a aplicação FastAPI.

A API ficará disponível em:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Comandos úteis

Verificar os serviços:

```bash
docker compose ps
```

Consultar os logs da API:

```bash
docker compose logs -f api
```

Parar os serviços:

```bash
docker compose down
```

O banco SQLite utiliza um volume persistente para manter os registros quando o contêiner da API é recriado. O Redis também possui um volume para persistência dos dados do cache.

**Atenção:** `docker compose down -v` remove os volumes do projeto e pode apagar os dados persistidos.

## ⚙️ Configuração por variáveis de ambiente

O projeto utiliza variáveis de ambiente para configurar o banco de dados e a conexão com o Redis.

Crie seu arquivo `.env` com base no `.env.example`, caso necessário para sua execução local.

Exemplo de configuração local:

```dotenv
DATABASE_URL=sqlite:///./pokemon.db
REDIS_HOST=localhost
REDIS_PORT=6379
```

No Docker Compose, o banco é configurado para utilizar o arquivo `/data/pokemon.db`, armazenado no volume persistente, e o Redis é acessado pelo nome do serviço `redis`.

## 📚 Documentação da API

O FastAPI disponibiliza documentação interativa automaticamente.

- **Swagger:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Através dessas interfaces, é possível consultar os endpoints, informar parâmetros, enviar requisições e visualizar as respostas.

## 🔗 Endpoints disponíveis

### Verificação da aplicação

#### `GET /`

Verifica se a API está funcionando.

Exemplo de resposta:

```json
{
  "Hello": "World"
}
```

### CRUD local — SQLite

Os endpoints abaixo operam sobre os Pokémon armazenados no banco de dados local.

#### `POST /pokemons`

Cadastra um Pokémon.

Exemplo de requisição:

```json
{
  "name": "pikachu",
  "height": 4,
  "weight": 60,
  "types": ["electric"],
  "front_default": "https://example.com/front.png",
  "back_default": "https://example.com/back.png"
}
```

A API gera o ID do registro e retorna os dados cadastrados.

#### `GET /pokemons`

Lista os Pokémon cadastrados no banco local.

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": ["electric"],
    "front_default": "https://example.com/front.png",
    "back_default": "https://example.com/back.png"
  }
]
```

Se não houver registros, a resposta será uma lista vazia.

#### `GET /pokemons/{id}`

Busca um Pokémon cadastrado pelo ID.

Exemplo:

```http
GET /pokemons/1
```

Caso o registro não exista, a API retorna `404 Not Found`.

#### `PUT /pokemons/{id}`

Atualiza os dados de um Pokémon existente.

Exemplo:

```http
PUT /pokemons/1
```

O corpo da requisição deve conter os campos esperados pelo schema de criação, incluindo nome, altura, peso e tipos. Os campos de sprites são opcionais.

Caso o ID não exista, a API retorna `404 Not Found`.

#### `DELETE /pokemons/{id}`

Exclui um Pokémon cadastrado.

Exemplo:

```http
DELETE /pokemons/1
```

Resposta de sucesso:

```json
{
  "mensagem": "Pokemon excluído com sucesso"
}
```

Caso o registro não exista, a API retorna `404 Not Found`.

### Integração com a PokéAPI

As rotas externas são separadas do CRUD local para evitar conflitos entre os dados consultados na PokéAPI e os registros salvos no SQLite.

#### `GET /pokeapi/pokemons`

Lista os Pokémon disponibilizados pela PokéAPI.

Parâmetros:

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `page` | Integer | 1 | Página solicitada |
| `limit` | Integer | 20 | Quantidade de resultados por página |

Exemplo:

```http
GET /pokeapi/pokemons?page=1&limit=20
```

A resposta contém os metadados de paginação, os links para a página anterior e a próxima e os resultados da PokéAPI.

O deslocamento é calculado por:

```python
offset = (page - 1) * limit
```

#### `GET /pokeapi/pokemons/{id}`

Consulta um Pokémon na PokéAPI pelo ID.

Exemplo:

```http
GET /pokeapi/pokemons/25
```

A resposta inclui:

- `name`: nome do Pokémon.
- `id`: identificador.
- `height`: altura.
- `weight`: peso.
- `types`: lista de tipos.
- `sprites`: URLs das imagens frontal e traseira.

Se o Pokémon não for encontrado na API externa, a aplicação retorna `404 Not Found`.

## ⚡ Cache com Redis

O endpoint de consulta individual verifica primeiro se os dados estão armazenados no Redis.

O fluxo de consulta é:

1. A API recebe o ID do Pokémon.
2. Verifica a existência dos dados no cache.
3. Se houver dados, retorna o resultado armazenado.
4. Caso contrário, consulta a PokéAPI.
5. Armazena o resultado no Redis por 300 segundos.
6. Retorna os dados ao cliente.

O cache reduz requisições repetidas à fonte externa. Ele não substitui o SQLite, que é responsável pela persistência dos registros do CRUD local.

## 🗄️ Banco de dados

O projeto utiliza SQLite com SQLAlchemy para persistir os registros criados pela API.

O SQLAlchemy é responsável pelo mapeamento entre os objetos Python e a tabela de Pokémon no banco de dados.

O arquivo SQLite é configurado pela variável `DATABASE_URL`. Na execução com Docker Compose, um volume mantém os dados persistidos fora do ciclo de vida do contêiner.

## 🧪 Executando os testes

O projeto utiliza Pytest para validar o CRUD e a integração com a PokéAPI.

Executar todos os testes:

```bash
poetry run pytest
```

Executar com detalhes:

```bash
poetry run pytest -v
```

Executar com relatório de cobertura:

```bash
poetry run pytest --cov=app --cov-report=term-missing
```

A cobertura observada durante o desenvolvimento chegou a **99%**, considerando os arquivos contabilizados pelo relatório.

Os testes do CRUD utilizam um banco SQLite isolado, permitindo validar as operações sem depender dos registros do banco de desenvolvimento.

## 💻 Executando localmente

### 1. Instalar as dependências

Com o Poetry instalado, execute:

```bash
poetry install
```

### 2. Configurar o ambiente

Configure as variáveis de ambiente necessárias, conforme o arquivo `.env.example`.

Certifique-se de que o Redis esteja disponível em `localhost:6379`.

### 3. Iniciar a aplicação

```bash
poetry run uvicorn app.main:app --reload
```

A API ficará disponível em http://localhost:8000.

## 🔗 Links úteis

- [Repositório no GitHub](https://github.com/iuriolv/projeto-final-ebac-backend)
- [PokéAPI](https://pokeapi.co/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentação do Redis](https://redis.io/docs/)

## 👨‍💻 Autor

**Iuri Oliveira**

Projeto desenvolvido como parte do Projeto Final do curso de Backend Python da EBAC.