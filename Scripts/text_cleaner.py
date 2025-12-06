import re
import spacy

# Cleaning text using Regex
def clean_text(text):
    text = text.lower() # Lowercase conversion
    text = re.sub(r'http\S+|www\S+|https\S+','',text) # URL Removing
    text = re.sub(r'<.*?>','',text) # HTML tag removal
    text = re.sub(r'[^a-z\s]','',text) # Special Character removal
    text = re.sub(r'\s+',' ',text).strip() # Extra Whitespace removal # strip() to remove forward and backword spaces
    text = re.sub(r'\S+@\S+\.\S+','',text) # Email removal
    text = re.sub(r'[^\w\s]','',text) # Punctuation removal
    text = re.sub(r'(.)\1{2,}',r'\1',text) # For Repeated Characters / Elongated words
    text = re.sub(r'#','',text) # Hashtags removal
    text = re.sub(r'@\w+','',text) # Mention Username
    text = re.sub(r'[^\x00-\x7F]+','',text) # Non ASCII characters(emojis, foreign characters)
    return text


# Tokenization & Lemmatization
def lemmatize_spacy(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            word.append(token.lemma_)

    return word