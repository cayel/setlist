# Setlist Application

Cette application permet de suivre les événements musicaux auxquels vous avez assisté, de rechercher des événements, et de visualiser des statistiques.

## Fonctionnalités

- **Accueil** : Affiche le nombre total d'événements auxquels vous avez assisté, ainsi que les événements récents.
- **Recherche** : Permet de rechercher des événements par date, artiste et lieu.
- **Statistiques** : Affiche des graphiques des concerts par année et par mois.
- **Administration** : Permet de rafraîchir la base de données avec les dernières données de l'API Setlist.fm.
- **Paramètres** : Permet de définir et de gérer votre nom d'utilisateur.

## Installation

1. Clonez le dépôt :
    ```sh
    git clone <URL_DU_DEPOT>
    cd setlist
    ```

2. Créez et activez un environnement virtuel :
    ```sh
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

4. Créez un fichier `.env` à la racine du projet et ajoutez votre clé API Setlist.fm :
    ```env
    SETLIST_API_KEY="votre_cle_api"
    ```

## Utilisation

Pour lancer l'application, exécutez la commande suivante :
```sh
streamlit run app.py