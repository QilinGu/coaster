import re
import enchant
import requests
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem.snowball import SnowballStemmer


tokenizer = WhitespaceTokenizer()
stemmer = SnowballStemmer("english")

english_dict = enchant.Dict("en_US")
english_contractions = {
    "ain't"       : ["am not"],
    "aren't"      : ["are not"],
    "can't"	      : ["cannot"],
    "could've"	  : ["could have"],
    "couldn't"	  : ["could not"],
    "couldn't've" :	["could not have"],
    "didn't"      : ["did not"],
    "doesn't"	  : ["does not"],
    "don't"	      : ["do not"],
    "hadn't"      : ["had not"],
    "hadn't've"   : ["had not have"],
    "hasn't"      : ["has not"],
    "haven't"	  : ["have not"],
    "he'd"	      : ["he had", "he would"],
    "he'd've"	  : ["he would have"],
    "he'll"	      : ["he shall", "he will"],
    "he's"	      : ["he has", "he is"],
    "how'd"	      : ["how did", "how would"],
    "how'll"	  : ["how will"],
    "how's"	      : ["how has", "how is", "how does"],
    "I'd"	      : ["I had", "I would"],
    "I'd've"	  : ["I would have"],
    "I'll"	      : ["I shall", "I will"],
    "I'm"	      : ["I am"],
    "I've"	      : ["I have"],
    "isn't"	      : ["is not"],
    "it'd"	      : ["it had", "it would"],
    "it'd've"	  : ["it would have"],
    "it'll"	      : ["it shall", "it will"],
    "it's"	      : ["it has", "it is"],
    "let's"	      : ["let us"],
    "ma'am"	      : ["madam"],
    "mightn't"	  : ["might not"],
    "mightn't've" : ["might not have"],
    "might've"	  : ["might have"],
    "mustn't"	  : ["must not"],
    "must've"	  : ["must have"],
    "needn't"	  : ["need not"],
    "not've"	  : ["not have"],
    "o'clock"	  : ["of the clock"],
    "oughtn't" 	  : ["ought not"],
    "'ow's'at"	  : ["how is that"],
    "shan't"	  : ["shall not"],
    "she'd"	      : ["she had", "she would"],
    "she'd've" 	  : ["she would have"],
    "she'll"	  : ["she shall", "she will"],
    "she's"	      : ["she has", "she is"],
    "should've"	  : ["should have"],
    "shouldn't"	  : ["should not"],
    "shouldn't've": ["should not have"],
    "that'll"	  : ["that will"],
    "that's"	  : ["that has", "that is"],
    "there'd"	  : ["there had", "there would"],
    "there'd've"  : ["there would have"],
    "there're"	  : ["there are"],
    "there's"	  : ["there has", "there is"],
    "they'd"	  : ["they had", "they would"],
    "they'd've"	  : ["they would have"],
    "they'll"	  : ["they shall", "they will"],
    "they're"	  : ["they are"],
    "they've"	  : ["they have"],
    "wasn't"	  : ["was not"],
    "we'd"	      : ["we had", "we would"],
    "we'd've"	  : ["we would have"],
    "we'll"	      : ["we will"],
    "we're"	      : ["we are"],
    "we've"	      : ["we have"],
    "weren't"	  : ["were not"],
    "what'll"	  : ["what shall", "what will"],
    "what're"	  : ["what are"],
    "what's"	  : ["what has", "what is", "what does"],
    "what've"	  : ["what have"],
    "when's"	  : ["when has", "when is"],
    "where'd"	  : ["where did"],
    "where's"	  : ["where has", "where is"],
    "where've" 	  : ["where have"],
    "who'd"	      : ["who would", "who had"],
    "who'd've" 	  : ["who would have"],
    "who'll"	  : ["who shall", "who will"],
    "who're"	  : ["who are"],
    "who's"	      : ["who has", "who is"],
    "who've"	  : ["who have"],
    "why'll"	  : ["why will"],
    "why're"	  : ["why are"],
    "why's"	      : ["why has", "why is"],
    "won't"	      : ["will not"],
    "would've"	  : ["would have"],
    "wouldn't"	  : ["would not"],
    "wouldn't've" : ["would not have"],
    "y'all"       : ["you all"],
    "y'all'd've"  : ["you all should have", "you all could have", "you all would have"],
    "you'd"       : ["you had", "you would"],
    "you'd've"	  : ["you would have"],
    "you'll"	  : ["you shall", "you will"],
    "you're"	  : ["you are"],
    "you've" 	  : ["you have"],
}


def normalize_token(token):
    token = stemmer.stem(token)
    return remove_needless_punctuation(token).strip()


def remove_needless_punctuation(text):
    '''
    Remove punctuation that indicates pauses, as well
    as parentheses, brackets, etc.
    '''
    return re.sub(ur"[,.;:!\?\[\]\(\)\{\}<>]+", '', text)


def is_valid_term(term):
    return in_english_dictionary(term) or in_wikipedia(term)


def in_english_dictionary(term):
    return english_dict.check(term)


def in_wikipedia(term):
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s" \
        % term

    r = requests.get(url).json()
    return '-1' not in r['query']['pages'].keys()
