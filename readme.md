# Compte rendu du projet RicoSheep
Projet réalisé en 2022 durant le bloc de L1, Projet2, d'une durée d'un mois et demi. <br>
Par Karim PORCARI, Yassin SEGHDAU et Nathan CHAPELAIN tous trois du TP6.

## Sommaire :
- Manuel utilisateur
- Etat d'avancement du projet
- Organisation du travail
- Conclusion

### Manuel utilisateur
Pour lancer le programme il vous suffit d'executer le fichier ricosheep.py à l'aide de python. <br>
`python ricosheep.py`
Le fichier ricosheep.py ne prend pas d'argument, tout se passe graphiquement ! <br>

Pour ce qui de l'aspect graphique, une fois le programme lancé, vous aurez accès au menu principal. <br>
Dans celui-ci vous trouverez 4 boutons:
- _Setting_ en haut a gauche permettant de changer les paramètres ;
- _Play_ au milieu haut permettant de jouer ;
- _Editor_ en plein millieu permettant d'éditer ou de créer des cartes ;
- _Rules_ au milieu bas permettant de connaitre les règles du jeu.
 
Commencez d'abord par le bouton _Rules_ si c'est la première fois que vous jouez. <br>
Par la suite, je vous invite a consulté/modifié les commandes dans les paramètres. <br>


### Etat d'avancement du projet
Nous avons réalisé l'ensemble des taches **obligatoires** et réalisé certaines des taches complémentaires. <br>
Nous avons fait un choix dans les taches complémentaires de ce qui nous plaisait pour rendre le jeu sympatique. <br>
Vous trouverez donc les ajouts complémentaires suivant :
- Solveur graphique ;
- Recherche d'une solution minimale ;
- Sauvegarde d'une parti en cours ;
- Annuler les derniers coups joués;
- Créer des grilles entièrement aléatoires ;
- Créer des grilles aléatoires avec des paramètres données ;
- Editeur de grille ;
- Raccourcis clavier modifiable dans les paramètres.

Problème avec les évènements touches -> à résoudre avant de rendre

Nous nous sommes permis de modifié fltk pour pouvoir faire des nombreuses choses à savoir :
- Récupérer la taille de la fenetre ;
- Redimensionner la fenetre en temps réel ;
- Redimensionner les images ;
- Créer une fenetre de saisi tkinter ;

Grâce à ses changements, vous pouvez changer la résolution de la fenetre, vous mettre en plein écran, et de nombreuses autres choses.
