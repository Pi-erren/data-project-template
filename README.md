# data-project-template

Template de départ pour tout projet data : **Python + uv + Docker**, packagé comme **Dev Container VS Code**.

## Structure

```
.
├── src/                     # code du projet
│   └── main.py              # point d'entrée
├── scripts/                 # notebooks Jupyter d'exploration
├── data/                    # données locales (ignorées par git)
├── pyproject.toml           # dépendances (uv)
├── uv.lock                  # lockfile reproductible
└── .devcontainer/          # tout l'environnement Docker
    ├── Dockerfile           # python:3.12-slim + uv + git + openssh-client
    ├── docker-compose.yaml  # build + volume .:/app
    └── devcontainer.json    # config VS Code Dev Container
```

## Démarrage rapide (Dev Container, recommandé)

1. Ouvrez le projet dans VS Code.
2. `Ctrl+Shift+P` → **Dev Containers: Reopen in Container** (l'extension Dev Containers s'occupe du build).
3. Le workspace complet est monté dans `/app`, les dépendances sont installées par `uv sync` au `postCreateCommand`.

## Transformer src en un package exécutable avec uv

Le code vit dans `src/`. Pour lancer le projet avec une commande simple (au lieu de
`uv run python src/main.py`), déclarez un point d'entrée console dans `pyproject.toml` :

1. Transformez `src/` en package importable : créez un dossier du nom du projet, par
   exemple `src/my_project/`, avec un `__init__.py` et déplacez-y `main.py`.
2. Dans `pyproject.toml`, remplacez `[tool.uv] package = false` par la déclaration de
   build et du script :

   ```toml
   [build-system]
   requires = ["uv_build>=1.0,<2.0"]
   build-backend = "uv_build"

   [tool.uv]
   package = true

   [tool.uv.build-backend]
   module-name = "my_project"
   module-root = ""

   [project.scripts]
   my-project = "my_project.main:main"
   ```

3. Lancez ensuite le projet avec :

   ```bash
   uv sync
   uv run my-project
   ```

Le nom à gauche (`my-project`) est la commande tapée dans le terminal ; la valeur est le
chemin d'import `package.module:fonction` appelé au démarrage. Pour refléter ce changement
dans Docker, mettez à jour le `CMD` du `Dockerfile` : `CMD ["uv", "run", "my-project"]`.

## Ajouter une dépendance

```bash
uv add <package>          # ajoute dans pyproject.toml + uv.lock
uv add --group dev <tool> # outil de dev uniquement
```

## À faire pour un nouveau projet

1. Cloner ce template dans un nouveau repo (voir "Use this repository as template" sur GitHub).
2. Renommer le projet dans `pyproject.toml` (`name = ...`) et `"name"` dans `.devcontainer/devcontainer.json`.
3. Supprimer ce paragraphe et adapter le README.
