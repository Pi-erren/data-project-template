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

## Initialiser un projet uv (si besoin)

Ce template est déjà un projet uv valide (`pyproject.toml` + `uv.lock`). Si vous partez
d'un dossier vide ou si vous devez réinitialiser la configuration :

```bash
uv init --bare                    # crée un pyproject.toml minimal (sans écraser l'existant)
uv add <package>                  # ajoute une dépendance (met à jour pyproject.toml et uv.lock)
uv add --group dev <tool>         # outil de dev uniquement (ruff, pyright...)
uv sync                           # crée/mets à jour .venv depuis uv.lock
uv lock --upgrade                 # met à jour les versions verrouillées
```

Installez uv s'il n'est pas présent : `curl -LsSf https://astral.sh/uv/install.sh | sh`
(ou `pip install uv`, `pipx install uv`, `brew install uv`).

## Définir la commande de lancement du projet

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

## Démarrage rapide (local, sans Docker)

```bash
uv sync
uv run python src/main.py
```

## Utiliser le compose directement (sans VS Code)

```bash
docker compose -f .devcontainer/docker-compose.yaml up --build
docker compose -f .devcontainer/docker-compose.yaml run --rm app uv run python src/main.py
```

## Ajouter une dépendance

```bash
uv add <package>          # ajoute dans pyproject.toml + uv.lock
uv add --group dev <tool> # outil de dev uniquement
```

Puis **Rebuild Container** dans VS Code (ou `docker compose ... up --build`).

## SSH / Git depuis le conteneur

Le conteneur n'a **pas** besoin de vos clés SSH montées : VS Code Dev Containers forward
automatiquement votre `ssh-agent` local dans le conteneur (`SSH_AUTH_SOCK`).
Important : `ssh-add` doit être exécuté **sur la machine hôte**, pas dans le conteneur —
la clé reste sur l'hôte, seul l'agent y est forwardé. Assurez-vous que votre agent
tourne sur la machine hôte avec la clé chargée :

```bash
ssh-add                       # liste les clés chargées (à lancer sur l'hôte)
ssh-add ~/.ssh/id_ed25519    # si aucune
```

Ensuite `git push` / `git pull` en SSH fonctionnent directement dans le conteneur.
`git` et `openssh-client` sont installés dans l'image.

### Identité Git dans le conteneur

Le nom et l'email de commit sont repris de `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL`
définis sur la machine hôte (via `postStartCommand` dans `devcontainer.json`).
Si ces variables ne sont pas définies sur l'hôte, configurez l'identité **dans le
conteneur**, une seule fois :

```bash
git config --global user.name  "Prénom Nom"
git config --global user.email "prenom@example.com"
```

## À faire pour un nouveau projet

1. Cloner ce template dans un nouveau repo (voir "Use this repository as template" sur GitHub).
2. Renommer le projet dans `pyproject.toml` (`name = ...`) et `"name"` dans `.devcontainer/devcontainer.json`.
3. Supprimer ce paragraphe et adapter le README.
