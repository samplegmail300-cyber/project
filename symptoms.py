"""
symptoms.py - Doctor AI (beginner-level, rule-based symptom checker)

How it works:
1. The user selects symptoms (a list of words like "Fever", "Cough").
2. We first check for EMERGENCY warning signs (safety comes first!).
3. Then we compare the symptoms with a small list of common conditions
   and count how many symptoms match each one.
4. We return a friendly text with possible related conditions,
   self-care tips, and advice about when to see a doctor.

IMPORTANT: This is a learning project. It does NOT diagnose diseases
and does NOT recommend medicines. It only shows general information.

In Streamlit you can show the result with:  st.markdown(check_symptoms(my_list))
"""

# ----------------------------------------------------------
# PART 1: Data (easy to edit in one place)
# ----------------------------------------------------------

# The symptoms this checker supports (use these names in your Streamlit
# multiselect box).
SUPPORTED_SYMPTOMS = [
    "Fever",
    "Headache",
    "Cough",
    "Sore throat",
    "Runny nose",
    "Fatigue",
    "Nausea",
    "Vomiting",
    "Stomach pain",
    "Diarrhea",
    "Body aches",
]

# If any of these words/phrases appear in the input, we show an
# emergency message instead of the normal result.
EMERGENCY_WARNING_SIGNS = [
    "chest pain",
    "chest tightness",
    "difficulty breathing",
    "trouble breathing",
    "can't breathe",
    "cannot breathe",
    "cant breathe",
    "short of breath",
    "shortness of breath",
    "unconscious",
    "fainting",
    "passed out",
    "severe bleeding",
    "heavy bleeding",
    "vomiting blood",
    "blood in vomit",
    "seizure",
    "confusion",
    "stiff neck",
    "severe allergic reaction",
    "swelling of face",
    "severe stomach pain",
]

# Common conditions that MAY be associated with some of the symptoms.
# "symptoms" = which symptoms are often linked with it.
# To add a new condition, just add another item to this list!
CONDITIONS = [
    {
        "name": "Common cold",
        "symptoms": {"Runny nose", "Sore throat", "Cough", "Headache", "Fatigue"},
        "explanation": (
            "A mild illness caused by viruses that mostly affects the nose "
            "and throat. It often gets better by itself with rest."
        ),
    },
    {
        "name": "Flu-like illness",
        "symptoms": {"Fever", "Body aches", "Fatigue", "Headache", "Cough", "Sore throat"},
        "explanation": (
            "A viral illness that often comes on quickly with fever, body "
            "aches, and tiredness. It is usually stronger than a common cold."
        ),
    },
    {
        "name": "Throat irritation or throat infection",
        "symptoms": {"Sore throat", "Fever", "Cough", "Headache"},
        "explanation": (
            "The throat can become sore from viruses, bacteria, dry air, or "
            "smoke. A doctor can tell the cause."
        ),
    },
    {
        "name": "Seasonal allergies",
        "symptoms": {"Runny nose", "Cough", "Sore throat", "Headache"},
        "explanation": (
            "Dust, pollen, or pets can cause a runny nose and cough. "
            "Allergies usually do not cause a fever."
        ),
    },
    {
        "name": "Stomach upset from a stomach bug (viral gastroenteritis)",
        "symptoms": {"Nausea", "Vomiting", "Diarrhea", "Stomach pain", "Fever", "Body aches", "Fatigue"},
        "explanation": (
            "An infection of the stomach and gut, often spread through "
            "germs on hands, food, or water. The main risk is losing too "
            "much body fluid."
        ),
    },
    {
        "name": "Food-related stomach upset",
        "symptoms": {"Nausea", "Vomiting", "Stomach pain", "Diarrhea"},
        "explanation": (
            "Eating food that is spoiled, very oily, or hard to digest can "
            "upset the stomach for a short time."
        ),
    },
    {
        "name": "Indigestion or acid upset",
        "symptoms": {"Stomach pain", "Nausea"},
        "explanation": (
            "Eating too fast, eating spicy or heavy food, or stress can "
            "cause stomach discomfort and a feeling of sickness."
        ),
    },
    {
        "name": "Tension headache or dehydration",
        "symptoms": {"Headache", "Fatigue", "Body aches", "Nausea"},
        "explanation": (
            "Stress, lack of sleep, long screen time, or not drinking "
            "enough water can cause headaches and tiredness."
        ),
    },
    {
        "name": "General tiredness or lack of rest",
        "symptoms": {"Fatigue", "Body aches", "Headache"},
        "explanation": (
            "Poor sleep, stress, or too much physical work can leave the "
            "body feeling tired and achy."
        ),
    },
]

# Simple self-care tips for each symptom (no medicines).
SELF_CARE_TIPS = {
    "Fever": "Rest, drink plenty of fluids, and wear light clothing.",
    "Headache": "Rest in a quiet place, drink water, and take a break from screens.",
    "Cough": "Drink warm fluids, rest your voice, and stay away from smoke and dust.",
    "Sore throat": "Sip warm drinks and gargle with warm salt water.",
    "Runny nose": "Rest, drink fluids, and wash your hands often.",
    "Fatigue": "Get enough sleep and eat regular, balanced meals.",
    "Nausea": "Sip water slowly and eat light, simple foods when you feel ready.",
    "Vomiting": "Take small sips of water or oral rehydration drinks, and rest your stomach.",
    "Stomach pain": "Rest, avoid oily or spicy food, and eat light meals.",
    "Diarrhea": "Drink lots of fluids to avoid dehydration and wash your hands well.",
    "Body aches": "Rest, keep warm, and do gentle stretching if it feels okay.",
}

# Message when no symptoms are selected.
NO_SYMPTOMS_MESSAGE = (
    "Hello! Please select at least one symptom from the list, "
    "and I will share some general information."
)

# Message shown for emergency warning signs.
EMERGENCY_MESSAGE = (
    "### ⚠️ This could be a medical emergency\n\n"
    "Please call your local emergency number or go to the nearest hospital "
    "**right now**. If someone is with you, ask them to help you.\n\n"
    "Do not wait for an online tool to tell you what to do."
)

# Safety note added at the end of normal results.
DISCLAIMER = (
    "*Note: This is a student project that gives general information only. "
    "It cannot diagnose diseases or recommend medicines. "
    "Please talk to a doctor or healthcare professional for personal advice.*"
)


# ----------------------------------------------------------
# PART 2: Small helper functions
# ----------------------------------------------------------

def _clean_symptoms(selected_symptoms):
    """
    Turn the input into a clean list of text items.
    Accepts a list (or a single string) and ignores empty values.
    """
    if selected_symptoms is None:
        return []
    if isinstance(selected_symptoms, str):
        selected_symptoms = [selected_symptoms]

    cleaned = []
    for item in selected_symptoms:
        if isinstance(item, str) and item.strip() != "":
            cleaned.append(item.strip())
    return cleaned


def _has_emergency_sign(symptom_list):
    """Return True if any item contains an emergency warning sign."""
    for item in symptom_list:
        # Lowercase and fix curly apostrophes so "can't" matches.
        text = item.lower().replace("’", "'").replace("_", " ")
        for sign in EMERGENCY_WARNING_SIGNS:
            if sign in text:
                return True
    return False


def _match_to_supported(symptom_list):
    """
    Match the user's items to our supported symptom names.
    Returns two lists: (known symptoms, unknown items).
    """
    # Make a dictionary like {"sore throat": "Sore throat"}
    lookup = {name.lower(): name for name in SUPPORTED_SYMPTOMS}

    known = []
    unknown = []
    for item in symptom_list:
        key = item.lower().replace("_", " ").strip()
        if key in lookup:
            if lookup[key] not in known:  # avoid duplicates
                known.append(lookup[key])
        else:
            unknown.append(item)
    return known, unknown


def _find_related_conditions(known_symptoms):
    """
    Count how many selected symptoms match each condition and return
    the best matches (at most 3).
    """
    selected = set(known_symptoms)

    # With 1 symptom we need 1 match; with 2 or more we need at least 2.
    minimum_matches = 1 if len(selected) == 1 else 2

    results = []
    for condition in CONDITIONS:
        matches = selected & condition["symptoms"]  # symptoms in common
        if len(matches) >= minimum_matches:
            results.append((len(matches), condition, sorted(matches)))

    # Sort best matches first. If two conditions have the same number of
    # matches, Python keeps them in the same order as the CONDITIONS list,
    # so put the most common conditions at the top of that list.
    results.sort(key=lambda r: r[0], reverse=True)
    return results[:3]


def _see_doctor_soon_notes(known_symptoms):
    """Return extra warning notes for certain symptom combinations."""
    selected = set(known_symptoms)
    notes = []

    if "Vomiting" in selected and "Diarrhea" in selected:
        notes.append(
            "Vomiting and diarrhea together can cause dehydration "
            "(losing too much body fluid). Please see a doctor if you "
            "cannot keep fluids down, feel very weak or dizzy, or pass "
            "very little urine."
        )
    elif "Fever" in selected and ("Vomiting" in selected or "Diarrhea" in selected):
        notes.append(
            "Fever together with vomiting or diarrhea is worth checking "
            "with a doctor, especially if it continues."
        )

    if len(selected) >= 4:
        notes.append(
            "You selected several symptoms at once. It is a good idea "
            "to get checked by a healthcare professional."
        )
    return notes


# ----------------------------------------------------------
# PART 3: The main function used by your Streamlit app
# ----------------------------------------------------------

def check_symptoms(selected_symptoms):
    """
    Take a list of symptoms and return a friendly text (Markdown format).

    Order of checks:
    1. No symptoms selected
    2. Emergency warning signs  (most important!)
    3. Possible related conditions
    4. Self-care tips and when to see a doctor
    """

    # Step 1: Clean the input and check if anything was selected.
    symptom_list = _clean_symptoms(selected_symptoms)
    if len(symptom_list) == 0:
        return NO_SYMPTOMS_MESSAGE

    # Step 2: Emergency check comes FIRST.
    if _has_emergency_sign(symptom_list):
        return EMERGENCY_MESSAGE

    # Step 3: Match the input to the symptoms we support.
    known, unknown = _match_to_supported(symptom_list)
    if len(known) == 0:
        return (
            "Sorry, I do not recognize those symptoms. "
            "Please choose from this list: "
            + ", ".join(SUPPORTED_SYMPTOMS)
            + ".\n\nFor anything else, please consult a healthcare professional."
        )

    # Step 4: Build the answer piece by piece.
    lines = []
    lines.append("### Your selected symptoms")
    lines.append(", ".join(known))
    lines.append("")

    # Possible related conditions
    lines.append("### Conditions that may be associated with these symptoms")
    lines.append(
        "These are only general possibilities, **not a diagnosis**. "
        "Many different causes can look similar."
    )
    lines.append("")
    related = _find_related_conditions(known)
    if related:
        for _, condition, matched in related:
            lines.append(
                f"- **{condition['name']}**: {condition['explanation']} "
                f"(Matches: {', '.join(matched)})"
            )
    else:
        lines.append(
            "- I could not find a clear general match. "
            "Please talk to a healthcare professional."
        )
    lines.append("")

    # Self-care tips
    lines.append("### General self-care tips")
    for symptom in known:
        lines.append(f"- **{symptom}:** {SELF_CARE_TIPS[symptom]}")
    lines.append(
        "- **For everyone:** Get plenty of rest, drink enough water, and "
        "wash your hands often. If you want to use any medicine, ask a "
        "doctor or pharmacist first."
    )
    lines.append("")

    # When to see a doctor
    lines.append("### When to see a doctor")
    for note in _see_doctor_soon_notes(known):
        lines.append(f"- {note}")
    lines.append(
        "- See a doctor if your symptoms last more than 2 to 3 days, get "
        "worse, or keep coming back."
    )
    lines.append(
        "- Please get checked sooner if the person is a baby, a young "
        "child, an older adult, pregnant, or has a long-term health "
        "condition."
    )
    lines.append(
        "- Get emergency help right away if you have chest pain, trouble "
        "breathing, fainting, confusion, a stiff neck, or severe bleeding."
    )
    lines.append("")

    # Mention anything we did not understand.
    if unknown:
        lines.append(
            "*I did not recognize: " + ", ".join(unknown)
            + ". I only used the symptoms I know.*"
        )
        lines.append("")

    lines.append(DISCLAIMER)
    return "\n".join(lines)


# ----------------------------------------------------------
# PART 4: Optional quick test in the terminal
# Run with:  python symptoms.py
# (This part does NOT run when you import the file in Streamlit.)
# ----------------------------------------------------------
if __name__ == "__main__":
    print("Doctor AI symptom checker test mode.")
    print("Supported symptoms:", ", ".join(SUPPORTED_SYMPTOMS))
    text = input("Type symptoms separated by commas (or press Enter): ")
    items = [part.strip() for part in text.split(",")]
    print()
    print(check_symptoms(items))
