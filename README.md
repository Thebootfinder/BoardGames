# Tablée

Appli web installable pour compter les points des jeux de société (Skyjo, Flip 7, Uno, 6 qui prend, ou n'importe quel autre jeu) et garder l'historique des parties.

- Fonctionne hors ligne une fois installée.
- Les parties restent sur le téléphone (stockage local). La page « Sauvegarde & partage » crée un fichier de sauvegarde à restaurer sur un autre appareil, et l'appli rappelle de sauvegarder quand plusieurs parties ne le sont pas.
- Partage sans serveur : une partie (ou tout l'historique) part dans un lien `#t=…` (JSON compressé). En l'ouvrant, l'ami ajoute les parties à son Tablée et relie les joueurs aux siens pour cumuler les stats.

## Installer sur son téléphone

- **iPhone (Safari)** : ouvrir le site, bouton Partager, puis « Sur l'écran d'accueil ».
- **Android (Chrome)** : ouvrir le site, menu ⋮, puis « Installer l'application ».

## Développement

`src.html` est la source unique (aussi utilisée pour le prototype Claude). `python3 build.py` génère `index.html`.
Pour tester : `python3 -m http.server` puis ouvrir http://localhost:8000.
Après une modification, changer `CACHE` dans `sw.js` pour forcer la mise à jour sur les téléphones.
