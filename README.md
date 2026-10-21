# Pokémon API — EBAC

API desenvolvida em Python com FastAPI para consultar informações de Pokémon por meio da [PokéAPI](https://pokeapi.co/), armazenar dados localmente e disponibilizar operações de consulta e gerenciamento.

O projeto foi desenvolvido como parte da formação de Desenvolvedor Full Stack Python da EBAC, com foco em integração entre APIs, persistência de dados, cache, conteinerização e automação de processos.

## Funcionalidades

- Consulta de Pokémon utilizando a PokéAPI.
- Listagem paginada de Pokémon.
- Consulta de detalhes por identificador.
- Armazenamento local dos dados com SQLite e SQLAlchemy.
- Cache com Redis para reduzir requisições externas repetidas.
- Operações CRUD para os Pokémon armazenados localmente.
- Tratamento de erros nas requisições externas.
- Conteinerização com Docker e Docker Compose.
- Automação de execução de testes e verificação de cobertura com GitHub Actions.

## Tecnologias utilizadas

- **Python** — linguagem principal.
- **FastAPI** — desenvolvimento da API REST.
- **Pydantic** — validação e estruturação dos dados.
- **SQLAlchemy** — mapeamento objeto-relacional (ORM).
- **SQLite** — banco de dados local.
- **Redis** — armazenamento temporário em cache.
- **Requests** — consumo da API externa.
- **Pytest** — testes automatizados.
- **pytest-cov** — análise de cobertura de testes.
- **Poetry** — gerenciamento de dependências.
- **Docker e Docker Compose** — conteinerização e execução dos serviços.
- **GitHub Actions** — integração contínua (CI).

## Como funciona

1. A aplicação recebe uma requisição HTTP.
2. Nas consultas à PokéAPI, verifica se os dados estão disponíveis no Redis.
3. Se houver dados em cache, retorna o resultado armazenado.
4. Caso contrário, consulta a PokéAPI e armazena os dados obtidos, conforme o fluxo da rota.
5. Os detalhes dos Pokémon consultados podem ser persistidos no banco de dados local.
6. As rotas CRUD permitem criar, consultar, atualizar e excluir registros locais.

O cache utiliza um tempo de expiração de 300 segundos (5 minutos).

## Endpoints

### Integração com a PokéAPI

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/pokeapi/pokemons` | Lista Pokémon com paginação |
| GET | `/pokeapi/pokemons/{id}` | Consulta detalhes de um Pokémon |

Exemplo de paginação:

`GET /pokeapi/pokemons?page=1&limit=20`

### Gerenciamento local

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/pokemons` | Cadastra um Pokémon |
| GET | `/pokemons` | Lista Pokémon armazenados localmente |
| GET | `/pokemons/{id}` | Consulta um Pokémon local pelo ID |
| PUT | `/pokemons/{id}` | Atualiza um registro |
| DELETE | `/pokemons/{id}` | Exclui um registro |

Os endpoints locais operam sobre os dados armazenados no banco de dados da aplicação.

## Como executar localmente

### Pré-requisitos

- Python compatível com as dependências do projeto.
- Poetry.
- Docker e Docker Compose, caso queira executar os serviços em contêineres.

### Opção 1 — Executar com Poetry

Clone o repositório:

```bash
git clone https://github.com/iuriolv/projeto-final-ebac.git
cd projeto-final-ebac
```

Instale as dependências:

```bash
poetry install
```

Configure as variáveis de ambiente conforme a seção abaixo e inicie o Redis, se necessário.

Execute a aplicação:

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Opção 2 — Executar com Docker Compose

Na raiz do projeto, execute:

```bash
docker compose up -d --build
```

Para consultar os logs:

```bash
docker compose logs -f api
```

Para encerrar os contêineres:

```bash
docker compose down
```

Os dados persistidos nos volumes nomeados são mantidos quando os contêineres são removidos sem excluir os volumes.

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto ou configure as variáveis diretamente no ambiente de execução.

| Variável | Descrição | Exemplo local |
|---|---|---|
| `DATABASE_URL` | URL de conexão com o banco de dados | `sqlite:///./pokemon.db` |
| `REDIS_HOST` | Host do Redis | `localhost` |
| `REDIS_PORT` | Porta do Redis | `6379` |

No Docker Compose, o host do Redis deve corresponder ao nome do serviço configurado no arquivo, como `redis`.

Não envie arquivos `.env` com credenciais ou dados sensíveis para o repositório. Utilize `.env.example` para documentar as variáveis necessárias.

## Testes e qualidade

Os testes automatizados são executados com Pytest.

Para executar a suíte de testes:

```bash
poetry run pytest -v
```

Para gerar o relatório de cobertura:

```bash
poetry run pytest --cov=app --cov-report=term-missing
```

O GitHub Actions executa verificações automatizadas conforme o workflow configurado no repositório.

## Deploy

A aplicação possui uma implantação no Render:

https://buscador-pokemon.onrender.com

A disponibilidade do serviço depende da configuração atual da plataforma e de suas dependências externas.

## Documentação da API

Com a aplicação em execução, acesse `/docs` para explorar os endpoints, consultar os parâmetros e enviar requisições pela interface Swagger UI.

## Autor

**Iuri Oliveira**

Projeto desenvolvido como parte do Projeto Final do curso de Backend Python da EBAC.