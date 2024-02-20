import nltk
import numpy as np
#nltk.download('punkt')   pre programmed tokenizer in punkt package

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenize(sentence):                     #splitting the sentence and put the words into an array
    return nltk.word_tokenize(sentence)  
  
def stem(word):                            #getting the root word of a word
    return stemmer.stem(word)

def bag_of_words(tokenized_sentence,all_words):   #matching the words in the array with the given user input 
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words),dtype = np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag




