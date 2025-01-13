
from typing import List, Dict, Tuple
from Levenshtein import distance as levenshtein_distance
from difflib import SequenceMatcher
import re

def levenshtein_similarity(word1: str, word2: str) -> float:
    """
    Calcule la similarité basée sur la distance de Levenshtein
    Adaptée pour les fautes de frappe et substitutions
    """
    word1, word2 = word1.lower(), word2.lower()
    max_len = max(len(word1), len(word2))
    if max_len == 0:
        return 0
    distance = levenshtein_distance(word1, word2)
    return 1 - (distance / max_len)

def sequence_similarity(word1: str, word2: str) -> float:
    """
    Calcule la similarité de séquence
    Meilleure pour détecter les parties communes
    """
    return SequenceMatcher(None, word1.lower(), word2.lower()).ratio()

def phonetic_similarity(word1: str, word2: str) -> float:
    """
    Calcule une similarité phonétique simple
    Utile pour les erreurs phonétiques courantes
    """
    # Dictionnaire de remplacement pour les sons similaires
    replacements = {
        'a': 'a', 'e': 'a', 'é': 'a', 'è': 'a', 'ê': 'a',
        'i': 'i', 'y': 'i',
        'o': 'o', 'u': 'o',
        'k': 'q', 'c': 'q',
        'z': 's',
        'f': 'v',
        'b': 'p',
        't': 'd',
        'n': 'm'
    }

    # Simplifie les mots en remplaçant les caractères similaires
    def simplify(word: str) -> str:
        return ''.join(replacements.get(c, c) for c in word.lower())

    simple1 = simplify(word1)
    simple2 = simplify(word2)
    return sequence_similarity(simple1, simple2)

def calculate_brand_similarity(word: str, brand: str) -> Dict:
    """
    Calcule tous les scores de similarité entre un mot et une marque
    """
    lev_score = levenshtein_similarity(word, brand)
    seq_score = sequence_similarity(word, brand)
    phon_score = phonetic_similarity(word, brand)

    # Score composite (moyenne des trois scores)
    composite_score = (lev_score + seq_score + phon_score) / 3

    return {
        'found_word': word,
        'matched_brand': brand,
        'composite_score': round(composite_score, 3),
        'details': {
            'levenshtein_score': round(lev_score, 3),
            'sequence_score': round(seq_score, 3),
            'phonetic_score': round(phon_score, 3)
        }
    }

def find_similar_brands(text: str, brands: List[str], threshold: float = 0.7) -> List[Dict]:
    """
    Trouve toutes les marques similaires dans un texte

    Args:
        text: Texte à analyser
        brands: Liste des marques correctes
        threshold: Seuil minimum de similarité (0-1)
    """
    words = text.lower().split()
    matches = []

    for word in words:
        for brand in brands:
            similarity = calculate_brand_similarity(word, brand)
            if similarity['composite_score'] >= threshold:
                matches.append(similarity)

    return sorted(matches, key=lambda x: x['composite_score'], reverse=True)

def correct_brand_names(text: str, brands: List[str], threshold: float = 0.7) -> Tuple[str, List[Dict]]:
    """
    Corrige les noms de marques dans un texte

    Returns:
        (texte_corrigé, liste_corrections)
    """
    words = text.split()
    corrections = []

    for i, word in enumerate(words):
        matches = find_similar_brands(word, brands, threshold)
        if matches:
            best_match = matches[0]
            if best_match['composite_score'] >= threshold:
                original = words[i]
                words[i] = best_match['matched_brand']
                corrections.append({
                    'original': original,
                    'corrected': best_match['matched_brand'],
                    'position': i,
                    'scores': best_match
                })

    return ' '.join(words), corrections

"""# Extraction des données

## Reads a CSV file and converts it into a list of lists, where each inner list represents a row.
"""

import csv

def csv_to_list(file_path: str) -> list:
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)
      return data
  except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

"""## Reads a CSV file and returns a list of the first column's values."""

import csv

def get_first_column(file_path):
  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      reader = csv.reader(file)
      first_column_data = [row[0] for row in reader]  # Extract the first element of each row
      return first_column_data
  except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    return None
  except IndexError:
    print("Error: Some rows might be empty in the CSV file.")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

"""## Download"""

spam_words = {
        "gratuit": 0.8,
        "argent": 0.7,
        "gagner": 0.9,
        "loterie": 0.85,
        "urgent": 0.75,
        "offre": 0.7,
        "promotion": 0.65,
        "gagnant": 0.8,
        "prix": 0.7,
        "crédit": 0.7,
        "casino": 0.9,
        "félicitations": 0.8,
        "mbrok":0.8,
        "gagné": 0.8,
        "free": 0.8,
        "money": 0.7,
        "win": 0.9,
        "lottery": 0.85,
        "urgent": 0.75,
        "offer": 0.7,
        "promotion": 0.65,
        "winner": 0.8,
        "prize": 0.7,
        "credit": 0.7,
        "casino": 0.9 ,
        "congratulations": 0.8,
        "won":0.8,
        "r7bti": 0.9,
        "rebe7ti":0.9,
        "ma7dod": 0.8,
        "hemza":0.7,
        "l3ard": 0.75,
        "fa2izin":0.8,
        "fa2iz":0.8,
        "fabor":0.9,
         "chance":0.7,
        "dkhol":0.6,
        "lien":0.6

}

"""#Filtring

## Spam filtring
"""

def detecter_lien(tweet):
    pattern = r"(https?://[^\s]+|www\.[^\s]+)"
    return re.findall(pattern, tweet)

def spam_analysis(phrases, spam_dict):
    positive_spam = []
    neutral_phrases = []

    for phrase in phrases:
        matches = find_similar_brands(phrase, spam_dict, threshold=0.7)
        matched_words = [match['matched_brand'] for match in matches]

        if matched_words:
            score_sum = sum(spam_dict[word] for word in matched_words)
            if detecter_lien(phrase)!=[]:score_sum+=0.5
            if score_sum > 1:
                  positive_spam.append((phrase, score_sum))

        else:neutral_phrases.append(phrase)

    return positive_spam , neutral_phrases

"""## filring on brand"""

def filterbrand(l,brands):
  v=[]
  nv=[]
  for i in l:
    matches = find_similar_brands(i[0], [brands], threshold=0.7)
    l1=[]
    for match in matches:
      l1.append(match['matched_brand'])
    if brands in l1:
      v.append(i)
    else:
      nv.append(i)
  return v,nv

"""# filtring on features"""

def filterproduit(l,qualité,prix):
  lq=[]
  lp=[]
  lr=[]
  for i in l:
    matchesquality = find_similar_brands(i[0], qualité, threshold=0.7)
    matchesprix = find_similar_brands(i[0], prix, threshold=0.8)
    l1=[]
    l2=[]
    for match in matchesquality:
      l1.append(match['matched_brand'])
    if l1!=[]:
      lq.append(i)
    for match in matchesprix:
      l2.append(match['matched_brand'])
    if l2!=[]:
      lp.append(i)
    if l1==[]and l2==[]: lr.append(i)
  return lq,lp,lr

qualité=["qualité, quality, kalité","jawda","ljawda","lqualité","lqualiti"]

prix=['taman','price',"pri","lprix","prix",'flous','derham','dh','dhs','dirham','ghali','rkhis']

"""# sentiment analysis"""

sentiment_positif = {
    "3jbni": 0.7, "7bit": 0.9, "7ebit": 0.7, "nadi": 0.8, "zwin": 0.7,"zouin":0.7,"zine":0.7,"mo3tabar":0.8,"fri3":0.8,"rfi3":0.8,"fr7an":0.6,"lkhr":0.8,"ra2i3":0.8,"modhil":0.8,"ani9":0.6,"sa3id":0.7,
    "wa3r": 8.0,"Zaynab":100, "naadia": 0.7, "mfrge3a": 8.0, "ghzal": 1.0 , "makhaybch": 0.4 ,"nadiya":0.8, "nadia":0.8 , "mana9ssach":0.4,"matay7ach":0.4,"herban":0.8,"kay7eme9":0.8,'kay7m9ni':0.8, "jdida":0.4,"fniwn":5
}

sentiment_negatif = {
    "ma3jbnich": -0.7, "ma7ebitch": -0.9, "khayb": -7.0, "na9ess": -0.7,"ma7ebitouch":-0.6,
    "7amed": -0.6, "fachel": -1.0, "probleme": -0.8, "mochkil": -0.9,
    "khasr": -0.7, "habta": -0.8, "ma7meltoch": -0.9 ,"tay7a" : -0.7 , "mazwinch" :-0.6,"mazouinch":-0.6 , "manadiyach":-0.6,"manadiach":-0.6,"mawa3rach":-0.4, "3iyan":-0.7,"frya":-0.7,"9dim":0.4
}

datapositif ={'bogos': 0.5,
 'jdid': 0.1363636363636363,
 'nachT': 0.8,
 'n9i': 0.3666666666666667,
 'fr7an': 0.5,
  'fakhour': 0.8,
 'raDi': 0.5,
 'mrta7': 0.4,
 'Drief': 0.2,
 'dki': 0.8,
 'ijabi': 0.2272727272727272,
 'waa9i3i': 0.1666666666666666,
 'ra2isi': 0.0625,
 'm2kked': 0.2142857142857142,
 'Si77i': 0.5,
 'ml7ouD': 0.5,
 'mota2lli9': 0.9,
 'mofDDal': 0.5,
 'tay9': 0.5,
 'mtnas9': 0.5,
 'fo9 l3ada': 0.3333333333333333,
 'khari9 lil3ada': 0.3333333333333333,
 'waD7': 0.25,
 'momti3': 0.5,
 'mobdi3': 0.5,
 'mobaachir': 0.375,
 'mtfowwe9': 0.7,
 '2aamin': 0.4,
 'raa9i': 0.5,
 'si7ri': 0.5,
 'kayD77ek': 0.3,
 'fnni': 0.3333333333333333,
 'Tamou7': 0.25,
 'fchkel': 0.5,
 'gharib': 0.5,
 'automatic': 0.4,
 'bnin': 1.0,
 'kayfrre7': 1.0,
 'tlkhdma': 0.3,
 'takhayyoli': 0.6,
 '3ajib': 0.4,
 'mobtakar': 0.5,
 'aSli': 0.5,
 'moD7ik': 0.25,
 'komidi': 0.25,
 'm9boul': 0.5,
 'wa3r': 0.5,
 'laa2i9': 0.1666666666666666,
 'jbbar': 0.4,
 'ldid': 1.0}
 

datanegatif={'DaSr': -0.15,
 'modmin': -0.4,
 'ghabyy': -0.7999999999999999,
 'mkllkh': -0.7999999999999999,
 'mjllj': -0.7999999999999999,
 'momill': -0.2916666666666667,
 'khayb': -0.6999999999999998,
 'mSTTi': -0.6,
 'S3ib': -0.2,
 '9as7': -0.2,
 'm3TTl': -0.3,
 'm399d': -0.3,
 't9il': -0.2,
 '7azin': -0.5,
 'mchoki': -0.7,
 'mrwwn': -0.4,
 '3yyan': -0.4,
 '3abiT': -0.5,
 'silbi': -0.3,
 'tay3yyef': -1.0,
 'ghali': -0.5,
 'khaT2': -0.4000000000000001,
 'myyet': -0.2,
 'mDllem': -0.15,
 'bard': -0.6,
 'm2louf': -0.25,
 'khawi': -0.1,
 'mDyye9': -0.2,
 '9aaser': -0.05,
 'mriD': -0.7142857142857143,
 'fchkel': -0.1666666666666666,
 'D3if': -0.5,
 'kaykhle3': -1.0,
 '9lil': -0.1666666666666666,
 'b3id': -0.1,
 '3anif': -0.8,
 'mossekh': -0.6,
 'mrkhi': -0.0769230769230769,
 'fa9d l2amal': -0.6,
 'ghayr 9anoni': -0.5,
 '3chwa2i': -0.5,
 'mzyyer': -0.1785714285714285,
 'mSTane3': -0.6,
 'mo2lim': -0.7,
 'm9lle9': -0.6,
 'maDarorich': -0.4,
 'mabaynch': -0.3333333333333333,
 'kay3yyef': -1.0,
 'mo7rij': -0.6,
 'm3nfj': -0.5,
 'mamori7ch': -0.5,
 'mamofri7ch': -0.6499999999999999,
 '8aawi': -0.25,
 'm2sawi': -0.75,
 'mofji3': -0.75,
 'kaariti': -0.7,
 'gharib': -0.5,
 'mam2ddebch': -0.3,
 'mamrbbich': -0.3,
 'ka2ib': -1.0,
 'kay9tel': -0.2,
 '9bi7': -1.0,
 'ghaleT': -0.5}

def merge_dicts(dict1, dict2):
  merged = dict1.copy()
  merged.update(dict2)
  return merged

bigdatapositif=merge_dicts(datapositif, sentiment_positif)
bigdatanegatif=merge_dicts(datanegatif, sentiment_negatif)

negate_words = ["machi", "machy", "mchi", "mashi", "maxi","mechi","mechy"]
    # Mots qui annulent l'effet de négation quand ils suivent machi
cancel_negation_words = ["ghir","ghr",'gha', "ghire","ghere","ghi", "ghyr", "gher"]

intensifiers = {
        "bzf": 1.5, "bzaf": 1.5, "bzaaf": 1.5, "bzef": 1.5, "bezaf": 1.5,
        "bazaf": 1.5, "bzff": 1.5, "ktir": 1.3, "keteer": 1.3,
        "chwiya": 0.7, "chwia": 0.7, "chouia": 0.7, "choia": 0.7,
        "kamel": 1.4, "bla9iyass": 1.6, "bela9ias": 1.6, "mout": 1.8, "moot": 1.8
            }

def sentiment_analysis8(l, sentimentpositif, sentimentnegatif):
    """
    Analyse les sentiments dans des textes darija avec gestion des inversions, fautes d'orthographe,
    et intensificateurs. Gestion spéciale de 'machi ghir'.
    """
    lq = []  # Liste pour les tweets positifs
    lp = []  # Liste pour les tweets négatifs
    lr = []  # Liste pour les tweets neutres




    def is_negated(word_index, words):
        """
        Vérifie si un mot est sous l'influence d'une négation.
        Prend en compte le cas spécial où 'machi' est suivi par 'ghir' ou ses variantes.
        """
        for i in range(max(0, word_index - 3), word_index):
            if words[i] in negate_words:
                # Vérifier si le mot suivant la négation est un mot qui annule l'effet
                next_idx = i + 1
                if next_idx < len(words):
                    # Chercher des correspondances approximatives pour les mots qui annulent
                    cancel_matches = find_similar_brands(words[next_idx],
                                                       cancel_negation_words,
                                                       threshold=0.7)
                    if cancel_matches:
                        # Si on trouve un mot qui annule, on ignore cette négation
                        continue
                return True
        return False

    def get_intensifier_multiplier(words, sentiment_index):
        """
        Calcule le multiplicateur d'intensité en cherchant les intensificateurs après le mot de sentiment.
        """
        multiplier = 1.0
        # Chercher dans les 2 mots suivant le mot de sentiment
        for i in range(sentiment_index + 1, min(sentiment_index + 3, len(words))):
            matches = find_similar_brands(words[i], list(intensifiers.keys()), threshold=0.7)
            if matches:
                matched_intensifier = matches[0]['matched_brand']
                multiplier *= intensifiers[matched_intensifier]
        return multiplier

    for text in l:
        if not text.strip():  # Ignorer les textes vides
            continue

        words = text.split()
        score = 0

        # Parcourir chaque mot
        for word_index, word in enumerate(words):
            # Vérifier la négation
            is_neg = is_negated(word_index, words)

            # Vérifier les sentiments positifs
            matches_pos = find_similar_brands(word, list(sentimentpositif.keys()), threshold=0.7)
            for match in matches_pos:
                matched_word = match['matched_brand']
                # Obtenir le multiplicateur en vérifiant les mots qui suivent
                multiplier = get_intensifier_multiplier(words, word_index)
                word_score = sentimentpositif[matched_word] * multiplier
                score += -word_score if is_neg else word_score

            # Vérifier les sentiments négatifs
            matches_neg = find_similar_brands(word, list(sentimentnegatif.keys()), threshold=0.8)
            for match in matches_neg:
                matched_word = match['matched_brand']
                # Obtenir le multiplicateur en vérifiant les mots qui suivent
                multiplier = get_intensifier_multiplier(words, word_index)
                word_score = sentimentnegatif[matched_word] * multiplier
                score += -word_score if is_neg else word_score

        # Classification selon le score
        if score > 0:
            lq.append((text, score))
        elif score < 0:
            lp.append((text, score))
        else:
            lr.append((text, score))

    return lq, lp, lr

def ratio(p,n,r):
  somme=len(p)+len(n)+len(r)
  return len(p)/somme,len(n)/somme,len(r)/somme

def calul_moyen_scores(data):
    # Remplace les scores > 1 par 1
    scores_ajustes = [min(score, 1) for _, score in data]

    # Calcul de la moyenne des scores ajustés
    moyenne = sum(scores_ajustes) / len(scores_ajustes) if scores_ajustes else 0

    return moyenne

"""# Exemple"""



def sentiment_analysis_darija(sentences):
  return sentiment_analysis8(sentences,bigdatapositif,bigdatanegatif)