import streamlit as st
from coach import generate_habits, generate_motivation
from tracker import (
    init_db,
    get_today_habits,
    save_habits,
    mark_habit_done,
    get_habit_status
)
from datetime import date

# Init DB
init_db()

st.set_page_config(page_title="Habitus", page_icon="🧠")

st.title("🧠 Habitus: AI Habit Coach")
st.subheader("Build better habits with the help of AI")

# Goal input
st.markdown("### 1. What's your goal?")
goal = st.text_input("E.g. I want to be more focused, healthier, or consistent")

if st.button("Generate Habits") and goal:
    with st.spinner("Thinking..."):
        habits = generate_habits(goal)
        if habits:
            save_habits(habits)
            st.success("Your habits have been generated and saved!")

# Show today habits
st.markdown("### 2. Today's Habits")
today = date.today().isoformat()
habits_today = get_today_habits()

if habits_today:
    for habit_id, habit_text, done in habits_today:
        checked = st.checkbox(habit_text, value=done, key=habit_id)
        if checked and not done:
            mark_habit_done(habit_id, today)

# Motivational message
st.markdown("### 3. Need a little boost?")
if st.button("Motivate Me"):
    with st.spinner("Getting encouragement..."):
        motivation = generate_motivation(goal=goal)
        st.info(motivation)