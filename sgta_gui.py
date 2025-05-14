import streamlit as st
import random
import json
import os

HISTORY_FILE = "group_history.json"

def load_history(total_groups, reset=False):
    if reset or not os.path.exists(HISTORY_FILE):
        return {str(i): 0 for i in range(1, total_groups + 1)}
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    # Ensure new groups are initialized
    for i in range(1, total_groups + 1):
        if str(i) not in history:
            history[str(i)] = 0
    return history


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def update_history(history, selected_groups):
    for g in selected_groups:
        history[str(g)] += 1


def select_groups(history, num_to_select):
    # Sort by fewest presentations
    sorted_groups = sorted(history.items(), key=lambda x: x[1])
    min_count = sorted_groups[0][1]
    eligible = [int(g) for g, count in sorted_groups if count == min_count]

    # Expand pool if needed
    i = len(eligible)
    while i < num_to_select and i < len(sorted_groups):
        next_count = sorted_groups[i][1]
        more = [int(g) for g, count in sorted_groups
                if count == next_count and int(g) not in eligible]
        eligible += more
        i = len(eligible)

    return random.sample(eligible, min(num_to_select, len(eligible)))


# Streamlit UI
st.title("🎓 SGTA Group Selector")

total_groups = st.number_input("Total number of groups", min_value=1, step=1)
reset = st.checkbox("Reset history for new SGTA")

if st.button("Load / Reset History"):
    st.session_state['history'] = load_history(total_groups, reset=reset)
    save_history(st.session_state['history'])

if 'history' in st.session_state:
    history = st.session_state['history']

    st.subheader("📊 Group History")
    st.table({k: history[k] for k in sorted(history, key=int)})

    num_to_select = st.number_input(
        "How many groups to select this session?", min_value=1, step=1)

    if st.button("Select Groups"):
        selected = select_groups(history, num_to_select)
        st.success(f"🎤 Selected groups: {selected}")
        update_history(history, selected)
        save_history(history)
        st.session_state['history'] = history
