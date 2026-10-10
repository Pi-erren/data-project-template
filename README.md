# data-project-template

Template de départ pour tout projet data : **Python + uv + Docker**, packagé comme **Dev Container VS Code**.

## Structure

```
.
├── src/                     # code du projet
│   └── main.py              # point d'entrée
├── scripts/                 # notebooks Jupyter d'exploration
├── data/                    # données locales (ignorées par git)
├── tests/                   # tests pytest
├── pyproject.toml           # dépendances (uv)
├── uv.lock                  # lockfile reproductible
└── .devcontainer/           # tout l'environnement Docker
    ├── Dockerfile           # python:3.12-slim + uv + git + openssh-client
    ├── docker-compose.yaml  # build + volume .:/app + mount SSH
    └── devcontainer.json    # config VS Code Dev Container
```

## Démarrage rapide (Dev Container, recommandé)

1. Ouvrez le projet dans VS Code.
2. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container** (l'extension Dev Containers s'occupe du build).
3. Le workspace complet est monté dans `/app`, les dépendances sont installées par `uv sync` au `postCreateCommand`.

Le conteneur monte aussi votre `~/.ssh` en lecture seule : les clés SSH de la machine hôte sont disponibles dans le conteneur, donc `git push` fonctionne directement (GitHub/SSH).

## Démarrage rapide (local, sans Docker)

```bash
uv sync
uv run python src/main.py
uv run pytest
```

## Utiliser le compose directement (sans VS Code)

```bash
docker compose -f .devcontainer/docker-compose.yaml up --build
docker compose -f .devcontainer/docker-compose.yaml run --rm app uv run pytest
```

## Ajouter une dépendance

```bash
uv add <package>          # ajoute dans pyproject.toml + uv.lock
uv add --group dev <tool> # outil de dev uniquement
```

Puis **Rebuild Container** dans VS Code (ou `docker compose ... up --build`).

## SSH / Git depuis le conteneur

- Le volume `- ~/.ssh:/root/./.ssh:ro` expose vos clés SSH hôte au conteneur (lecture seule).
- Le `Dockerfile` installe `git` et `openssh-client`.
- `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` sont propagés depuis la machine hôte (à définir dans votre shell hôte si besoin).

## À faire pour un nouveau projet

1. Cloner ce template dans un nouveau repo (voir "Use this repository as template" sur GitHub).
2. Renommer le projet dans `pyproject.toml` (`name = ...`) et `"name"` dans `.devcontainer/devcontainer.json`.
3. Supprimer ce paragraphe et adapter le README.
