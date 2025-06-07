
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Society Simulator", layout="wide")

st.title("🤖 AI-Automated Future Society Simulator")
st.markdown("Explore how AI automation, UBI, and taxation affect income, stability, and inequality over time.")

# Sidebar parameters
years = st.sidebar.slider("Years to Simulate", 10, 50, 30)
population = st.sidebar.slider("Population Size", 1000, 20000, 5000, step=1000)
start_automation = st.sidebar.slider("Initial AI Automation Rate (%)", 0, 100, 30) / 100
automation_growth = st.sidebar.slider("Automation Growth per Year (%)", 0, 10, 2) / 100
ubi_toggle = st.sidebar.checkbox("Enable Universal Basic Income", value=True)
ubi_amount = st.sidebar.number_input("UBI Amount (Yearly per Person)", value=10000) if ubi_toggle else 0
ai_tax_rate = st.sidebar.slider("AI Tax Rate (%)", 0, 100, 30) / 100

# Simulation variables
avg_incomes = []
stability_scores = []
gini_scores = []

for year in range(years):
    automation_rate = min(1.0, start_automation + automation_growth * year)
    employed_ratio = 1.0 - automation_rate
    employed_count = int(population * employed_ratio)
    unemployed_count = population - employed_count

    ai_output = 50000 * population * automation_rate
    tax_collected = ai_output * ai_tax_rate
    ubi_per_person = tax_collected / population if ubi_toggle else 0

    employed_income = np.random.randint(25000, 100000, employed_count) + ubi_per_person
    unemployed_income = np.full(unemployed_count, ubi_per_person)
    all_income = np.concatenate([employed_income, unemployed_income])

    avg_income = np.mean(all_income)
    avg_incomes.append(avg_income)

    stability = max(0, 100 - (unemployed_count / population) * 50 - (50000 - avg_income) / 1000)
    stability_scores.append(stability)

    sorted_income = np.sort(all_income)
    index = np.arange(1, population + 1)
    gini = (np.sum((2 * index - population - 1) * sorted_income)) / (population * np.sum(sorted_income))
    gini_scores.append(gini)

# Plotting
st.subheader("📈 Simulation Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Average Income Over Time**")
    st.line_chart(avg_incomes)

with col2:
    st.markdown("**Social Stability Over Time**")
    st.line_chart(stability_scores)

with col3:
    st.markdown("**Gini Coefficient Over Time**")
    st.line_chart(gini_scores)

st.markdown("Created with ❤️ by ChatGPT + Streamlit")
