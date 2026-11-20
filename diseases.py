"""
diseases.py - Doctor AI (beginner-level health conditions library)

This file stores simple information about 8 common health conditions
and gives you two functions to use in your app:

    get_disease_names()          -> list of all condition names
    get_disease_info(name)       -> information about one condition

MEDICAL DISCLAIMER: The information here is for education only.
It is NOT a diagnosis and NOT treatment advice. Having a symptom does
not mean a person has a certain condition. Please talk to a doctor or
healthcare professional about your health.
"""

# ----------------------------------------------------------
# PART 1: The disclaimer (shown with every result)
# ----------------------------------------------------------
DISCLAIMER = (
    "This information is for educational purposes only. It is not a "
    "diagnosis or treatment advice. Please talk to a doctor or "
    "healthcare professional about your health."
)

# ----------------------------------------------------------
# PART 2: The data
# ----------------------------------------------------------
# DISEASES is a dictionary. The key is the condition name, and the value
# is another dictionary with the details. Lists hold several short points.
#
# To add a new condition, copy one block, paste it below, and change the text.

DISEASES = {
    "Fever": {
        "name": "Fever",
        "description": (
            "A fever means the body temperature is higher than normal. "
            "It is not a disease by itself. It is a sign that the body is "
            "reacting to something, often an infection."
        ),
        "symptoms": [
            "Feeling hot or warm to the touch",
            "Sweating or chills",
            "Headache",
            "Body aches",
            "Tiredness and weakness",
            "Loss of appetite",
        ],
        "causes": [
            "Infections caused by viruses or bacteria",
            "Heat exhaustion from very hot weather",
            "Reactions to some vaccines",
            "Some long-term inflammation conditions",
        ],
        "prevention": [
            "Wash your hands often with soap and water",
            "Stay away from people who are sick when possible",
            "Keep up with recommended vaccines",
            "Drink safe water and eat safely prepared food",
            "Drink enough fluids and rest in the shade in hot weather",
        ],
        "when_to_consult": [
            "The fever is very high or lasts more than 2 to 3 days",
            "The person is a baby, an older adult, pregnant, or has a long-term health condition",
            "The fever comes with a rash, a stiff neck, confusion, or a very bad headache",
            "Get emergency help if there is trouble breathing or the person is hard to wake up",
        ],
    },
    "Common Cold": {
        "name": "Common Cold",
        "description": (
            "A mild illness caused by viruses that mainly affects the nose "
            "and throat. It usually gets better on its own in about a week "
            "to ten days."
        ),
        "symptoms": [
            "Runny or blocked nose",
            "Sneezing",
            "Sore throat",
            "Mild cough",
            "Mild tiredness",
            "Sometimes a mild headache",
        ],
        "causes": [
            "Cold viruses spread through coughs and sneezes",
            "Touching a surface with the virus and then touching your face",
            "Close contact with a person who has a cold",
        ],
        "prevention": [
            "Wash your hands often",
            "Cover your mouth and nose when you cough or sneeze",
            "Avoid touching your eyes, nose, and mouth",
            "Do not share cups, towels, or utensils",
            "Get enough sleep and eat a balanced diet",
        ],
        "when_to_consult": [
            "Symptoms last more than 10 days or keep getting worse",
            "There is a high fever or trouble breathing",
            "Ear pain, chest pain, or a very painful throat appears",
            "The person is a baby, an older adult, or has a long-term health condition",
        ],
    },
    "Flu": {
        "name": "Flu",
        "description": (
            "Flu (influenza) is a viral illness that affects the nose, "
            "throat, and sometimes the lungs. It often starts suddenly and "
            "feels stronger than a common cold."
        ),
        "symptoms": [
            "Fever or chills",
            "Body aches",
            "Tiredness and weakness",
            "Cough",
            "Sore throat",
            "Headache",
        ],
        "causes": [
            "Influenza viruses",
            "Spread through coughs, sneezes, and close contact",
            "Touching infected surfaces and then touching your face",
        ],
        "prevention": [
            "Get the yearly flu vaccine if your health authority recommends it",
            "Wash your hands often",
            "Cover your mouth and nose when you cough or sneeze",
            "Stay home when you are sick to protect others",
            "Avoid crowded places during flu season when possible",
        ],
        "when_to_consult": [
            "Symptoms are strong or last more than a few days",
            "The person is pregnant, an older adult, a young child, or has a long-term health condition",
            "Symptoms get better and then suddenly get worse",
            "Get emergency help for trouble breathing, chest pain, or confusion",
        ],
    },
    "Diabetes": {
        "name": "Diabetes",
        "description": (
            "A long-term condition where the level of sugar in the blood "
            "stays too high. This happens when the body does not make "
            "enough insulin or cannot use insulin well."
        ),
        "symptoms": [
            "Feeling very thirsty",
            "Passing urine often",
            "Feeling very tired",
            "Blurred vision",
            "Cuts or wounds that heal slowly",
            "Losing weight without trying",
            "Some people have no clear symptoms at first",
        ],
        "causes": [
            "Type 1: the body's defense system attacks the cells that make insulin (the exact reason is not fully known)",
            "Type 2: the body does not respond well to insulin, often linked to extra body weight, little physical activity, age, and family history",
            "Gestational diabetes: high blood sugar that can appear during pregnancy",
        ],
        "prevention": [
            "Type 2 can often be delayed or prevented with a healthy lifestyle",
            "Keep a healthy body weight",
            "Be active most days of the week",
            "Eat a balanced diet with plenty of vegetables and whole grains",
            "Limit sugary drinks and avoid smoking",
            "Have regular health check-ups, especially with a family history",
            "Type 1 diabetes cannot currently be prevented",
        ],
        "when_to_consult": [
            "You have symptoms like extreme thirst, frequent urination, or unexplained weight loss",
            "You have a family history of diabetes or other risk factors",
            "Your doctor suggested a blood sugar check",
            "Get emergency help for vomiting, deep fast breathing, confusion, or extreme sleepiness",
        ],
    },
    "High Blood Pressure": {
        "name": "High Blood Pressure",
        "description": (
            "Also called hypertension. It means the force of blood pushing "
            "against the walls of blood vessels is often too high. Over "
            "time, it can strain the heart and blood vessels."
        ),
        "symptoms": [
            "Often there are no symptoms, so it is called a silent condition",
            "Some people may notice headaches or dizziness",
            "Blood pressure checks are the only reliable way to know",
        ],
        "causes": [
            "Eating too much salt",
            "Extra body weight",
            "Not enough physical activity",
            "Smoking and too much alcohol",
            "Long-term stress",
            "Family history and growing older",
            "Some kidney or hormone conditions",
        ],
        "prevention": [
            "Eat less salt and fewer processed foods",
            "Eat more fruits and vegetables",
            "Keep a healthy body weight",
            "Be active most days of the week",
            "Avoid smoking and limit alcohol",
            "Manage stress and get enough sleep",
            "Check your blood pressure regularly",
        ],
        "when_to_consult": [
            "Your blood pressure readings are often higher than normal",
            "You have a family history of high blood pressure",
            "You have not had your blood pressure checked in a long time",
            "Get emergency help for chest pain, trouble breathing, sudden weakness, or a sudden severe headache",
        ],
    },
    "Asthma": {
        "name": "Asthma",
        "description": (
            "A long-term condition where the airways in the lungs can "
            "become swollen and narrow, which makes breathing harder. "
            "Symptoms can come and go."
        ),
        "symptoms": [
            "Wheezing (a whistling sound when breathing)",
            "Coughing, often at night or early morning",
            "Chest tightness",
            "Shortness of breath",
        ],
        "causes": [
            "Allergies to dust, pollen, pets, or mold",
            "Cigarette smoke and air pollution",
            "Cold air or exercise",
            "Breathing infections like colds",
            "Family history",
        ],
        "prevention": [
            "Asthma cannot always be prevented, but attacks can often be reduced",
            "Learn what triggers your symptoms and avoid them",
            "Stay away from smoke and strong smells",
            "Keep your home clean and dust free",
            "Follow the asthma plan your doctor gives you",
        ],
        "when_to_consult": [
            "You often cough, wheeze, or feel short of breath",
            "Symptoms wake you at night or limit your daily activities",
            "Your usual plan does not seem to be working",
            "Get emergency help for severe trouble breathing, trouble speaking, or blue lips",
        ],
    },
    "Migraine": {
        "name": "Migraine",
        "description": (
            "A type of headache that is often strong and throbbing, usually "
            "on one side of the head. It can last from a few hours to a "
            "few days."
        ),
        "symptoms": [
            "Throbbing or pulsing head pain",
            "Feeling sick (nausea) or vomiting",
            "Sensitivity to light, sound, or smells",
            "Seeing flashing lights or blind spots before the headache (in some people)",
        ],
        "causes": [
            "The exact cause is not fully understood",
            "Common triggers include stress and lack of sleep",
            "Skipping meals or not drinking enough water",
            "Bright lights, loud noise, or strong smells",
            "Hormone changes",
            "Family history",
        ],
        "prevention": [
            "Sleep and wake up at regular times",
            "Eat regular meals and drink enough water",
            "Manage stress with relaxation, walks, or hobbies",
            "Keep a headache diary to find your triggers",
            "Take regular breaks from screens",
        ],
        "when_to_consult": [
            "Headaches are frequent, getting worse, or changing in pattern",
            "Headaches affect your school, work, or daily life",
            "Get emergency help for a sudden, very severe headache",
            "Get emergency help if a headache comes with weakness, trouble speaking, confusion, a stiff neck, or after a head injury",
        ],
    },
    "Food Poisoning": {
        "name": "Food Poisoning",
        "description": (
            "An illness caused by eating or drinking food or water that "
            "contains harmful germs or toxins. Most cases are mild and get "
            "better within a few days."
        ),
        "symptoms": [
            "Nausea and vomiting",
            "Diarrhea",
            "Stomach cramps or pain",
            "Mild fever",
            "Tiredness and weakness",
        ],
        "causes": [
            "Bacteria, viruses, or parasites in food or water",
            "Undercooked meat, eggs, or seafood",
            "Unwashed fruits and vegetables",
            "Food left out in the heat for too long",
            "Poor hand washing while preparing food",
        ],
        "prevention": [
            "Wash your hands before cooking and eating",
            "Cook food thoroughly",
            "Keep raw and cooked foods separate",
            "Store food in the fridge soon after cooking",
            "Drink safe, clean water",
            "Check food expiry dates and avoid food that smells or looks spoiled",
        ],
        "when_to_consult": [
            "Symptoms last more than 2 days",
            "You cannot keep fluids down or have signs of dehydration, like very dark urine, dizziness, or a dry mouth",
            "There is blood in the vomit or stool, or a high fever",
            "The person is a baby, an older adult, pregnant, or has a long-term health condition",
            "Get emergency help for confusion, severe stomach pain, or extreme weakness",
        ],
    },
}


# ----------------------------------------------------------
# PART 3: Functions used by your Streamlit app
# ----------------------------------------------------------

def get_disease_names():
    """Return a list of all condition names (for example, for a dropdown)."""
    return list(DISEASES.keys())


def get_disease_info(disease_name):
    """
    Return the information for one condition as a dictionary.

    The dictionary has these keys:
    name, description, symptoms, causes, prevention,
    when_to_consult, disclaimer

    It is not case sensitive, so "flu", "FLU", and "Flu" all work.
    If the name is not found, it returns None.
    """

    # Make sure we received text.
    if not isinstance(disease_name, str):
        return None

    # Compare in lowercase and ignore extra spaces.
    wanted = disease_name.strip().lower()

    for key, info in DISEASES.items():
        if key.lower() == wanted:
            result = dict(info)              # make a copy so the original is safe
            result["disclaimer"] = DISCLAIMER
            return result

    # No match found.
    return None


# ----------------------------------------------------------
# PART 4: Optional quick test in the terminal
# Run with:  python diseases.py
# (This part does NOT run when you import the file in Streamlit.)
# ----------------------------------------------------------
if __name__ == "__main__":
    print("Available conditions:", ", ".join(get_disease_names()))
    choice = input("Type a condition name: ")
    info = get_disease_info(choice)

    if info is None:
        print("Sorry, I do not have information about that condition.")
    else:
        print("\n" + info["name"])
        print(info["description"])
        for title, key in [("Common symptoms", "symptoms"),
                           ("Possible causes", "causes"),
                           ("Prevention tips", "prevention"),
                           ("When to consult a doctor", "when_to_consult")]:
            print("\n" + title + ":")
            for point in info[key]:
                print(" -", point)
        print("\nNote:", info["disclaimer"])
