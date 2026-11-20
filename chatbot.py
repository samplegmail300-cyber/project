
"""
chatbot.py - Doctor AI
Groq API powered health information chatbot.

Features:
1. Emergency detection before AI response.
2. Groq AI for general health questions.
3. English, Urdu and Roman Urdu support.
4. Keyword-based fallback if API is unavailable.
5. Secure API key loading from .env.
6. Medical safety instructions.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# ----------------------------------------------------------
# PART 1: CONFIGURATION
# ----------------------------------------------------------

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"

DISCLAIMER = (
    "\n\nNote: I am Doctor AI, an educational health information "
    "assistant. I cannot diagnose diseases or prescribe medicines. "
    "Please consult a qualified healthcare professional for personal "
    "medical advice."
)

EMERGENCY_RESPONSE = (
    "This could be a medical emergency. Please contact your local "
    "emergency service or go to the nearest hospital immediately. "
    "Do not wait for an online chatbot."
)

UNKNOWN_RESPONSE = (
    "Sorry, I could not process your question. Please ask a general "
    "health-related question or consult a healthcare professional."
)

# ----------------------------------------------------------
# PART 2: EMERGENCY KEYWORDS
# ----------------------------------------------------------

EMERGENCY_KEYWORDS = [
    "chest pain",
    "chest tightness",
    "pain in my chest",
    "difficulty breathing",
    "trouble breathing",
    "can't breathe",
    "cannot breathe",
    "cant breathe",
    "short of breath",
    "shortness of breath",
    "unconscious",
    "passed out",
    "not waking up",
    "won't wake up",
    "severe bleeding",
    "heavy bleeding",
    "bleeding a lot",
    "bleeding badly",
    "won't stop bleeding",
]

GREETING_KEYWORDS = [
    "hello",
    "hi",
    "hey",
    "good morning",
    "good evening",
]

# ----------------------------------------------------------
# PART 3: KEYWORD-BASED HEALTH TOPICS
# ----------------------------------------------------------

TOPICS = [
    {
        "name": "fever",
        "keywords": ["fever", "high temperature", "temperature"],
        "answer": (
            "A fever means your body temperature is higher than normal.\n\n"
            "General care:\n"
            "- Rest as much as possible.\n"
            "- Drink enough fluids.\n"
            "- Wear light clothing.\n\n"
            "Consult a doctor if fever is persistent, very high, "
            "or accompanied by concerning symptoms."
        ),
    },
    {
        "name": "headache",
        "keywords": ["headache", "head ache", "head hurts", "migraine"],
        "answer": (
            "Headaches can have many causes.\n\n"
            "General care:\n"
            "- Rest in a quiet place.\n"
            "- Drink enough water.\n"
            "- Get sufficient sleep.\n"
            "- Take breaks from screens.\n\n"
            "Seek medical advice for severe, sudden or recurring headaches."
        ),
    },
    {
        "name": "cough",
        "keywords": ["cough", "coughing"],
        "answer": (
            "A cough can have many different causes.\n\n"
            "General care:\n"
            "- Drink warm fluids.\n"
            "- Stay hydrated.\n"
            "- Rest.\n"
            "- Avoid smoke and dust.\n\n"
            "Consult a doctor if the cough persists or worsens."
        ),
    },
    {
        "name": "sore throat",
        "keywords": ["sore throat", "throat pain", "throat hurts", "throat"],
        "answer": (
            "A sore throat can feel uncomfortable.\n\n"
            "General care:\n"
            "- Drink warm fluids.\n"
            "- Rest your voice.\n"
            "- Gargling with warm salt water may help.\n\n"
            "Consult a doctor if symptoms persist or worsen."
        ),
    },
    {
        "name": "cold",
        "keywords": ["cold", "runny nose", "blocked nose", "sneezing", "flu"],
        "answer": (
            "Common cold symptoms often improve with time.\n\n"
            "General care:\n"
            "- Get enough rest.\n"
            "- Drink fluids.\n"
            "- Wash your hands regularly.\n"
            "- Cover your mouth when coughing or sneezing.\n\n"
            "Seek medical advice if symptoms worsen."
        ),
    },
    {
        "name": "stomach pain",
        "keywords": [
            "stomach pain",
            "stomach ache",
            "stomachache",
            "stomach",
            "tummy",
            "belly pain",
            "abdominal pain",
            "nausea",
            "vomiting",
        ],
        "answer": (
            "Stomach pain can happen for many reasons.\n\n"
            "General care:\n"
            "- Rest.\n"
            "- Sip water slowly.\n"
            "- Eat simple foods when you feel ready.\n\n"
            "Seek medical attention for severe or persistent pain, "
            "blood in vomit or stool, or repeated vomiting."
        ),
    },
    {
        "name": "healthy lifestyle",
        "keywords": [
            "healthy",
            "lifestyle",
            "stay fit",
            "exercise",
            "workout",
            "diet",
            "nutrition",
            "sleep",
            "wellness",
            "immunity",
        ],
        "answer": (
            "Healthy lifestyle habits include:\n\n"
            "- Eat a balanced diet.\n"
            "- Drink enough water.\n"
            "- Exercise regularly.\n"
            "- Get sufficient sleep.\n"
            "- Maintain good hygiene.\n"
            "- Manage stress.\n"
            "- Avoid smoking."
        ),
    },
]

# ----------------------------------------------------------
# PART 4: HELPER FUNCTIONS
# ----------------------------------------------------------

def _clean_message(message):
    """Convert message to lowercase and remove extra spaces."""
    message = message.replace("\u2019", "'")
    return message.lower().strip()


def _contains_any(message, keywords):
    """Check whether any keyword exists in the message."""
    return any(word in message for word in keywords)


def _is_greeting(message):
    """Check whether the message is a greeting."""
    words = (
        message.replace(",", " ")
        .replace("!", " ")
        .replace("?", " ")
        .split()
    )

    for greeting in GREETING_KEYWORDS:
        if " " in greeting:
            if greeting in message:
                return True
        elif greeting in words:
            return True

    return False


# ----------------------------------------------------------
# PART 5: KEYWORD-BASED FALLBACK
# ----------------------------------------------------------

def _get_keyword_response(user_message):
    """Return a predefined response if AI is unavailable."""

    if not isinstance(user_message, str) or not user_message.strip():
        return "Please type a health question and I will try to help."

    message = _clean_message(user_message)

    if _contains_any(message, EMERGENCY_KEYWORDS):
        return EMERGENCY_RESPONSE

    for topic in TOPICS:
        if _contains_any(message, topic["keywords"]):
            return topic["answer"] + DISCLAIMER

    if _is_greeting(message):
        return (
            "Hello! I am Doctor AI, your health information assistant. "
            "You can ask me general health questions."
        )

    return UNKNOWN_RESPONSE


# ----------------------------------------------------------
# PART 6: GROQ AI RESPONSE
# ----------------------------------------------------------

def _get_ai_response(user_message):
    """Generate a response using Groq API."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Doctor AI, an educational health information "
                    "assistant. Answer in the language used by the user, "
                    "including English, Urdu or Roman Urdu. Give clear, "
                    "accurate and easy-to-understand general health "
                    "information. Never diagnose diseases or prescribe "
                    "medicines or personalized dosages. Explain uncertainty "
                    "when appropriate. Encourage users to consult qualified "
                    "healthcare professionals for personal medical advice. "
                    "For potentially serious symptoms, recommend prompt "
                    "medical evaluation. For emergency symptoms, advise "
                    "immediate emergency medical assistance. Never invent "
                    "medical facts or claim to replace a doctor."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0.3,
        max_completion_tokens=700,
    )

    answer = response.choices[0].message.content

    if answer and answer.strip():
        return answer.strip()

    return None


# ----------------------------------------------------------
# PART 7: MAIN FUNCTION USED BY STREAMLIT
# ----------------------------------------------------------

def get_bot_response(user_message):
    """
    Main chatbot function.

    1. Validate input.
    2. Detect emergencies.
    3. Handle greetings.
    4. Try Groq AI.
    5. Use keyword fallback if API fails.
    """

    if not isinstance(user_message, str) or not user_message.strip():
        return "Please type a health question and I will try to help."

    message = _clean_message(user_message)

    # Emergency detection always comes first.
    if _contains_any(message, EMERGENCY_KEYWORDS):
        return EMERGENCY_RESPONSE

    # Handle greetings without using API.
    if _is_greeting(message):
        return (
            "Hello! I am Doctor AI, your health information assistant. "
            "You can ask me general health questions about health, "
            "symptoms, diseases and healthy lifestyle."
        )

    try:
        answer = _get_ai_response(user_message)

        if answer:
            return answer + DISCLAIMER

    except Exception:
        pass

    # API unavailable, key missing or free limit reached.
    return _get_keyword_response(user_message)


# ----------------------------------------------------------
# PART 8: OPTIONAL TERMINAL TEST
# ----------------------------------------------------------

if __name__ == "__main__":

    print("Doctor AI - Groq API Test")
    print("Type 'quit' to stop.\n")

    while True:

        user_input = input("You: ")

        if user_input.strip().lower() == "quit":
            break

        bot_reply = get_bot_response(user_input)

        print("\nDoctor AI:", bot_reply)
        print()
