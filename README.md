
# SentimentAnalysisDarijaNZ
=======
# Mabibliotheque

**Mabibliotheque** est une bibliothèque Python modulaire qui fournit des outils pour le calcul de similarité, le filtrage de données, et l'analyse de sentiments. Elle est conçue pour traiter des textes en langue Darija (ou d'autres langues) en utilisant des techniques avancées de traitement de texte.

## Fonctionnalités

- **Module `similarity`** :
  - Calcul de la similarité entre deux mots à l'aide de différentes méthodes (Levenshtein, séquence, phonétique).
  
- **Module `filtering`** :
  - Filtrage des textes en fonction de mots-clés et de seuils de similarité.
  - Filtrage basé sur des marques ou des caractéristiques spécifiques.

- **Module `sentiment`** :
  - Analyse des sentiments positifs, négatifs et neutres dans des phrases.
  - Gestion des intensificateurs et des mots de négation.

- **Module `utils`** :
  - Chargement de fichiers CSV et extraction des colonnes.

## Installation

Pour installer cette bibliothèque, vous devez d'abord la télécharger ou la cloner depuis son dépôt GitHub. Ensuite, vous pouvez l'installer en mode développement ou la rendre accessible via `pip`.

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Benhamdane/SentimentAnalysisDarijaNZ.git
   cd mabibliotheque
   ```

2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Voici des exemples d'utilisation des modules principaux :

### 1. Calcul de similarité
```python
from mabibliotheque.similarity import levenshtein_similarity, sequence_similarity

word1 = "hello"
word2 = "helo"
similarity = levenshtein_similarity(word1, word2)
print(f"Levenshtein Similarity: {similarity}")
```

### 2. Filtrage de données
```python
from mabibliotheque.filtering import find_similar_brands

text = "This is a test sentence for brand filtering."
brands = ["brand1", "test", "filter"]
matches = find_similar_brands(text, brands)
print(matches)
```

### 3. Analyse de sentiments
```python
from mabibliotheque.sentiment import sentiment_analysis8

sentences = ["Cette phrase est super !", "Je n'aime pas ça."]
positive, negative, neutral = sentiment_analysis8(sentences, bigdatapositif, bigdatanegatif)
print(f"Positifs: {positive}, Négatifs: {negative}, Neutres: {neutral}")
```

### 4. Utilitaires
```python
from mabibliotheque.utils import csv_to_list

data = csv_to_list("path/to/your/file.csv")
print(data)
```

## Tests

Vous pouvez exécuter les tests unitaires pour vérifier que tout fonctionne correctement :
```bash
pytest tests/
```

## Contribuer

Les contributions sont les bienvenues ! Suivez ces étapes pour contribuer :

1. Forkez le dépôt.
2. Créez une branche pour votre fonctionnalité ou correction de bug :
   ```bash
   git checkout -b feature/nom-fonctionnalite
   ```
3. Faites vos modifications et commitez-les :
   ```bash
   git commit -m "Description de votre changement"
   ```
4. Poussez vos changements et soumettez une Pull Request.

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier `LICENSE` pour plus d'informations.

## Auteur
  **Nawfal BENHAMDANE**  
  - Elève-Ingénieur à l'Ecole Centrale Casablanca
  
- **Zaynab RAOUNAK**  
   - Elève-Ingénieur à l'Ecole Centrale Casablanca

