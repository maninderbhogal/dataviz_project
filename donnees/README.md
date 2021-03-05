# Scripts de données

## Environnement de développement

Vous pouvez utiliser soit `Nix` ou `virtualenv` de Python pour installer les dépendances du projet.

### Nix

Cette méthode fonctionne avec les systèmes GNU+Linux (et Mac théoriquement).

Installez `Nix` avec:

```
curl -L https://nixos.org/nix/install | sh
```

Par la suite, lancez `nix-shell` pour entrer dans l'environnement de développement.
Cet environnement s'assure qu'on travaille tous avec la même version de Python, les bonnes librairies Python, et les mêmes libraires dans le système d'exploitation.

### Virtualenv

En alternative à `Nix`, vous pouvez utiliser `virtualenv` pour installer les dépendances Python.

Tout d'abord, assurez-vous d'avoir une version de Python >= 3.6. Par la suite, dans le dossier courrant, lancez:

```
$ python -m venv .venv
$ source .venv/bin/activation
$ pip install -r requirements
```

## Génération de jeux de données

Dans ce dossier, vous trouverez plusieurs scripts Python qui génère des jeux de données selon les données RDF de la Cinémathèque québécoise et de Wikidata.

Simplement exécuter chaque script pour générer le jeu de données.
