# Jeedom plugin skeleton generator
Générateur de squelette de plugin pour Jeedom

## Présentation
Ce script permet de générer un squelette de plugin pour Jeedom avec uniquement les fichiers nécessaires.
## Utilisation
Dans le répertoire plugin de Jeedom (habituellement **/var/www/html/plugins**), lancez la commande suivante : 

```bash
wget https://raw.githubusercontent.com/Sylvaner/JeedomPluginSkeletonGenerator/master/gen.py
chmod +x gen.py
```

ou 

```bash
curl https://raw.githubusercontent.com/Sylvaner/JeedomPluginSkeletonGenerator/master/gen.py > gen.py
chmod +x gen.py
```

Une fois le script téléchargé, vous pouvez le lancer directement : 

```bash
./gen.py
```

Une série de question permettra d'obtenir les informations nécessaires.

## Liste des questions
### Name
Nom qui sera affiché dans les menus de Jeedom.

*Valeur par défaut : The best plugin in the world*

### ID
Identifiant du plugin. Il doit être unique afin de ne pas être confondu avec un autre plugin.

*Valeur par défaut : Nom du plugin sans les espaces en minuscule.*

### Description
Description du plugin afin de le présenter.

*Optionnel*

### Author
Auteur du plugin.

*Optionnel*

### License
Licence sous laquelle le plugin sera fournit.

*Valeur par défaut : GPL (la même que Jeedom)*

### Jeedom required version
Version minimale de Jeedom pour que le plugin fonctionne

*Valeur par défaut : 3.0*

### Plugin category
Catégorie dans laquelle votre plugin sera. Cette liste provient de Jeedom : https://github.com/jeedom/core/blob/beta/core/config/jeedom.config.php

*Numéro à sélectionner dans la liste*

### Documentation language
Langue et encodage de la documentation du plugin.

*Valeur par défaut : en_US*

#### Generate plugin configuration page
Permet de générer les paramètres de configuration du plugin. Deux types peuvent l'être par ce générateur : 

* Texte,
* Case à cocher.

Chaque champ a deux paramètres : 

* Label : Texte affiché à l'utilisateur,
* Code : Identifiant par lequel le plugin pourra retrouver la valeur du champ.

Pour finaliser, il faut sélectionner le troisième choix.

## Sauvegarde
A la fin des questions, il est proposé de sauvegarder les informations demandées. Celle-ci seront stockées dans le fichier **data.json**. Il sera possible par la suite de regénérer le squelette du plugin en entrant la commande 

```bash
./gen.py data.json
```

## Résultat
Un répertoire est créé avec l'identifiant du plugin. Dans celui-ci, différents fichiers ont été créés.
### Arborescence
Pour un plugin dont l'identifiant est *plugin_test* : 

```
+ plugin_test
  - LICENSE
  + 3rdparty
  + core
    + ajax
    + class
      - plugin_test.class.php
    + template
  + desktop
    + css
    + js
    + modal
    + php
      - plugin_test.php
  + docs
  	 + fr_FR
  + plugin_info
    - configuration.php
    - info.json
    - installation.php
    - plugin_test_icon.png
  + ressources    
```
### Description des fichiers
#### LICENCE
Fichier vide où sera contenu les informations de la licence du plugin.
#### plugin\_info/info.json
Informations générales du plugin.
#### plugin\_info/configuration.php
Page de configuration du plugin.
#### plugin\_info/installation.php
Classe appelée à l'installation, la mise à jour ou la suppression du plugin. Les 3 méthodes sont créées.
#### plugin_info/PLUGIN\_ID\_icon.png
Icône du plugin qui sera affiché dans Jeedom.
#### core/class/PLUGIN\_ID.class.php
Fichier principal du plugin.
#### desktop/php/PLUGIN\_ID.php
Fichier gérant l'affichage du plugin.

