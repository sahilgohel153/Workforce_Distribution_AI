import streamlit as st
from main import process_csv, get_top_candidates, apply_filters, load_default_dataset
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="WorkforceDistribution.AI", layout="wide")
st.title("WorkforceDistribution.AI: Candidate Role & Suitability Analyzer")
st.markdown("""
Upload a CSV of candidates or use the default dataset. Filter by skill, salary, or job role. View top candidates per role and analyze skill/salary distributions.
""")

# Sidebar for dataset selection
st.sidebar.header("Dataset Options")
use_default = st.sidebar.checkbox("Use default dataset (WA_Fn-UseC_-HR-Employee-Attrition.csv)", value=True)

if use_default:
    df = load_default_dataset()
else:
    uploaded_file = st.sidebar.file_uploader("Upload Candidate CSV", type=["csv"])
    if uploaded_file:
        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        df = process_csv("temp.csv")
    else:
        st.warning("Please upload a CSV file or select the default dataset.")
        st.stop()

# Show analyzed candidates
display_cols = [col for col in df.columns if col not in ["Skill Ratings"]]

# --- Dashboard Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Candidates", len(df))
col2.metric("Unique Roles", df['Assigned Role'].nunique() if 'Assigned Role' in df else 0)
col3.metric("Avg. Suitability Score", f"{df['Suitability Score'].mean():.2f}" if 'Suitability Score' in df else "N/A")

# --- Filtering ---
st.sidebar.header("Filter Candidates")
skill = st.sidebar.text_input("Filter by Skill")
min_salary = st.sidebar.number_input("Min Salary", value=0)
max_salary = st.sidebar.number_input("Max Salary", value=0)
role = st.sidebar.text_input("Filter by Role")

filtered_df = apply_filters(
    df,
    skill=skill if skill else None,
    min_salary=min_salary if min_salary > 0 else None,
    max_salary=max_salary if max_salary > 0 else None,
    role=role if role else None
)

# --- Filtered Candidates Table ---
st.subheader(":busts_in_silhouette: Filtered Candidates")
if not filtered_df.empty:
    st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("No candidates match the current filters.")

# --- Top Candidates per Role ---
st.subheader(":trophy: Top Candidates per Role")
top_candidates = get_top_candidates(filtered_df)
if top_candidates:
    for role, candidates in top_candidates.items():
        if candidates:
            with st.expander(f"{role}"):
                st.dataframe(candidates, use_container_width=True, hide_index=True)
else:
    st.info("No top candidates to display.")

# --- Skill Distribution Chart ---
st.subheader(":bar_chart: Skill Distribution (Top 10 Skills)")
if 'Skills' in filtered_df.columns and not filtered_df.empty:
    skill_series = filtered_df['Skills'].str.split(',').explode().str.strip()
    skill_counts = skill_series.value_counts().head(10)
    if not skill_counts.empty:
        fig, ax = plt.subplots()
        skill_counts.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel('Number of Candidates')
        ax.set_xlabel('Skill')
        ax.set_title('Top 10 Skills')
        st.pyplot(fig)
    else:
        st.info("No skill data available to plot.")
else:
    st.info("No skill data available to plot.")

# --- Salary vs. Suitability Score Chart ---
st.subheader(":chart_with_upwards_trend: Salary vs. Suitability Score")
if 'Expected Salary' in filtered_df.columns and 'Suitability Score' in filtered_df.columns and not filtered_df.empty:
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df['Expected Salary'], filtered_df['Suitability Score'], alpha=0.6, c='green')
    ax2.set_xlabel('Expected Salary')
    ax2.set_ylabel('Suitability Score')
    ax2.set_title('Salary vs. Suitability Score')
    st.pyplot(fig2)
else:
    st.info("No data to plot.")

# --- Candidates per Role Pie Chart ---
st.subheader(":pie: Candidates per Role")
if 'Assigned Role' in filtered_df.columns and not filtered_df.empty:
    role_counts = filtered_df['Assigned Role'].value_counts()
    if not role_counts.empty:
        fig3, ax3 = plt.subplots()
        ax3.pie(role_counts, labels=role_counts.index, autopct='%1.1f%%', startangle=140)
        ax3.axis('equal')
        st.pyplot(fig3)
    else:
        st.info("No role data to plot.")
else:
    st.info("No role data to plot.") 