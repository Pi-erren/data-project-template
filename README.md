# data-project-template

Template de départ pour tout projet data : **Python + uv + Docker**.

## Structure

```
.
├── src/                 # code du projet
│   └── main.py          # point d'entrée
├── data/                # données locales (montées dans le conteneur, ignorées par git)
├── tests/               # tests pytest
├── pyproject.toml       # dépendances (uv)
├── uv.lock              # lockfile reproductible
├── Dockerfile           # image basée sur python:3.12-slim + uv
├── docker-compose.yaml  # build + volumes (src/ et data/ montés)
└── .devcontainer/       # config VS Code Dev Container
```

## Démarrage rapide (local, sans Docker)

```bash
uv sync
uv run python src/main.py
uv run pytest
```

## Démarrage rapide (Docker)

```bash
docker compose up --build        # lance src/main.py
docker compose run --rm app uv run pytest
```

Le code dans `src/` et les données dans `data/` sont montés comme volumes :
vous pouvez modifier le code à chaud sans rebuild.

## Ajouter une dépendance

```bash
uv add <package>          # ajoute dans pyproject.toml + uv.lock
uv add --group dev <tool> # outil de dev uniquement
```

Puis rebuild : `docker compose up --build`.

## À faire pour un nouveau projet

1. Cloner ce template dans un nouveau repo (voir ci-dessous).
2. Renommer le projet dans `pyproject.toml` (`name = ...`).
3. Supprimer ce paragraphe et adapter le README.
