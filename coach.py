import os
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt template for generating habits
HABIT_PROMPT_TEMPLATE = """
You are a helpful and realistic productivity coach.

A user has this goal: "{goal}"

Suggest 3 to 5 daily micro-habits they can realistically start doing to achieve this goal.
Make sure each habit is:
- Short
- Actionable
- Clear

Respond in bullet points without explanations.
"""

# Prompt template for motivation
MOTIVATION_PROMPT_TEMPLATE = """
You are a friendly, encouraging AI coach.

The user is working toward this goal: "{goal}"

Give a short, warm motivational message (1-2 sentences) to keep them going.
Make it personal, empathetic, and positive.
"""

def generate_habits(goal: str) -> list[str]:
    prompt = HABIT_PROMPT_TEMPLATE.format(goal=goal)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change if using another model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        content = response['choices'][0]['message']['content']
        # Parse bullet points
        habits = [line.strip("•- ").strip() for line in content.strip().split("\n") if line.strip()]
        return habits

    except Exception as e:
        print("Error generating habits:", e)
        return []

def generate_motivation(goal: str) -> str:
    prompt = MOTIVATION_PROMPT_TEMPLATE.format(goal=goal)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=60
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print("Error generating motivation:", e)
        return "You're doing great—just keep showing up!"