
from keras.models import load_model
import pickle
from transformers import AutoTokenizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import nltk
import re
import os

nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.stem.porter import *


current_path =os.path.dirname(os.path.abspath(__file__))

###Spam Massage
#tokenizer load
#Spam_tokenizer_pickle_file = "/content/drive/MyDrive/Work_space/Project/Cyber/API/app/service01/service01_model/Spam_massage_detection/tokenizer_spam.pickle"
Spam_tokenizer_pickle_file =os.path.join(current_path,"service01_model/Spam_massage_detectionhdf5/tokenizer_spam.pickle")

with open(Spam_tokenizer_pickle_file, 'rb') as f:
  tokenizer_spam = pickle.load(f)

# Load model
#model_spam_class = load_model('/content/drive/MyDrive/Work_space/Project/Cyber/API/app/service01/service01_model/Spam_massage_detection/spam_massage.keras')
model_spam_path = os.path.join(current_path, "service01_model/Spam_massage_detectionhdf5/spam_massage.hdf5")
model_spam_class = load_model(model_spam_path)

def pre_text(tweet):
    ''' Convert tweet text into a sequence of words '''

    # convert to lowercase
    text = tweet.lower()
    # remove non letters
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    # tokenize
    words = text.split()
    # remove stopwords
    words = [w for w in words if w not in stopwords.words("english")]
    # apply stemming
    words = [PorterStemmer().stem(w) for w in words]
    # return list

    final_text=' '.join(words)
    return final_text


def predict_spam_class(text):
    max_len=100
    '''Function to predict sentiment class of the passed text'''

    sentiment_classes = ['Unhamed', 'spam']
    max_len=100
    final_text=pre_text(text)
    #print(pro_text)
    # Transforms text to a sequence of integers using a tokenizer object
    xt = tokenizer_spam.texts_to_sequences([final_text])
    # Pad sequences to the same length
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    # Do the prediction using the loaded model
    yt = model_spam_class.predict(xt).argmax(axis=1)
    #print(yt)
    # Print the predicted sentiment
    print('The predicted sentiment is', sentiment_classes[yt[0]])

    return sentiment_classes[yt[0]]
