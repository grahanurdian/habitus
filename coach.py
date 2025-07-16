import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

USE_MOCK = not api_key  # Enable mock mode if no API key

# Mock habit suggestions
MOCK_HABITS = [
    "Write down 3 things you're grateful for",
    "Spend 10 minutes focused on a single task",
    "Take a 5-minute walk without distractions",
    "Review your goals for 2 minutes",
    "Plan your top 1 task for tomorrow"
]

# Mock motivation
MOCK_MOTIVATION = "Progress is progress, no matter how small. Keep showing up — you're doing great!"

def generate_habits(goal: str) -> list[str]:
    if USE_MOCK:
        return MOCK_HABITS

    import openai
    openai.api_key = api_key

    prompt = f"""
    You are a helpful and realistic productivity coach.

    A user has this goal: "{goal}"

    Suggest 3 to 5 daily micro-habits they can realistically start doing to achieve this goal.
    Respond in bullet points without explanations.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        content = response['choices'][0]['message']['content']
        habits = [line.strip("•- ").strip() for line in content.strip().split("\n") if line.strip()]
        return habits

    except Exception as e:
        print("Error generating habits:", e)
        return MOCK_HABITS

def generate_motivation(goal: str) -> str:
    if USE_MOCK:
        return MOCK_MOTIVATION

    import openai
    openai.api_key = api_key

    prompt = f"""
    You are a friendly, encouraging AI coach.

    The user is working toward this goal: "{goal}"

    Give a short, warm motivational message (1–2 sentences) to keep them going.
    """

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
        return MOCK_MOTIVATION
