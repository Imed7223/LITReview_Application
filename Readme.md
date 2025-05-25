# 📚 LITRevu

LITRevu est une application web développée avec Django permettant à une communauté d'utilisateurs de :
- publier des critiques de livres ou d'articles,
- demander une critique via un billet,
- consulter un flux personnalisé basé sur les critiques et billets des utilisateurs suivis.

---

## 🚀 Fonctionnalités principales

- 📝 Création de **billets** pour demander une critique
- 💬 Publication de **critiques** en réponse à un billet (ou directement avec billet + critique en une étape)
- 📢 **Flux personnalisé** affichant :
  - billets et critiques de l'utilisateur connecté,
  - contenus des utilisateurs suivis,
  - critiques de billets de l'utilisateur connecté
- 🤝 Suivi d'autres utilisateurs par nom d'utilisateur
- 🔒 Authentification (inscription, connexion, déconnexion)
- ⚙️ Interface d'administration Django pour la gestion complète

---

## 🧱 Structure du projet

litrevu/
├── accounts/ # Gestion des utilisateurs personnalisés
├── reviews/ # Logiciel métier (billets, critiques, abonnements)
├── templates/ # Fichiers HTML (avec includes)
│ ├── registration/ # Login / Signup
│ └── reviews/ # Feed, forms, snippets
├── static/ # CSS (style minimaliste et accessible)
├── litrevu/ # Configuration Django principale
├── db.sqlite3 # Base de données avec données de test
└── manage.py # Lanceur du projet Django


---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/litrevu.git
cd litrevu

2. Créer et activer un environnement virtuel
python -m venv env
# Windows
env\\Scripts\\activate
# macOS/Linux
source env/bin/activate
3. Installer les 
pip install -r requirements.txt
Si le fichier requirements.txt n’est pas encore créé, tu peux le générer avec :
pip freeze > requirements.txt

 Lancer l'application en local
 python manage.py migrate
python manage.py createsuperuser  # si tu veux accéder à /admin
python manage.py runserver
Puis va sur : http://127.0.0.1:8000

Accès à l'administration Django
