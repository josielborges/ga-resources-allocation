# Resource Allocation - FastAPI + Vue.js

Aplicação de alocação de recursos usando Algoritmo Genético, migrada de Streamlit para FastAPI + Vue.js.

## Estrutura do Projeto

```
resource-allocation/
├── backend/           # API FastAPI
│   ├── db/           # Banco de dados
│   │   ├── alembic/     # Migrations
│   │   ├── models.py    # Modelos SQLAlchemy
│   │   ├── schemas.py   # Schemas Pydantic
│   │   ├── crud.py      # Operações CRUD
│   │   └── database.py  # Configuração do banco
│   ├── scripts/      # Scripts utilitários
│   │   ├── setup_db.py  # Setup do banco
│   │   └── seed_data.py # Popular dados
│   ├── docs/         # Documentação
│   ├── main.py       # Servidor principal
│   ├── genetic_algorithm.py  # Lógica do AG
│   ├── Makefile      # Comandos úteis
│   └── requirements.txt
├── frontend/         # Interface Vue.js
│   ├── src/
│   │   ├── components/  # Componentes Vue
│   │   ├── App.vue     # Componente principal
│   │   └── main.js     # Entrada da aplicação
│   ├── package.json
│   └── vite.config.js
└── data/            # Dados JSON (colaboradores e projetos)
```

## Instalação e Execução

### Backend (FastAPI)
```bash
cd backend

# Instalação completa (dependências + banco + dados)
make full-setup

# Ou manualmente:
pip install -r requirements.txt
make start-db
make setup-db
python main.py
```
API disponível em: http://localhost:8000

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```
Interface disponível em: http://localhost:3000

## Funcionalidades

- **API REST**: Endpoints para dados e execução do algoritmo
- **Interface Moderna**: Vue.js com Element Plus
- **Visualizações**: Gráficos Chart.js e calendário FullCalendar
- **Componentes Modulares**: Separação clara de responsabilidades
- **Proxy de Desenvolvimento**: Comunicação automática entre frontend e backend

## Endpoints da API

- `GET /api/colaboradores` - Lista colaboradores
- `GET /api/projetos` - Lista projetos  
- `POST /api/executar-algoritmo` - Executa algoritmo genético

## Componentes Vue

- **DadosTab**: Exibe colaboradores e projetos
- **FitnessTab**: Gráfico de evolução da fitness
- **ConflitosTab**: Detalhes das penalidades
- **GanttTab**: Cronograma visual
- **CalendarioTab**: Vista calendário com filtros