import os
import re
import joblib
import nltk
from django.conf import settings
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

MODEL_DIR = os.path.join(settings.BASE_DIR, "models")

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

lemmatiser = WordNetLemmatizer()
useless_words = set(stopwords.words("english"))

unique_type_list = [
    "infj", "entp", "intp", "intj",
    "entj", "enfj", "infp", "enfp",
    "isfp", "istp", "isfj", "istj",
    "estp", "esfp", "estj", "esfj"
]


class PersonalityPredictor:

    def __init__(self):
        self.vectorizer = joblib.load(
            os.path.join(MODEL_DIR, "count_vectorizer.pkl")
        )

        self.tfidf = joblib.load(
            os.path.join(MODEL_DIR, "tfidf_transformer.pkl")
        )

        self.models = {
            "IE": joblib.load(os.path.join(MODEL_DIR, "IE_xgb_model.pkl")),
            "NS": joblib.load(os.path.join(MODEL_DIR, "NS_xgb_model.pkl")),
            "FT": joblib.load(os.path.join(MODEL_DIR, "FT_xgb_model.pkl")),
            "JP": joblib.load(os.path.join(MODEL_DIR, "JP_xgb_model.pkl")),
        }

    def preprocess_text(self, text):
        temp = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            " ",
            text
        )

        temp = re.sub(r"[^a-zA-Z]", " ", temp)
        temp = re.sub(r" +", " ", temp).lower()
        temp = re.sub(r"([a-z])\1{2,}[\s|\w]*", "", temp)

        temp = " ".join(
            [lemmatiser.lemmatize(w) for w in temp.split(
                " ") if w and w not in useless_words]
        )

        for t in unique_type_list:
            temp = temp.replace(t, "")

        return temp.strip()

    def predict(self, text):
        cleaned_text = self.preprocess_text(text)
        text_input = [cleaned_text]

        X_cnt = self.vectorizer.transform(text_input)
        X_tfidf = self.tfidf.transform(X_cnt).toarray()

        label_mapping = {
            "IE": {0: "I", 1: "E"},
            "NS": {0: "N", 1: "S"},
            "FT": {0: "F", 1: "T"},
            "JP": {0: "J", 1: "P"},
        }

        final_type = ""
        percentages = []
        personality_percentages = {}

        for key, model in self.models.items():
            pred = model.predict(X_tfidf)[0]
            letter = label_mapping[key][pred]

            probs = model.predict_proba(X_tfidf)[0]
            percent = max(probs) * 100

            final_type += letter
            percentages.append(percent)
            personality_percentages[letter] = round(percent, 2)

        overall_confidence = round(sum(percentages) / len(percentages), 2)

        return {
            "personality_type": final_type,
            "percentages": personality_percentages,
            "overall_confidence": overall_confidence
        }
