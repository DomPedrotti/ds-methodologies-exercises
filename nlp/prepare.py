import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def pre_prep(unclean_str):
    clean_str = unclean_str.lower()
    clean_str = re.sub(r'[\s]+', ' ', clean_str)
    clean_str = clean_str.strip()
    return clean_str

def remove_non_ascii(unclean_str):  
    clean_str =     unicodedata.normalize('NFKD', unclean_str)\
                        .encode('ascii', 'ignore')\
                        .decode('utf-8', 'ignore')
    return clean_str

def remove_special_characters(unclean_str):
    clean_str = re.sub(r"[^a-z'\s]", '', unclean_str)
    return clean_str

def tokenize(unclean_str):
    tokenizer = ToktokTokenizer()
    clean_str = tokenizer.tokenize(unclean_str, return_str=True)
    return clean_str

def lemmatize(unclean_str):
    wn1 = nltk.stem.WordNetLemmatizer()
    clean_str = ' '.join([wn1.lemmatize(word) for word in unclean_str.split()])
    return clean_str

def stem(unclean_str):
    ps = nltk.porter.PorterStemmer()
    clean_str = ' '.join([ps.stem(word) for word in unclean_str.split()])
    return clean_str

def remove_stopwords(unclean_str, extra_words = [], exclude_words = []):
    sw_list = stopwords.words('english')
    for add_word in extra_words:
        sw_list.append(add_word)
    for rm_word in exclude_words:
        sw_list.remove(rm_word)
    unclean_str = tokenize(unclean_str).split()
    clean_str = ' '.join([word for word in unclean_str if word not in sw_list])
    return clean_str

def basic_clean(df, stem_or_lem = 'lemmatize'):
    for col in df:
        df[col] = df[col].apply(pre_prep)
        df[col] = df[col].apply(remove_non_ascii) 
        df[col] = df[col].apply(remove_special_characters) 
        df[col] = df[col].apply(tokenize)
        if stem_or_lem == 'lemmatize':
            df[col] = df[col].apply(lemmatize)
        elif stem_or_lem == 'stem':
            df[col] = df[col].apply(stem)
        df[col] = df[col].apply(remove_stopwords)
    return df


