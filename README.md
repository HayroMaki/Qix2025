# Projet Qix

Prototype inspiré du jeu d'arcade **Qix** développé par Jules & Khephren. L'objectif est de capturer au moins 75 % de l'aire de jeu en traçant des lignes sans se faire toucher par le Qix (l'entité centrale) ni par les Sparx (ennemis circulant sur les chemins).

## Gameplay en bref

1. Le joueur démarre sur le périmètre d'un carré (mode *chemin*).
2. En appuyant sur la barre d'espace, il passe en mode *dessin* et trace une ligne à travers la zone vide.
3. Dès qu'il referme son tracé sur un chemin existant, la zone coupée est remplie si le Qix ne s'y trouve pas.
4. Trois vies permettent de survivre aux collisions avec le Qix, les Sparx ou son propre tracé.
5. Trois niveaux successifs augmentent la difficulté (Qix plus gros/rapide, davantage de Sparx).

## Commandes

| Action                | Touche                  |
| --------------------- | ----------------------- |
| Déplacer le joueur    | Flèches directionnelles |
| Mode dessin           | Espace                  |
| Quitter               | Échap                   |

## Boucles principales

- **Menu** : permet d'activer les variantes (obstacles, bonus, configuration), de lancer une partie classique ou d'afficher l'option 2 joueurs (prototype non implémenté).
- **Partie** : rafraîchit l'intégralité de la scène à chaque frame (chemins, zones, Qix, Sparx, bonus, etc.), vérifie la progression, gère les collisions et transitions de modes, et contrôle la montée de niveau.

## Variantes & options

- **Obstacles** : chargés depuis `data/obstacles.txt` ou générés aléatoirement. Ils bloquent le joueur pendant le mode dessin.
- **Bonus** : issus de `data/bonus.txt` ou générés aléatoirement. Les bonus rendent le joueur temporairement invincible.
- **Configuration** : le fichier `data/config.txt` ajuste la taille/vitesse du Qix, le nombre de Sparx et la taille initiale de la zone jouable.
- **Mode 2 joueurs** : interface présente mais gameplay non implémenté.

## Architecture du code

Tout le gameplay est regroupé dans `QixRendu3.py` et s'appuie sur la bibliothèque `fltk` pour l'affichage. Les principales catégories de fonctions sont :

- **Affichage** : rendu de la fenêtre, polygones, Qix, Sparx, bonus, HUD (vie, score, surface capturée).
- **Gestion d'état** : bascule entre modes chemin/dessin, suivi des chemins, stockage des zones capturées, calcul d'aires.
- **IA ennemies** : déplacement pseudo-aléatoire du Qix avec rebonds sur les chemins, suivi des chemins et reconnection pour les Sparx.
- **Systèmes auxiliaires** : lecture des fichiers de données, génération de bonus/obstacles, adaptation des chemins après capture, ray tracing pour déterminer l'appartenance des points.

## Données & ressources

```
data/
 ├─ config.txt      # paramètres initiaux (taille/vitesse du Qix, nb de Sparx, taille de zone)
 ├─ obstacles.txt   # obstacles prédéfinis
 └─ bonus.txt       # bonus prédéfinis
```

Ces fichiers sont facultatifs : si un fichier est absent, le jeu bascule automatiquement sur une génération aléatoire ou une configuration par défaut.

## Dépendances & exécution

1. Créer et activer un environnement virtuel (facultatif).
2. S'assurer que la bibliothèque `fltk` est installée.
3. Lancer le jeu :
   ```bash
   python3 QixRendu3.py
   ```

Le script charge les fichiers présents dans `data/` puis ouvre directement la fenêtre de jeu.

## Problèmes connus / pistes d'amélioration

- Système anti-AFK en mode dessin non implémenté (on peut s'arrêter de bouger sans pénalités).
- Mode 2 joueurs uniquement esquissé.
- Vitesse du joueur fixe : modifier ce paramètre provoque actuellement des soucis de détection des chemins.