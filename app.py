import streamlit as st
from coach import generate_habits, generate_motivation, USE_MOCK
from tracker import init_db, get_today_habits, save_habits, mark_habit_done
from datetime import date

# Init DB
init_db()

# Page Config
st.set_page_config(page_title="AI Habit Coach", page_icon="🧠", layout="centered")
st.title("🧠 AI Habit Coach")
st.caption("Build better habits — one small action at a time.")

# 🔧 Mock Mode Indicator
if USE_MOCK:
    st.warning("⚠️ Mock Mode Enabled: Using sample habits & motivation (no OpenAI key detected)")

# 📝 Goal Input Section
st.markdown("### 🎯 Set Your Goal")
with st.form("goal_form"):
    goal = st.text_input("What is your current focus or goal?", placeholder="e.g. Become more focused, healthier, etc.")
    submitted = st.form_submit_button("💡 Generate Habit Suggestions")
    if submitted and goal:
        with st.spinner("Asking your AI coach..."):
            habits = generate_habits(goal)
            if habits:
                save_habits(habits)
                st.success("✅ Habits generated and saved!")
            else:
                st.error("Something went wrong. Try again!")

# 📋 Today's Habits Section
st.markdown("### 📅 Your Daily Habits")
today = date.today().isoformat()
habits_today = get_today_habits()

if not habits_today:
    st.info("No habits for today yet. Set a goal above to get started!")
else:
    for habit_id, habit_text, done in habits_today:
        checked = st.checkbox(habit_text, value=done, key=f"habit_{habit_id}")
        if checked and not done:
            mark_habit_done(habit_id, today)

# 💬 Motivation Section
st.markdown("### 🔥 Need Motivation?")
if st.button("⚡ Motivate Me"):
    with st.spinner("Fetching a motivational boost..."):
        motivation = generate_motivation(goal or "being your best self")
        st.markdown(f"> 💬 *{motivation}*")

# 📌 Footer
st.markdown("---")
st.caption("Made with ❤️ by [Your Name] • [GitHub](https://github.com/yourusername/ai-habit-coach)")
