
import re
from datetime import datetime
from spam_lists import SPAMHAUS_DBL
import spf
import checkdmarc
import pandas as pd
import numpy as np
import pickle
import os

current_path =os.path.dirname(os.path.abspath(__file__))
# Path to the .pkl file
#model_path = '/content/drive/MyDrive/Work_space/Project/Cyber/API/app/service01/service01_model/email_header_model/email_header_RFC.pkl'
model_path = os.path.join(current_path,"service01_model/email_header_model/email_header_RFC.pkl")



# Load the model
with open(model_path, 'rb') as file:
    model_header = pickle.load(file)



def if_special(x):
    special_characters = "]!@#$%^&*()-+?_=,<>/["
    for c in x :
        if c in special_characters:
            return 1
    return 0

def count_num_words(x):
    w = x.split(" ")
    return len(w)

def count_num_cap_words(x):
    w = x.split(" ")
    count = 0
    for i in w:
        if i.isupper():
            count+=1
    return count

def count_num_cap_char(x):
    count = 0
    for i in x:
        if i.isupper():
            count+=1
    return count

def count_digit(x):
    count=0
    for i in x:
        if i.isdigit():
            count+=1
    return count

def count_num_char(x):
    count=0
    for i in x:
        if i.isalpha():
            count+=1
    return count

def count_space(x):
    count=0
    for i in x:
        if i.isspace():
            count+=1
    return count

def count_special(x):
    special_characters = "]!@#$%^&*()-+?_=,<>/["
    return len([c for c in x if c in special_characters])

def singleQuote(x):
    count = 0
    for res in x:
        if "'" in res:
            count+=1
    save = count/2
    return save

def count_num_semiColon(x):
    count = 0
    for i in x:
        if ';' in i:
            count+=1
    return count

def ratio_upperCase_lowerCae(x):

    countUpp =0
    countLow =0

    save = x.split(" ")
    for i in save:
        if i.isupper():
            countUpp+=1
        else:
            countLow+=1

    ratio = countUpp/countLow

    return ratio

def upperCase(x):
    count = 0
    save = x.split(" ")
    for i in save:
        if i.isupper():
            count+=1
    return count

def MaxWordLength(str):
    strLen = len(str)
    save = 0; currentLength = 0

    for i in range(0, strLen):
        if (str[i] != ' '):
            currentLength += 1
        else:
            save = max(save, currentLength)
            currentLength = 0

    return max(save, currentLength)

stored_spf = dict()
def check_spf_valid(domain):
    if(domain == ' ' or domain == '' or domain == 'nan'):
        return 0
    if(stored_spf.get(domain)==None):
        try:
            checkdmarc.get_dmarc_record(domain, nameservers=["1.1.1.1"])
            stored_spf[domain] = 1
            return 1
        except:
            stored_spf[domain] = 0
            return 0
    else:
        return stored_spf.get(domain)


stored_val = dict()
def check_blackListed(domain):
    if(domain == ' ' or domain == '' or domain == 'nan'):
        return 0
    if(stored_val.get(domain)==None):
        try:
            if(domain in SPAMHAUS_DBL):
                stored_val[domain] = 1
                return 1
            else:
                stored_val[domain]= 0
                return 0
        except:
            return 0
    else:
        return stored_val.get(domain)




def header_spam_detection(hops:int,date:str,Subject:str,From:list):
  #hops=3
  #date=" Sun, 17 Jun 2007 "# Sun, 17 Jun 2007
  #Subject="riffle"
  #From=['"Gilda Isaac" <Phoebesiemensclaudia@victorytu']#["Shane <shane-keyword-speakup.aca783@cm.nu>","<ktwarwic@flax9.uwaterloo.ca>"]#
  domain=[]
  df=dict()



  #Get the domain address
  for i in From:
    new_email=re.findall(r'([\w\.-]+@[\w\.-]+)',i)
    #print(new_email)
    for email in new_email:
      domain.append(email.split('@')[1])
  #print(df)
  #print(domain)

  df["hops"]=hops
  df['special_characters_exists_subject'] = if_special(Subject)
  df['number_of_words_subject'] = count_num_words(Subject)
  df['number_of_capitalized_words_subject'] = count_num_cap_words(Subject)
  df['number_of_capitalized_characters_subject'] = count_num_cap_char(Subject)
  df['number_of_digits_subject'] = count_digit(Subject)
  df['number_of_characters_subject'] =count_num_char(Subject)
  df['number_of_spaces_subject'] =count_space(Subject)
  df['number_of_special_characters_subject'] =count_special(Subject)
  df['number_of_single_Quotes_subject'] = singleQuote(Subject)
  df['number_of_semiColon_subject'] = count_num_semiColon(Subject)
  df['ratio_of_uppercase/lowercase_words'] = ratio_upperCase_lowerCae(Subject)
  df['Total_number_of_upperCase'] = upperCase(Subject)
  df['Max_word_length_in_subject'] = MaxWordLength(Subject)

  for i in domain:
    df['spf_valid'] = check_spf_valid(i)
    df['blackListed'] = check_blackListed(i)

  df['Date'] = date.split(',')[-1]
  #validating date after converting it to datetime
  df['new_date'] = pd.to_datetime(df['Date'],errors="coerce")

  df['validate_date'] = 1 if df['new_date'] < datetime.now() else 0
  df['Subject_length']  = len(Subject)
  '''
  Validating date and subject length
  '''
  select_columns=['hops', 'special_characters_exists_subject', 'number_of_words_subject', 'number_of_capitalized_words_subject', 'number_of_capitalized_characters_subject',
 'number_of_digits_subject', 'number_of_characters_subject', 'number_of_spaces_subject', 'number_of_special_characters_subject', 'number_of_single_Quotes_subject',
 'number_of_semiColon_subject', 'ratio_of_uppercase/lowercase_words', 'Total_number_of_upperCase', 'Max_word_length_in_subject', 'spf_valid', 'blackListed',
 'validate_date', 'Subject_length']

  #create panda data series
  new_df=pd.Series(df)
  select_df=new_df[select_columns]

  #print(select_df.values.reshape(1,-1))

  y_predict=model_header.predict(select_df.values.reshape(1,-1))
  #print(y_predict)

  classe=''
  if y_predict[0]==1:
    classe="Spam"
  else:
    classe="Unhamed"


  return classe

