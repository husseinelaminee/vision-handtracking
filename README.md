# Vision-HandTracking – Pipeline modulaire de vision par ordinateur

**Vision-HandTracking** est un projet personnel visant à construire un **pipeline modulaire**, déterministe et extensible pour le hand-tracking.
L’objectif est de permettre d’enchaîner une série de *stages* (capture → prétraitement → détection → tracking → communication réseau, etc.) de manière flexible et testable, tout en restant simple à itérer.

---

## Compatibilité

* **Python** : 3.10 – 3.11
* **OS supportés** : Ubuntu / Windows
* **Dépendances** : gérées automatiquement via `setup.sh` / `setup.ps1`

---

# 1. Installation & Environnement

### Ubuntu

```bash
./setup.sh
```

### Windows (PowerShell)

```powershell
.\setup.ps1
```

Ces scripts :

* créent automatiquement un environnement Python isolé (`.venv`)
* installent toutes les dépendances requises
* configurent les alias locaux pour exécuter le bon interpréteur

---

# 2. Exécution de l’application

Une fois l’environnement configuré :

### Linux

```bash
./python manual_tests/app/test_app.py
```

### Windows

```powershell
.\python.ps1 manual_tests/app/test_app.py
```

**Note :** `./python` et `./python.ps1` pointent automatiquement vers l’interpréteur virtuel, donc pas besoin d’activer l’environnement manuellement.

---

# 3. Lancer les tests

### Exécuter toute la suite :

```bash
./python -m pytest
```

### Ajouter un test

1. Créer un fichier dans `tests/` avec un nom du style :

```text
test_nom_module.py
```

2. Suivre la structure pytest (fonctions commençant par `test_...`).

> Les tests se concentrent actuellement sur l’orchestration du pipeline et les utilitaires critiques.

---

# 4. Structure du projet

```text
├── app/                     # Applications exécutables
├── vision/                  # Stages de pipeline (capture, prétraitement, etc.)
├── utils/                   # Helpers, logging, structures partagées
├── manual_tests/            # Expérimentations manuelles
├── tests/                   # Tests unitaires pytest
├── setup.sh / setup.ps1     # Scripts d'installation automatisée
├── python / python.ps1      # Wrappers d’exécution
└── pyproject.toml           # Gestion du projet et dépendances
```

---

# 5. Concepts clés & Architecture technique

> Les points ci-dessous décrivent **l’architecture visée**, dont certaines parties sont déjà en place et d’autres encore en développement.
> Cela permet de documenter clairement la direction technique du projet.

## Pipeline linéaire (DAG simplifié)

Le pipeline se compose d’une suite déterministe de *stages* :

```text
[Capture] → [Prétraitement] → [Détection] → [Tracking] → [Sortie]
```

Aujourd’hui :

* la structure **est linéaire**
* les stages sont entièrement interchangeables
* l’orchestration centralise la logique de passage des données entre stages

Futur :

* support de branches (DAG réel)
* gestion d’état et de synchronisation plus complexe

---

## Patterns logiciels utilisés

Plusieurs patterns sont déjà en place ou prévus :

| Pattern                     | Utilisation prévue                                           |
| --------------------------- | ------------------------------------------------------------ |
| **Observer / Publisher**    | Propagation d’événements ou d’images entre stages            |
| **Chain of Responsibility** | Pipeline séquentiel configurable                             |
| **Strategy**                | Choix du modèle ou de l’algorithme sans modifier le pipeline |
| **Dependency Injection**    | Faciliter le remplacement ou le mock pour les tests          |

---

## Philosophie orientée tests

Le projet est conçu pour rester stable malgré les expérimentations :

* tests unitaires sur l’orchestrateur du pipeline
* tests sur utilitaires et structures de données
* intégration continue (GitHub Actions) pour exécuter pytest à chaque push

Objectif : garantir que les refactorings fréquents ne cassent pas la chaîne.

---

## Intégrations futures (en cours)

Certaines fonctionnalités sont en conception et non encore implémentées, mais font partie de la vision globale.

### 🔹 ROS2 & simulation (ex. SOFA)

Objectif :

* publier un petit nombre de degrés de liberté (1–2 DOF)
* piloter une simulation à partir du tracking
* permettre des démonstrations interactives

---

### 🔹 Collecte & auto-annotation

En préparation :

* pipeline de capture
* auto-annotation basée sur détecteur existant
* enregistrement pour dataset supervisé

---

### 🔹 Imitation learning / Behavior Cloning

Objectif futur :

* entraîner un modèle capable de reproduire un geste sans input caméra
* se baser uniquement sur l’historique des démonstrations

---

# 6. Roadmap

### Court terme (en cours)

* Refactoring et amélioration continue de l’application
* Ajout de tests pour les modules vision/capture
* Ajout de métriques et tests de performance/benchmark
* Documentation interne

### Moyen terme

* Fonctionnalité de replays et tests de déterminisme
* Ajout d’un stage ROS2 Publisher
* Enregistrement / auto-annotation des frames
* Visualisation en temps réel / debug UI

### Long terme

* DAG dynamique
* Système multi-caméra
* Imitation learning complet

---

# 7. Licence

MIT — libre utilisation, modification et redistribution.

---

# 8. Contribution

Même pour usage personnel, le projet est ouvert aux contributions :

1. Fork
2. Nouvelle branche `feature/...` ou `fix/...`
3. Commit clair et explicite
4. Pull Request
