import string
import re
import nltk
from configparser import ConfigParser
from nltk.corpus import wordnet
import psycopg2
import spacy
import pyinflect
nlp = spacy.load('en_core_web_sm')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

config = ConfigParser()
config.read('config/config.cfg')

fresnodailynews = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="root",
    database="fresnodailynews"
)

fresnodailynews_cursor = fresnodailynews.cursor()


def get_keyword_synonyms(keyword):
    synonyms = []
    # get synonyms
    syns = wordnet.synsets(keyword)
    for s in syns:
        for lemma in s.lemmas():
            synonyms.append(keyword + ":" + lemma.name())
    print(keyword + " -syn: ")
    print(synonyms)
    return synonyms


def extract_keywords(t):
    t = remove_punctuation_except("'", t)
    t = remove_prepositions_and_articles(t)
    print(t)
    # prepare arrays for keywords
    key_words = []
    # removing punctuation
    key_phrases = t.split(" ")
    print(key_phrases)
    # iterate by keywords
    for key_phrase in key_phrases:
        # skip one-letter words
        if len(key_phrase) > 1:
            key_words.append(key_phrase + ":" + key_phrase)
    # get rid of duplicate keywords
    keywords_set = [*set(key_words)]
    keywords_copy = keywords_set.copy()
    print("keywords_set")
    print(keywords_set)
    synonyms = []
    for k in keywords_copy:
        post_k = k
        if k.find(":") > 0:
            post_k = k[k.find(":") + 1:]
        synonyms = get_keyword_synonyms(post_k) + synonyms
        print("synonyms")
        print(synonyms)
    keywords_set = keywords_set + [*set(synonyms)]
    keywords_set_copy = keywords_set.copy()
    for word in keywords_set_copy:
        pre_word = word
        post_word = word
        if word.find(":") > 0:
            pre_word = word[:word.find(":")]
            post_word = word[word.find(":") + 1:]
        print(post_word)
        if post_word.find("'") > 0:
            print("found")
            post_word = post_word.replace("'", "\\\'")
        print("post_word")
        post_word = re.sub(r'[^A-Za-z\s]', '',  post_word)
        print(post_word)
        fresnodailynews_cursor.execute("SELECT forms FROM verbs where verb =\'" + post_word.lower() + "\'")
        forms = fresnodailynews_cursor.fetchall()
        print("forms")
        print(forms)
        # iterate over the list - forms
        for f in forms:
            # convert tuple to array
           # f_arr = numpy.asarray(f)
            f_arr = list(f)
            for el in f_arr:
                # decode string
                e = el #.decode('utf-8')
                # skip empty values
                if e != '':
                    e = remove_punctuation_except(",", e)
                    e = e.replace('/', ' ')
                    # create array from string
                    e_array = e.split(",")
                    for i in e_array:
                        keywords_set.append(pre_word + ":" + i.strip())
    keywords_set = [*set(keywords_set)]
    result = ','.join(keywords_set)
    result = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", result)
    print(result)
    return result


def remove_punctuation_except(ex, text):
    punctuation = string.punctuation.replace(ex, '')
    result = text.translate(str.maketrans('', '', punctuation))
    return result


def remove_prepositions_and_articles(text):
    pattern = r'\b(?:a|an|the|in|on|at|of|with|to|from|for|by|and|or|' \
              r'under|that|this|these|those|whose|what|how|it|he|she|' \
              r'their|they|our|we|her|his|its|it|was|will|have|has|had|\'s|\'ve|\'d|\'ll|\'m|\'re)\b'
    result = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return result


def get_verb_forms(verb):
    doc = nlp(verb)
    token = doc[0]
    forms = [
        verb,
        token._.inflect('VBD'),
        token._.inflect('VBN'),
        token._.inflect('VBG'),
        token._.inflect('VBZ'),
        token._.inflect('VBP')
    ]
    print(forms)
    return ", ".join(forms)


def get_verbs_start_with(letter):
    print("get_verbs_start_with")
    verbs = []
    for synset in wn.all_synsets('v'):
        print(synset)
        for lemma in synset.lemmas():
            word = lemma.name()
            if word.startswith(letter):
                if '_' in word:
                    word = word.split("_")[0]
                verbs.append(word)
    verb = ", ".join(list(set(verbs)))
    print(verb)
    return verb
