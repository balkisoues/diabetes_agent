import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Diabetes Lifestyle Tracker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .log-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 2rem;
    }
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #155724;
        font-weight: 600;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Setup: Persistent storage
# -----------------------------
LOG_FILE = Path("logs.json")

def load_logs():
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {"food": [], "water": [], "sleep": [], "activity": []}

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

LOGS = load_logs()

# -----------------------------
# Header Section
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🏥 Diabetes Lifestyle Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.1rem;'>Track your daily health activities with ease</p>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/health-graph.png", width=150)
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Meals Logged", len(LOGS["food"]))
    st.metric("Water Entries", len(LOGS["water"]))
    st.metric("Sleep Records", len(LOGS["sleep"]))
    st.metric("Activities Logged", len(LOGS["activity"]))
    st.markdown("---")
    action = st.radio(
        "Choose an action:",
        ["🍽️ Log Food", "💧 Log Water", "😴 Log Sleep", "🏃 Log Activity", "📈 Show Summary"],
        label_visibility="collapsed"
    )

# -----------------------------
# Main Content Area
# -----------------------------
if action == "🍽️ Log Food":
    st.markdown("### 🍽️ Log Your Meal")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        food = st.text_input("What did you eat?", placeholder="e.g., Grilled chicken with vegetables", label_visibility="collapsed")
    
    with col2:
        if st.button("✅ Log Food", type="primary"):
            if food:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                LOGS["food"].append({"item": food, "timestamp": timestamp})
                save_logs(LOGS)
                st.success(f"✨ Logged meal: {food}")
                st.balloons()
            else:
                st.warning("Please enter a food item!")

elif action == "💧 Log Water":
    st.markdown("### 💧 Log Water Intake")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        water = st.text_input("How much water?", placeholder="e.g., 2 cups, 500ml", label_visibility="collapsed")
    
    with col2:
        if st.button("✅ Log Water", type="primary"):
            if water:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                LOGS["water"].append({"amount": water, "timestamp": timestamp})
                save_logs(LOGS)
                st.success(f"💦 Logged water: {water}")
            else:
                st.warning("Please enter water amount!")

elif action == "😴 Log Sleep":
    st.markdown("### 😴 Log Sleep Duration")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        hours = st.number_input("Hours slept", min_value=0.0, max_value=24.0, step=0.5, format="%.1f")
    
    with col2:
        quality = st.selectbox("Sleep quality", ["Excellent", "Good", "Fair", "Poor"])
    
    with col3:
        st.write("")
        st.write("")
        if st.button("✅ Log Sleep", type="primary"):
            timestamp = datetime.now().strftime("%Y-%m-%d")
            LOGS["sleep"].append({"hours": hours, "quality": quality, "timestamp": timestamp})
            save_logs(LOGS)
            st.success(f"🌙 Logged sleep: {hours} hours ({quality})")

elif action == "🏃 Log Activity":
    st.markdown("### 🏃 Log Physical Activity")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        activity = st.text_input("What activity?", placeholder="e.g., Running, Walking, Yoga", label_visibility="collapsed")
    
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=300, step=5)
    
    with col3:
        st.write("")
        st.write("")
        if st.button("✅ Log Activity", type="primary"):
            if activity:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                LOGS["activity"].append({"type": activity, "duration": duration, "timestamp": timestamp})
                save_logs(LOGS)
                st.success(f"🎯 Logged activity: {activity} for {duration} min")
            else:
                st.warning("Please enter an activity!")

elif action == "📈 Show Summary":
    st.markdown("### 📈 Your Health Summary")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Food", "💧 Water", "😴 Sleep", "🏃 Activity"])
    
    with tab1:
        if LOGS["food"]:
            for idx, entry in enumerate(reversed(LOGS["food"])):
                if isinstance(entry, dict):
                    st.markdown(f"""
                        <div class='log-item'>
                            <strong>{entry['item']}</strong><br>
                            <small style='color: #666;'>⏰ {entry['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class='log-item'><strong>{entry}</strong></div>""", unsafe_allow_html=True)
        else:
            st.info("No food logged yet. Start tracking your meals!")
    
    with tab2:
        if LOGS["water"]:
            for idx, entry in enumerate(reversed(LOGS["water"])):
                if isinstance(entry, dict):
                    st.markdown(f"""
                        <div class='log-item'>
                            <strong>{entry['amount']}</strong><br>
                            <small style='color: #666;'>⏰ {entry['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class='log-item'><strong>{entry}</strong></div>""", unsafe_allow_html=True)
        else:
            st.info("No water logged yet. Stay hydrated!")
    
    with tab3:
        if LOGS["sleep"]:
            for idx, entry in enumerate(reversed(LOGS["sleep"])):
                if isinstance(entry, dict):
                    st.markdown(f"""
                        <div class='log-item'>
                            <strong>{entry['hours']} hours</strong> - Quality: {entry.get('quality', 'N/A')}<br>
                            <small style='color: #666;'>📅 {entry['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class='log-item'><strong>{entry} hours</strong></div>""", unsafe_allow_html=True)
        else:
            st.info("No sleep logged yet. Track your rest!")
    
    with tab4:
        if LOGS["activity"]:
            for idx, entry in enumerate(reversed(LOGS["activity"])):
                if isinstance(entry, dict):
                    st.markdown(f"""
                        <div class='log-item'>
                            <strong>{entry['type']}</strong> - {entry.get('duration', 'N/A')} minutes<br>
                            <small style='color: #666;'>⏰ {entry['timestamp']}</small>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class='log-item'><strong>{entry}</strong></div>""", unsafe_allow_html=True)
        else:
            st.info("No activities logged yet. Get moving!")
    
    st.markdown("---")
    if st.button("🗑️ Clear All Logs", type="secondary"):
        LOGS = {"food": [], "water": [], "sleep": [], "activity": []}
        save_logs(LOGS)
        st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>💜 Stay healthy and track your progress daily!</p>", unsafe_allow_html=True)
