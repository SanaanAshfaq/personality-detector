from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings
from dotenv import load_dotenv
from .serializer import TextInputSerializer
from .service import PersonalityPredictor
import os
load_dotenv()
predictor = PersonalityPredictor()
from groq import Groq  # Note: Changed import to 'groq' (lowercase) 
import os
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise Exception("GROQ_API_KEY not found in environment!")

# Initialize the client
client = Groq(api_key=api_key)

def generate_personality_advice(personality_type: str, user_text: str):
    prompt = f"""
    The user is {personality_type}.
    Based on their personality type, give personalized advice or insights 
    about their behavior, mindset, and strengths.
    Text they provided: "{user_text}".
    """
    
    # Correct method for Groq client
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="qwen/qwen3-32b",  # Active as of Feb 2026
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content  # Correct way to access the response

class PredictPersonalityView(APIView):

    def post(self, request):
        serializer = TextInputSerializer(data=request.data)

        if serializer.is_valid():
            text = serializer.validated_data["text"]

            # Step 1: Predict personality
            result = predictor.predict(text)
            personality_type = result["personality_type"]
            overall_confidence = result["overall_confidence"]

            # Step 2: Call LLM to generate advice
            advice = generate_personality_advice(personality_type, text)

            # Step 3: Return combined response
            return Response({
                "prediction": result,
                "personality_type": personality_type,
                "overall_confidence": overall_confidence,
                "advice": advice,  
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)