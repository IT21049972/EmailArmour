
import pickle
import re
import os

current_path =os.path.dirname(os.path.abspath(__file__))

###Language detection model
#Language_detection="/content/drive/MyDrive/Work_space/Project/Cyber/API/app/service01/service01_model/Launguage_detection/Language_detection_model_v1.pkl"
Language_detection=os.path.join(current_path,"service01_model/Launguage_detection/Language_detection_model_v1.pkl")

#Language_encoder="/content/drive/MyDrive/Work_space/Project/Cyber/API/app/service01/service01_model/Launguage_detection/Language_encoder.pkl"
Language_encoder=os.path.join(current_path,"service01_model/Launguage_detection/Language_encoder.pkl")


with open(Language_detection, 'rb') as file:
    model_language = pickle.load(file)

with open(Language_encoder, 'rb') as file:
    encode_language = pickle.load(file)


# function to clean text
def clean_txt(text):
    text=text.lower()
    text=re.sub(r'[^\w\s]',' ',text)
    text=re.sub(r'[_0-9]',' ',text)
    text=re.sub(r'\s\s+',' ',text)
    return text

def predict_language(text):
    pred =model_language.predict([clean_txt(text)])
    ans = encode_language.inverse_transform(pred)
    return ans[0]


