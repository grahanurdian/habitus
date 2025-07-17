import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Check for keys
api_key = os.getenv("OPENAI_API_KEY")
use_g4f = os.getenv("USE_G4F") == "1"

USE_MOCK = not api_key and not use_g4f

if not USE_MOCK and use_g4f:
    import g4f
elif not USE_MOCK:
    import openai
    openai.api_key = api_key

HABIT_PROMPT_TEMPLATE = """
You are a helpful habit coach AI.

Help the user create 3 healthy, achievable daily habits based on their personal goal below.

Be clear and concise. Focus on consistency, not intensity.

Goal: {goal}

Respond in numbered list format.
"""

def generate_habits(goal: str) -> list[str]:
    if USE_MOCK:
        return [
            "Wake up at the same time every day.",
            "Write 3 sentences about your goal in a journal.",
            "Drink a full glass of water after waking up.",
            f"(Mock response for goal: {goal})"
        ]
    
    elif use_g4f:
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": HABIT_PROMPT_TEMPLATE.format(goal=goal)}
                ]
            )
            content = response.choices[0].message.content
            return content.strip().split("\n")  # Converts to list of lines
        except Exception as e:
            return [f"⚠️ Error using G4F: {e}"]  # Return list even if it's error

    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": HABIT_PROMPT_TEMPLATE.format(goal=goal)}
                ]
            )
            content = response.choices[0].message.content
            return content.strip().split("\n")
        except Exception as e:
            return [f"⚠️ Error using OpenAI: {e}"]
    
def generate_motivation(goal: str, mode: str = "Auto") -> str:
    if mode == "Mock":
        return f"Keep going with your goal to '{goal}' — every step counts!"
    elif mode == "G4F":
        # Dummy placeholder for G4F call
        return f"[G4F] You're doing great! Keep pushing toward '{goal}'!"
    elif mode == "OpenAI":
        # Placeholder for OpenAI call
        return f"[OpenAI] Remember why you started: '{goal}'. Keep going!"
    else:
        return f"Stay consistent with your goal to '{goal}'!"
