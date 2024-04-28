import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from autocorrect import Speller
import contractions

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def lowercase(text):
    return text.lower()

def tokenize(text):
    return word_tokenize(text)

def remove_punctuation(tokens):
    return [token for token in tokens if token not in string.punctuation]

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def remove_special_characters(tokens):
    return [re.sub('[^A-Za-z]+', '', token) for token in tokens]

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, wordnet.VERB) for token in tokens]

def spell_check(tokens):
    spell = Speller(lang='en')
    return [spell(token) for token in tokens]

def preprocess_text(text):

    # Lowercasing
    text = lowercase(text)
    print("after lowering :", text)
    

    # Expansion of contractions
    expanded_words = []    
    for word in text.split():
        expanded_words.append(contractions.fix(word))   
    
    expanded_text = ' '.join(expanded_words)
    
    print("after removing contraction: ", expanded_text)


    # Tokenization
    tokens = tokenize(expanded_text)
    print("after tokenization : ", tokens)


    # Removing Punctuation
    tokens = remove_punctuation(tokens)
    print("after removing puncuation : ", tokens)


    # Removing Stopwords
    tokens = remove_stopwords(tokens)
    print("after removing stopword : ", tokens)
    

    # Removing Special Characters and Numbers
    tokens = remove_special_characters(tokens)
    print("after removing special char and num : ", tokens)
    

    # Lemmatization
    tokens = lemmatize(tokens)
    print("after lemetizing : ", tokens)
    
    # Spell Checking
    tokens = spell_check(tokens)
    print("after spell cheacking : ", tokens)
    
    # Joining the tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

