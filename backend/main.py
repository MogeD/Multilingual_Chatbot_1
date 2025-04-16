from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from langdetect import detect
from googletrans import Translator
import json
import os

app = FastAPI(title="Multilingual Chatbot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load language-specific responses
RESPONSES = {
    # Default/English Language
    "en": {
        "greetings": ["Hello", "Hi", "Hey there"],
        "how_are_you": ["I'm doing well, how are you?"],
        "goodbye": ["Goodbye", "See you later", "Bye"],
        "default": "How can I help you?",
        "responses": {
            "i need help": "I'm here to help! What can I do for you?",
            "thank you": "You're welcome!",
            "good morning": "Good morning! How are you today?",
            "good night": "Good night! Have a great rest!",
            "i'm hungry": "I can help you find some good restaurants nearby. What kind of food would you like?"
        }
    },
    
    # Indian Languages
    "hi": {  # Hindi
        "greetings": ["नमस्ते", "नमस्कार", "हैलो"],
        "how_are_you": ["मैं ठीक हूं, आप कैसे हैं?"],
        "goodbye": ["फिर मिलेंगे", "अलविदा", "नमस्ते"],
        "default": "मैं आपकी कैसे मदद कर सकता हूं?",
        "responses": {
            "मैं ठीक हूं": "बहुत अच्छा! क्या मैं आपकी कोई मदद कर सकता हूं?",
            "धन्यवाद": "आपका स्वागत है!",
            "शुभ रात्रि": "शुभ रात्रि! अच्छी नींद आए!",
            "भूख लगी है": "मैं आपको अच्छे रेस्टोरेंट ढूंढने में मदद कर सकता हूं। आप किस तरह का खाना पसंद करेंगे?",
            "मदद चाहिए": "ज़रूर, मैं आपकी क्या मदद कर सकता हूं?"
        }
    },
    "te": {  # Telugu
        "greetings": ["నమస్కారం", "హలో"],
        "how_are_you": ["నేను బాగున్నాను, మీరు ఎలా ఉన్నారు?"],
        "goodbye": ["వీడ్కోలు", "మళ్ళీ కలుద్దాం"],
        "default": "నేను మీకు ఎలా సహాయపడగలను?"
    },
    "ta": {  # Tamil
        "greetings": ["வணக்கம்", "நமஸ்காரம்"],
        "how_are_you": ["நான் நலம், நீங்கள் எப்படி இருக்கிறீர்கள்?"],
        "goodbye": ["பிறகு சந்திப்போம்", "வணக்கம்"],
        "default": "நான் உங்களுக்கு எப்படி உதவ முடியும்?"
    },
    "kn": {  # Kannada
        "greetings": ["ನಮಸ್ಕಾರ", "ಹಲೋ"],
        "how_are_you": ["ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ, ನೀವು ಹೇಗಿದ್ದೀರಿ?"],
        "goodbye": ["ಮತ್ತೆ ಸಿಗೋಣ", "ನಮಸ್ಕಾರ"],
        "default": "ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
    },
    "ml": {  # Malayalam
        "greetings": ["നമസ്കാരം", "ഹലോ"],
        "how_are_you": ["എനിക്ക് സുഖമാണ്, നിങ്ങൾക്ക് എങ്ങനെ ഉണ്ട്?"],
        "goodbye": ["വിട", "നമസ്കാരം"],
        "default": "എനിക്ക് നിങ്ങളെ എങ്ങനെ സഹായിക്കാൻ കഴിയും?"
    },
    "bn": {  # Bengali
        "greetings": ["নমস্কার", "হ্যালো"],
        "how_are_you": ["আমি ভালো আছি, আপনি কেমন আছেন?"],
        "goodbye": ["বিদায়", "আবার দেখা হবে"],
        "default": "আমি আপনাকে কীভাবে সাহায্য করতে পারি?"
    },
    "gu": {  # Gujarati
        "greetings": ["નમસ્તે", "હેલો"],
        "how_are_you": ["હું સારું છું, તમે કેમ છો?"],
        "goodbye": ["આવજો", "ફરી મળીશું"],
        "default": "હું તમને કેવી રીતે મદદ કરી શકું?"
    },

    # Nigerian Languages
    "yo": {  # Yoruba
        "greetings": ["Ẹ nlẹ́", "Ẹ káàárọ̀", "Báwo ni"],
        "how_are_you": ["Mo wà dáadáa, báwo ni ẹ̀yin?"],
        "goodbye": ["Ó dàbọ̀", "Ṣé àrọ́ìkúlẹ̀"],
        "default": "Báwo ni mo ṣe lè ràn yín lọ́wọ́?",
        "responses": {
            "mo wa daada": "Ó dára púpọ̀! Ṣé mo lè ràn yín lọ́wọ́?",
            "e se": "Ẹ kú àárọ̀!",
            "ebi n pa mi": "Mo lè ràn yín lọ́wọ́ láti wá ibi tó dára láti jẹun. Irú oúnjẹ wo ni ẹ fẹ́?",
            "mo nilo iranlowo": "Dájúdájú, báwo ni mo ṣe lè ràn yín lọ́wọ́?",
            "o dara": "Ó dára púpọ̀! Ṣé ẹ nílò nǹkan mìíràn?"
        }
    },
    "ha": {  # Hausa
        "greetings": ["Sannu", "Barka da yamma", "Barka da zuwa"],
        "how_are_you": ["Ina lafiya, yaya kake/kike?"],
        "goodbye": ["Sai an jima", "Sai gobe"],
        "default": "Yaya zan taimaka maka/miki?"
    },
    "ig": {  # Igbo
        "greetings": ["Nnọọ", "Kedụ", "Ụtụtụ ọma"],
        "how_are_you": ["Adị m mma, kedụ ka ị mere?"],
        "goodbye": ["Ka ọ dị", "Ka emesia"],
        "default": "Kedụ ka m ga-esi nyere gị aka?"
    },

    # Other African Languages
    "sw": {  # Swahili
        "greetings": ["Jambo", "Habari", "Hujambo"],
        "how_are_you": ["Mimi ni mzima, vipi wewe?"],
        "goodbye": ["Kwaheri", "Tutaonana"],
        "default": "Nawezaje kukusaidia?"
    },
    "am": {  # Amharic
        "greetings": ["ሰላም", "እንደምን አደርክ/ሽ"],
        "how_are_you": ["ጥሩ ነኝ፣ አንተ/ቺስ እንደምን ነህ/ሽ?"],
        "goodbye": ["ደህና ሁን/ኚ", "ቻው"],
        "default": "እንዴት ልረዳህ/ሽ?"
    },

    # European Languages
    "fr": {  # French
        "greetings": ["Bonjour", "Salut", "Bonsoir"],
        "how_are_you": ["Je vais bien, et vous?"],
        "goodbye": ["Au revoir", "À bientôt"],
        "default": "Comment puis-je vous aider?",
        "responses": {
            "comment ca va": "Je vais très bien, merci! Et vous?",
            "ca va bien": "Je suis ravi(e) de l'entendre!",
            "ca va mal": "Je suis désolé(e) d'entendre ça. Puis-je faire quelque chose pour vous aider?",
            "j'ai besoin": {
                "d'aide": "Bien sûr, je suis là pour vous aider. Que puis-je faire pour vous?",
                "de manger": "Je peux vous recommander de bons restaurants. Quel type de cuisine préférez-vous?",
                "d'un conseil": "Je serai ravi(e) de vous conseiller. Sur quel sujet?"
            },
            "merci": "Je vous en prie!",
            "bonne": {
                "nuit": "Bonne nuit! Faites de beaux rêves!",
                "journée": "Bonne journée à vous aussi!",
                "soirée": "Bonne soirée! Profitez bien!"
            }
        }
    },
    "es": {  # Spanish
        "greetings": ["¡Hola!", "¡Buenos días!", "¡Buenas tardes!"],
        "how_are_you": ["Estoy bien, ¿y tú?"],
        "goodbye": ["¡Adiós!", "¡Hasta luego!"],
        "default": "¿Cómo puedo ayudarte?",
        "responses": {
            "estoy bien": "¡Me alegro! ¿Necesitas ayuda con algo?",
            "gracias": "¡De nada!",
            "buenas noches": "¡Buenas noches! ¡Que descanses!",
            "tengo hambre": "Puedo ayudarte a encontrar buenos restaurantes. ¿Qué tipo de comida te gustaría?",
            "necesito ayuda": "¡Por supuesto! ¿En qué puedo ayudarte?"
        }
    },

    # East Asian Languages
    "zh": {  # Chinese
        "greetings": ["你好", "早上好", "晚上好"],
        "how_are_you": ["我很好，你呢？"],
        "goodbye": ["再见", "拜拜"],
        "default": "我能帮你什么？",
        "responses": {
            "我很好": "太好了！我能帮你什么吗？",
            "谢谢": "不用谢！",
            "晚安": "晚安！祝你好梦！",
            "我饿了": "我可以帮你找到好的餐馆。你想吃什么类型的食物？",
            "需要帮助": "当然可以，你需要什么帮助？",
            "早上好": "早上好！今天感觉如何？"
        }
    },
    "ja": {  # Japanese
        "greetings": ["こんにちは", "おはようございます"],
        "how_are_you": ["元気です、あなたは？"],
        "goodbye": ["さようなら", "じゃあね"],
        "default": "どのようにお手伝いできますか？",
        "responses": {
            "元気です": "よかったです！何かお手伝いできることはありますか？",
            "ありがとう": "どういたしまして！",
            "おやすみ": "おやすみなさい！良い夢を！",
            "お腹が空きました": "良いレストランをお探しできます。どんな料理がお好みですか？",
            "助けて": "もちろん、どのようなお手伝いが必要ですか？"
        }
    },
    "ko": {  # Korean
        "greetings": ["안녕하세요", "좋은 아침이에요"],
        "how_are_you": ["저는 잘 지내요, 당신은요?"],
        "goodbye": ["안녕히 가세요", "다음에 봐요"],
        "default": "어떻게 도와드릴까요?"
    }
}

class ChatMessage(BaseModel):
    message: str
    language: str

def get_response(message: str, language: str) -> str:
    message = message.lower().strip()
    responses = RESPONSES.get(language, RESPONSES["en"])
    
    # Check for language-specific responses first
    if "responses" in responses:
        lang_responses = responses["responses"]
        
        # Check for nested responses first (like in French responses)
        for key, nested_responses in lang_responses.items():
            if isinstance(nested_responses, dict):
                if key in message:
                    for sub_key, response in nested_responses.items():
                        if sub_key in message:
                            return response
            elif key in message:
                return nested_responses
    
    # Common greetings in different languages
    greetings = ["hi", "hello", "hey", "bonjour", "hola", "你好", "こんにちは", 
                 "नमस्ते", "ẹ nlẹ́", "salut", "buenos dias"]
    
    # Common "how are you" phrases
    how_are_you_phrases = ["how are you", "comment ca va", "que tal", "お元気ですか", 
                          "कैसे हो", "báwo ni", "como estas"]
    
    # Common goodbye phrases
    goodbyes = ["bye", "goodbye", "au revoir", "adios", "さようなら", "अलविदा", 
                "ó dàbọ̀", "hasta luego"]
    
    if any(greeting in message for greeting in greetings):
        return responses["greetings"][0]
    elif any(phrase in message for phrase in how_are_you_phrases):
        return responses["how_are_you"][0]
    elif any(bye in message for bye in goodbyes):
        return responses["goodbye"][0]
    
    return responses["default"]

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = get_response(chat_message.message, chat_message.language)
        return {"response": response, "language": chat_message.language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-languages")
async def get_supported_languages():
    return {"languages": list(RESPONSES.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 