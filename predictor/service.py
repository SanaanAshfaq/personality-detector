import os
import joblib
from django.conf import settings


MODEL_DIR = os.path.join(settings.BASE_DIR, "predictor", "ml_models")


class PersonalityPredictor:

    def __init__(self):
        self.vectorizer = joblib.load(
            os.path.join(MODEL_DIR, "count_vectorizer.pkl")
        )

        self.tfidf = joblib.load(
            os.path.join(MODEL_DIR, "tfidf_transformer.pkl")
        )

        self.models = {
            "IE": joblib.load(os.path.join(MODEL_DIR, "IE__Introversion__I____Extroversion__E__model.pkl")),
            "NS": joblib.load(os.path.join(MODEL_DIR, "NS__Intuition__N____Sensing__S__model.pkl")),
            "FT": joblib.load(os.path.join(MODEL_DIR, "FT__Feeling__F____Thinking__T__model.pkl")),
            "JP": joblib.load(os.path.join(MODEL_DIR, "JP__Judging__J____Perceiving__P__model.pkl")),
        }

    def predict(self, text):
        text = [text]

        X_cnt = self.vectorizer.transform(text)
        X_tfidf = self.tfidf.transform(X_cnt)

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
            probs = model.predict_proba(X_tfidf)[0]  

  
            if probs[0] > probs[1]:
                letter = label_mapping[key][0]
                percent = probs[0] * 100
            else:
                letter = label_mapping[key][1]
                percent = probs[1] * 100

            final_type += letter
            percentages.append(percent)
            personality_percentages[letter] = round(percent, 2)

        overall_confidence = round(sum(percentages) / len(percentages), 2)

        return {
            "personality_type": final_type,
            "percentages": personality_percentages,
            "overall_confidence": overall_confidence
        }