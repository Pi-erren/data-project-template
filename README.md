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
    ├── docker-compose.yaml  # build + volume .:/app
    └── devcontainer.json    # config VS Code Dev Container
```

## Démarrage rapide (Dev Container, recommandé)

1. Ouvrez le projet dans VS Code.
2. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container** (l'extension Dev Containers s'occupe du build).
3. Le workspace complet est monté dans `/app`, les dépendances sont installées par `uv sync` au `postCreateCommand`.

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

Le conteneur n'a **pas** besoin de vos clés SSH montées : VS Code Dev Containers forward automatiquement votre `ssh-agent` local dans le conteneur (`SSH_AUTH_SOCK`). Assurez-vous juste que votre agent tourne sur la machine hôte avec la clé chargée :

```bash
ssh-add                       # liste les clés chargées
ssh-add ~/.ssh/id_ed25519    # si aucune
```

Ensuite `git push` / `git pull` en SSH fonctionnent directement dans le conteneur. `git` et `openssh-client` sont installés dans l'image, et `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` sont propagés depuis la machine hôte.

## À faire pour un nouveau projet

1. Cloner ce template dans un nouveau repo (voir "Use this repository as template" sur GitHub).
2. Renommer le projet dans `pyproject.toml` (`name = ...`) et `"name"` dans `.devcontainer/devcontainer.json`.
3. Supprimer ce paragraphe et adapter le README.
