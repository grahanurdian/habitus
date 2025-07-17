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

def generate_habits(goal: str, mode: str = "Mock") -> str:
    if mode == "Mock":
        return f"""1. Wake up at the same time every day.
2. Write 3 sentences about your goal in a journal.
3. Drink a full glass of water after waking up.
(Mock response for goal: {goal})"""

    elif mode == "G4F":
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": HABIT_PROMPT_TEMPLATE.format(goal=goal)}
                ]
            )
            return response
        except Exception as e:
            return f"Error using G4F: {e}"

    elif mode == "OpenAI":
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": HABIT_PROMPT_TEMPLATE.format(goal=goal)}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error using OpenAI: {e}"

    else:
        return "❌ Invalid mode selected. Please choose Mock, G4F, or OpenAI."