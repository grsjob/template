# graph/ — слои графа для работы с нейронкой

Здесь два РАЗНЫХ слоя графа. Не путать — они решают разные задачи.

## A. Graphiti — память агента (temporal knowledge graph)

Копит сущности и факты во времени (требования, решения, участники, документы) и
отдаёт агенту релевантный подграф. Это НЕ граф структуры кода.

### Что нужно
- Docker + Docker Compose
- Ключ LLM (OpenAI по умолчанию) — для извлечения сущностей и эмбеддингов

### Запуск
```bash
cd graph
copy .env.example .env      # заполнить OPENAI_API_KEY
docker compose up
```
- MCP-эндпоинт: `http://localhost:8000/mcp/`
- Веб-UI FalkorDB: `http://localhost:3000`

### Основные MCP-инструменты
- `add_memory` — добавить эпизод (текст/JSON/сообщение) в граф
- `search_memory_facts` — искать факты (рёбра)
- `search_nodes` — искать сущности
- `get_episodes` — последние эпизоды

### Идея применения на хакатоне
Кейс «Требования из встречи»: скармливаешь транскрипты через `add_memory`
(source="text"), Graphiti извлекает `Requirement`/`Person`/`Document`,
а агент потом достаёт связный контекст для генерации БТ. Настройка типов
сущностей — в `config.yaml`.

---

## B. code-graph — граф структуры кода (cgraphy)

Именно этот слой оптимизирует запросы по КОДУ: tree-sitter парсит проект в граф
символов/вызовов/импортов, агент читает только нужный символ, а не файлы целиком.

### Установка и индексация (Python)
```bash
pip install cgraphy
cgraphy index .              # строит .cgraphy/graph.db (инкрементально)
```

### Как подключить к агенту (MCP)
cgraphy поднимается как MCP-сервер; готовый блок регистрации — в
`.cursor/mcp.example.json` (скопировать в `.cursor/mcp.json`). Инструменты, которые
появятся у агента: `cgraphy_overview`, `cgraphy_search`, `cgraphy_context`, `cgraphy_read`.

### Альтернатива для Windows без возни с тулчейном
`repo-map` — precompiled tree-sitter, «no C toolchain, including on Windows».
Инструменты: `where_is`, `outline`, `get_symbol`, `who_references`.

---

## Что коммитить

- Коммитим: `docker-compose.yml`, `config.yaml`, `.env.example`, этот README.
- НЕ коммитим: `graph/.env`, индексы (`.cgraphy/`, `.codegraph/`), тома БД
  (уже в `.gitignore`).
