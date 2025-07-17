import streamlit as st
from coach import generate_habits, generate_motivation
from tracker import init_db, get_today_habits, save_habits, mark_habit_done
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

# Auto-detect available mode
auto_mode = "OpenAI" if os.getenv("OPENAI_API_KEY") else ("G4F" if os.getenv("USE_G4F") == "1" else "Mock")

# Sidebar mode selection
st.sidebar.markdown("## ⚙️ Settings")
user_mode = st.sidebar.selectbox("Select Mode", options=["Auto", "OpenAI", "G4F", "Mock"], index=0)

# Final mode decision
if user_mode == "Auto":
    mode = auto_mode
else:
    mode = user_mode

# Show current mode
st.sidebar.markdown(f"### 🤖 Active Mode: `{mode}`")

# Init DB
init_db()

# Page Config
st.set_page_config(page_title="Habitus - AI Habit Coach", page_icon="🧠", layout="centered")
st.title("🧠 Habitus - AI Habit Coach")
st.caption("Build better habits — one small action at a time.")

if mode == "Mock":
    st.warning("⚠️ Mock Mode Enabled: Using sample habits & motivation (no real AI model used)")
elif mode == "G4F":
    st.info("⚠️ G4F Mode Enabled: Using free GPT backend via unofficial API")
elif mode == "OpenAI":
    st.success("✅ OpenAI Mode Enabled: Using official OpenAI API")

# 📝 Goal Input Section
st.markdown("### 🎯 Set Your Goal")
with st.form("goal_form"):
    goal = st.text_input("What is your current focus or goal?", placeholder="e.g. Become more focused, healthier, etc.")
    submitted = st.form_submit_button("💡 Generate Habit Suggestions")

    if submitted and goal:
        with st.spinner("Asking your AI coach..."):
            habits = generate_habits(goal, mode=mode)

            # Check if valid list of habits
            if isinstance(habits, list) and all(isinstance(h, str) and len(h) > 2 for h in habits):
                for habit in habits:
                    st.write("✅", habit)
                save_habits(habits)
                st.success("✅ Habits generated and saved!")
            else:
                st.error("❌ Something went wrong generating habits. Try switching mode or changing your goal.")

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
        motivation = generate_motivation(goal or "being your best self", mode=mode)
        st.markdown(f"> 💬 *{motivation}*")

# 📌 Footer
st.markdown("---")
st.caption("Made with ❤️ by ootofthebox • [GitHub](https://github.com/grahanurdian/habitus)")
