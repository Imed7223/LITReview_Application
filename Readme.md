# 📚 LITReview_Application

LITReview_Application est une application web développée avec Django permettant à une communauté d'utilisateurs de :
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

LITReview_Application/
├── authentication/              # Application Django pour la gestion des utilisateurs personnalisés
│   ├── models.py                # Modèle utilisateur personnalisé (CustomUser)
│   ├── forms.py                 # Formulaires de login / inscription
│   ├── views.py                 # Vues d’authentification (login, logout, signup)
│   ├── validators.py                  
│   └── templates/authentication/  # Templates spécifiques à l'authentification
│       ├── base.html
│       ├── login.html
│       └── signup.html
│
├── reviews/                    # Application métier (tickets, reviews, abonnements)
│   ├── models.py               # Modèles Ticket, Review, UserFollows
│   ├── forms.py                # Formulaires pour tickets, critiques, abonnements
│   ├── views.py                # Vues principales : dashboard, creation, follow...
│   └── templates/reviews/      # Templates pour le flux, formulaires, et dashboard
│       ├── base.html
│       ├── dashboard.html
│       ├── ticket_form.html       
        ├── inscription_message.html
│       ├──edit_ ticket.html
│       ├── delete_review_confirm.html
│       ├── create_ticket_and_review.html
│       ├──confirm_unfollow.html
│       ├── confirm_delete.html
│       ├── review_form.html
│       ├── follow_user.html
│       ├── subscriptions.html       
        ├── user_list.html
│       └── user_follow_list.html
├── templates/                  # Dossier global de templates
│   └── base.html               # Template de base avec layout global
│
├── static/                     # Fichiers statiques (CSS, images éventuelles)
│   └── css/
│       └── styles.css          # Style global avec bonne accessibilité (WCAG)
│
├── media/                      # Dossier pour les images uploadées via Tickets
│   └── ticket_images/
│
├── LITReview/                    # Configuration principale Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3                  # Base de données SQLite avec jeux de données de test
├── manage.py                   # Script de gestion du projet Django
└── README.md                   # Documentation d'installation et d’utilisation



---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Imed7223/LITReview_Application.git
cd LITReview_Application

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
