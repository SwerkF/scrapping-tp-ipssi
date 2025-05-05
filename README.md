# Projet de Scraping Web

Ce projet est une application web complète pour le scraping, le stockage et l'affichage de données issues du blog du modérateur. Il comprend un backend Python pour le scraping et l'API, et un frontend React pour l'interface utilisateur.

## Architecture du projet

Le projet est composé de trois parties principales:

-   **Backend**: API FastAPI et scripts de scraping en Python
-   **Frontend**: Application React avec TypeScript
-   **Base de données**: MongoDB pour le stockage des données

## Prérequis

-   Docker et Docker Compose
-   Git

## Installation

1. Clonez le dépôt:

    ```bash
    git clone <url-du-repos>
    cd Scrapping
    ```

2. Lancez l'application avec Docker Compose:
    ```bash
    docker-compose up --build
    ```

## Services disponibles

Une fois l'application lancée, vous pouvez accéder aux services suivants:

-   **Frontend**: http://localhost:5173
-   **API Backend**: http://localhost:8000
-   **MongoDB**: mongodb://localhost:27017
-   **Mongo Express** (interface d'administration MongoDB): http://localhost:8081

## Fonctionnalités principales

### Backend

-   Scraping de données du Blog du Modérateur
-   Stockage des articles dans MongoDB
-   API RESTful pour accéder aux données
-   Classification par catégories et sous-catégories

### Endpoints API

-   `GET /hello`: Message de test
-   `GET /api/articles`: Liste des articles avec filtrage et pagination
-   `GET /api/categories`: Liste des catégories et sous-catégories disponibles

### Frontend

-   Interface utilisateur moderne avec React
-   Affichage des articles et catégories
-   Recherche et filtrage des articles
-   Responsive design

## Structure du projet

```
Scrapping/
├── backend/                # Code du backend
│ ├── api.py                # API FastAPI
│ ├── db.py                 # Logique d'accès à la base de données
│ ├── tp_ipssi.py           # Script de scraping
│ ├── requirements.txt      # Dépendances Python
│ ├── Dockerfile.api        # Configuration Docker pour l'API
│ └── Dockerfile.mongodb    # Configuration Docker pour MongoDB
├── frontend/               # Code du frontend React
│ ├── src/                  # Sources de l'application
│ ├── package.json          # Dépendances JavaScript
│ └── Dockerfile            # Configuration Docker pour le frontend
├── bruno/                  # Tests API avec Bruno
└── docker-compose.yaml     # Configuration Docker Compose
```

## Développement

### Backend

Le backend utilise FastAPI pour l'API et BeautifulSoup pour le scraping. Pour développer localement sans Docker:

```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
```

### Frontend

Le frontend est développé avec React, TypeScript et Vite. Pour développer localement sans Docker:

```bash
cd frontend
pnpm install
pnpm dev
```

## Notes de déploiement

Pour un déploiement en production, il est recommandé de:

-   Configurer des mots de passe sécurisés pour MongoDB
-   Activer HTTPS pour l'API et le frontend
-   Configurer un reverse proxy comme Nginx
