#1. Description Générale
Le projet est une application web "Single Page Application" (SPA) conçue pour la génération dynamique de CV professionnels, spécifiquement adaptée aux métiers du service à la personne (SPE). L'outil permet une édition en temps réel avec une interface scindée en deux : une colonne de formulaire à gauche et une prévisualisation PDF à droite.

#2. Fonctionnalités Clés
Édition en temps réel : Chaque modification dans le formulaire met immédiatement à jour la prévisualisation du CV.

Dynamisme des données :

Chargement asynchrone (fetch) de données métiers et compétences à partir de fichiers JSON (competences_SPE_par_metier.json).

Adaptation automatique du titre du métier selon le genre (Masculin/Féminin).

Gestion avancée des blocs :

Ajout dynamique de blocs d'expériences professionnelles.

Gestion complexe des formations avec système de "tags" pour les modules associés (ajout, suppression, prévention des doublons).

Personnalisation graphique : Sélecteur de couleurs de thème influençant les éléments CSS (--main-color).

Gestion des fichiers :

Import/Export de CV au format .json.

Upload de photo avec gestion dynamique de la taille.

Impression : Feuille de style dédiée @media print pour garantir une mise en page optimale (format A4) lors de la génération PDF.

#3. Architecture Technique
Structure HTML : Interface flex avec une sidebar (.form-side) et une zone de rendu (.preview-side).

CSS : Utilisation de variables CSS pour le thémage, structure en grid et flexbox.

JavaScript :

init() : Fonction asynchrone gérant le chargement initial des données.

update() : Moteur central de rendu qui reconstruit le DOM de la prévisualisation à chaque modification.

addModuleTag() : Logique de manipulation du DOM pour gérer les tags de modules de formation de manière encapsulée (par bloc).

saveData() / loadData() : Fonctions de sérialisation/désérialisation JSON.

#4. Stack utilisée
HTML5 / CSS3 / JavaScript Vanilla (ES6+).

Google Fonts (Montserrat).

Pas de dépendances externes (pas de framework type React/Vue), garantissant une portabilité totale.

#5. Instructions pour les prochaines évolutions
Maintenir l'isolation des blocs lors de l'ajout d'expériences ou de formations.

Veiller à la synchronisation entre le DOM généré dans update() et les écouteurs d'événements (notamment pour les boutons de suppression des tags).

Gestion des erreurs : Le chargement des fichiers JSON est encapsulé dans des blocs try/catch pour éviter le blocage de l'application en cas d'absence des fichiers.
