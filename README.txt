Projet Qix - Jules/Khephren

	TOUCHES:
Haut		-Flèche haut
Bas		-Flèche bas
Gauche		-Flèche Gauche
Droite		-Flèche Droite
Mode Dessin	-Espace
Fermer		-Echap

-----------------------------------------

Organisation du code:

Importation : 
fltk *
time(sleep,time)
random(randint,choice)
matplotlib (NON UTILISE, IMPORTE POUR DES TESTS)

Variables :
il y en a beaucoup, mais elles sont réunies en blocs:

la fenetre et la zone de jeu
le joueur (vie, déplacements, vitesse...)
les chemins
la surface
le Qix
les Sparx
les obstacles
autres(invincibilite,menu...)

Création de la fenetre et de la zone de jeu

Fonctions :
AfficheLife() 		Affiche la vie en haut de l'écran
perdu()			Affiche un écran de défaite
gagne()			Affiche un écran de victoire
lvlup()			Affiche un écran de montée de niveau
bouton()		Affiche les boutons du menu
menu()			Affiche le menu
Obstacle()		Affiche les obstacles
SetObstacleMode()	Vérifie la présence d'un fichier d'obstacles
ReadObstacleFile()	Lie le fichier d'obstacles et en renvoie la liste des obstacles
InChemin()  		Vérifie l'appartenance de coordonnées xy à une liste de chemins
DecrypteChemin()	Le rendu de InChemin est différent du format de la liste des chemins, cette fonction change cela
direction()  		Regarde les touches préssées par le joueur
Invert_direction()	renvoie la direction inverse à celle mise en paramètre
ActivateDrawMode() 	Regarde le pressage de la touche espace
AfficheLignes()		Affiche une liste de lignes (ex: chemins, tracé du joueur...)
AfficheZone()		Affiche chaque polygone selon une liste de polygones
testalldirect()		Test toutes les directions possibles sur les chemins
testalldirect_oldchemins() Pareil, sur les anciens chemins (pour les Sparx sortis du chemin)
Ini_Mat()		Initialise une matrice de la taille définie par les paramètres
AfficheMat()		(utilisé pour les tests) - Affiche le contenu d'une matrice de manière propre
diviseLigne()		Sépare un chemin en 2 et renvoie les 2 nouveaux chemins
diviseLigne3()		Sépare un chemin en 3 et renvoie les 3 nouveaux chemins
AdaptChemin()		Utilise les diviseLigne pour adapter le chemin apres la prise d'une zone
ray_tracing()		Vérifie l'appartenance d'un point à un polygone via une méthode de ray tracing
retire_doublons()	retire les doublons d'une liste
AdaptZone() 		Utilise le ray_tracing et Adapt_chemin pour s'occuper de tout ce qu'il faut faire lors de la capture de zone
Qix()			Affiche le Qix par rapport à ses coordonnées et sa taille
Sparx()			Affiche le Sparx par rapport à ses coordonnées et sa taille
Respawn()		Renvoie les coordonnées du centre d'un chemin existant aléatoire pour faire réaparraitre le joueur
Aire_Polygone()		Renvoie la surface d'un polygone
Creer_bonus()		Crée une liste de bonus aléatoirements placés sur la zone de jeu
SetBonusMode()		Vérifie la présence d'un fichier de bonus
ReadBonusFile()		Lie le fichier de bonus et en renvoie la liste des bonus
Affiche_bonus()		Affiche l'ensemble des bonus de la liste en paramètre
mange_bonus()		vérifie si un joueur mange un bonus et le retire de la liste si oui
SetConfigMode()		Vérifie la présence d'un fichier de configuration initiale
ReadConfigFile()	Lie le fichier de configuration et change les différentes variables concernées (taille et vitesse initiales du Qix, nombre initial de Sparxs et taille de la zone de jeu.


Boucle Menu :
Permet de choisir le mode de jeu (2 joueurs non implémenté), les variantes (obstacles, bonus, config) ou quitter le jeu

Change les paramètres initiales selon le fichier config (si choisi)
Crée les obstacles (aléatoirement ou selon le fichier obstacle) (si choisi)
Crée les sparx selon le nombre
Crée les bonus (aléatoirement ou selon le fichier bonus) (si choisi)

Boucle Principale :
Vérification de condition de victoire/passage au niveau supèrieur 
(3 niveaux augmentant en difficulté : + de sparx, Qix plus gros et plus rapide)

effacage et réaffichage de chaque élément (zone de jeu, chemins, vie, joueur, surface, Qix...)

Passage du mode chemin au mode dessin et inversement
--(si le joueur était en mode dessin à la dernière boucle et touche un chemin il repasse en mode chemin)
--Calcul de la zone capturé selon l'emplacement du Qix

Gestion des déplacements, de l'affichage et s'assurer que le joueur reste dans le chemin en mode chemin

Gestion des déplacements et de l'affichage du joueur en mode dessin
--contient la vérification en cas de croisement de son dessin (-1vie, respawn ou fin si vie à 0)

Gestion du Qix
--déplacement aléatoire
--empeche de passer outre un chemin
--détecte la collision avec le dessin et conséquences(-1vie, respawn ou fin si vie à 0)

Gestion des Sparx
--déplacements sur les chemins
--si plus sur un chemin, continue sur les anciens chemins jusqu'à retrouver le chemin principal
--détecte la collision avec le jouer et conséquences(-1vie, respawn ou fin si vie à 0)

Obstacles
--bloquent le joueur

Bonus
--Si mangé, rends le joueur invicible: ignore les sparx, et pas de vie retirée si collision avec le Qix pendant quelques secondes.

Empeche le joueur de sortir des limites de la zone de jeu

Fermeture de la fenetre si touche Echap pressée.

-----------------------------------------

Problèmes rencontrés :
-Pas encore implémenté "l'anti-afk"
 (qui apparait lorsqu'on est trop longtemps immobile en mode dessin)
-Pas encore implémenté le monde 2 joueurs
-Pas de changement de vitesse du joueur (pose des problèmes de détection des chemins)
-problème lors de la création d'un nombre trop conséquent de zones (ralentissement du jeu)
-problème lors de la création d'une zone sans sortir du chemin (crée une "fausse zone" qui pose ensuite problème dans les calculs de zone



