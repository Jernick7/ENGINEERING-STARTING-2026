import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# --- CONFIGURATION & CONSTANTS ---
DB_FILE = "chores_db.json"
PARENT_PASSWORD = "admin123"  # Change this to your preferred secret
USERS = ["Jernick", "Bave"]
CHORE_VALUES = {
    "Taking out the trash": 1,
    "Laundry": 2,
    "Cleaning the floor": 3,
    "Cleaning dishes": 3
}

# --- DATA PERSISTENCE FUNCTIONS ---
def load_data():
    """Load chore history from the JSON file."""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(logs):
    """Save chore history to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# --- APP LAYOUT ---
st.set_page_config(page_title="Chore Tracker & Rewards", page_icon="🏆")

st.title("🏆 Chore Tracker & Reward System")
st.markdown(f"Welcome **Jernick** and **Bave**! Complete chores to earn points and climb the leaderboard.")

# --- LOAD CURRENT DATA ---
chore_logs = load_data()

# --- SIDEBAR: LOG NEW CHORE ---
st.sidebar.header("📝 Log a Chore")
with st.sidebar.form("chore_form", clear_on_submit=True):
    selected_user = st.selectbox("Who completed the chore?", USERS)
    selected_date = st.date_input("Date", datetime.now())
    selected_chore = st.selectbox("Select Chore", list(CHORE_VALUES.keys()))
    
    st.divider()
    st.subheader("Parental Approval")
    verification_pwd = st.text_input("Enter Parent Password", type="password")
    
    submit_button = st.form_submit_button("Submit & Verify")

if submit_button:
    if verification_pwd == PARENT_PASSWORD:
        # Create new entry
        new_entry = {
            "user": selected_user,
            "date": str(selected_date),
            "chore": selected_chore,
            "points": CHORE_VALUES[selected_chore],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Update and save
        chore_logs.append(new_entry)
        save_data(chore_logs)
        st.sidebar.success(f"Verified! {CHORE_VALUES[selected_chore]} points added to {selected_user}.")
    else:
        st.sidebar.error("Incorrect Parent Password. Points not logged.")

# --- CALCULATION LOGIC ---
# Calculate totals
scores = {user: 0 for user in USERS}
for log in chore_logs:
    scores[log['user']] += log['points']

j_score = scores["Jernick"]
b_score = scores["Bave"]

# --- LEADERBOARD SECTION ---
st.header("📊 Current Leaderboard")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Jernick's Points", value=f"{j_score} pts")

with col2:
    st.metric(label="Bave's Points", value=f"{b_score} pts")

st.divider()

# --- VICTORY LOGIC ---
if j_score > 0 or b_score > 0:
    if j_score > b_score:
        st.balloons()
        st.success(f"🔥 **Jernick** is currently in the lead!")
    elif b_score > j_score:
        st.balloons()
        st.success(f"🔥 **Bave** is currently in the lead!")
    else:
        st.info("🤝 It's a tie! Keep up the hard work!")
else:
    st.write("No chores logged yet this week. Start cleaning to earn points!")

# --- DATA HISTORY TABLE ---
with st.expander("See Activity Log"):
    if chore_logs:
        df = pd.DataFrame(chore_logs)
        # Format for better display
        df = df[['date', 'user', 'chore', 'points']]
        st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)
    else:
        st.write("No history available.")

# --- CSS STYLING (Optional) ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 45px;
        color: #F63366;
    }
    </style>
    """, unsafe_allow_html=True)