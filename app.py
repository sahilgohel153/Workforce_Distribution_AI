import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="WorkforceDistribution.AI", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🔍 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "🏠 Dashboard",
        "👤 Employee Assessment",
        "📋 Job Recommendation",
        "📊 Analytics",
        "⚙️ Model Training",
        "🎯 Skill Rating"
    ]
)

# --- Load Data ---
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

def transform_ibm_dataset(df):
    names = df['EmployeeNumber'].astype(str)
    skills = df[['JobRole', 'OverTime', 'EducationField']].astype(str).agg(','.join, axis=1)
    skill_counts = skills.str.count(',') + 1
    skill_ratings = skill_counts.apply(lambda n: ','.join([str(np.random.randint(7, 11)) for _ in range(n)]))
    preferred_job_role = df['JobRole']
    expected_salary = (df['MonthlyIncome'] * 12).astype(int)
    transformed = pd.DataFrame({
        'Name': names,
        'Skills': skills,
        'Skill Ratings': skill_ratings,
        'Preferred Job Role': preferred_job_role,
        'Expected Salary': expected_salary
    })
    return transformed

st.sidebar.header("Dataset Options")
use_default = st.sidebar.checkbox("Use default dataset (WA_Fn-UseC_-HR-Employee-Attrition.csv)", value=True)

if use_default:
    df = load_data("WA_Fn-UseC_-HR-Employee-Attrition.csv")
else:
    uploaded_file = st.sidebar.file_uploader("Upload Employee CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file or select the default dataset.")
        st.stop()

# --- AI Model: Predict Salary ---
features = [
    'Age', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction', 'JobInvolvement',
    'JobLevel', 'JobSatisfaction', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike',
    'PerformanceRating', 'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears',
    'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
    'YearsSinceLastPromotion', 'YearsWithCurrManager'
]
target = 'MonthlyIncome'
df_model = df.dropna(subset=features + [target])
X = df_model[features]
y = df_model[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
df['AI_Predicted_MonthlyIncome'] = model.predict(df[features].fillna(0))
df['AI_Predicted_AnnualSalary'] = (df['AI_Predicted_MonthlyIncome'] * 12).astype(int)
df['Actual_AnnualSalary'] = (df['MonthlyIncome'] * 12).astype(int)

# --- Page Content ---
if page == "🏠 Dashboard":
    st.title("WorkforceDistribution.AI: AI-Powered Salary Prediction & Candidate Analyzer")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(df))
    col2.metric("Avg. Actual Salary", f"${df['Actual_AnnualSalary'].mean():,.0f}")
    col3.metric("Avg. Predicted Salary", f"${df['AI_Predicted_AnnualSalary'].mean():,.0f}")
    st.subheader(":busts_in_silhouette: Employee Data with AI Salary Prediction")
    st.dataframe(df[['EmployeeNumber', 'JobRole', 'PerformanceRating', 'Actual_AnnualSalary', 'AI_Predicted_AnnualSalary']], use_container_width=True)
    st.markdown("""
    **How to use:**
    - Use the sidebar to upload your own dataset or use the default.
    - Navigate between pages for assessment, recommendations, analytics, and more.
    - The dashboard shows a summary of your workforce and AI salary predictions.
    """)

elif page == "👤 Employee Assessment":
    st.title("Employee Assessment")
    st.write("Assess employee performance and compare actual vs. predicted salary.")
    st.dataframe(df[['EmployeeNumber', 'JobRole', 'PerformanceRating', 'Actual_AnnualSalary', 'AI_Predicted_AnnualSalary']], use_container_width=True)
    st.markdown("""
    - **PerformanceRating**: 1 (Low) to 4 (Outstanding)
    - Compare predicted salary to actual salary to identify underpaid or overpaid employees.
    - Use this data for HR reviews or salary adjustments.
    """)
    st.info("Tip: Sort the table by PerformanceRating or salary columns for deeper insights.")

elif page == "📋 Job Recommendation":
    st.title("Job Recommendation")
    st.write("This page recommends jobs to employees based on their skills and predicted performance.")
    # Simple example: Recommend top 3 job roles by average predicted salary
    top_roles = df.groupby('JobRole')['AI_Predicted_AnnualSalary'].mean().sort_values(ascending=False).head(3)
    st.markdown("**Top 3 Recommended Job Roles (by AI-predicted salary):**")
    for i, (role, salary) in enumerate(top_roles.items(), 1):
        st.write(f"{i}. {role} — Avg. Predicted Salary: ${salary:,.0f}")
    st.markdown("""
    - Recommendations are based on the roles with the highest AI-predicted salaries.
    - You can enhance this logic to use skills, preferences, or other criteria.
    """)

elif page == "📊 Analytics":
    st.title("Analytics")
    st.subheader(":bar_chart: Actual vs. Predicted Salary Distribution")
    fig, ax = plt.subplots()
    ax.hist(df['Actual_AnnualSalary'], bins=30, alpha=0.5, label='Actual')
    ax.hist(df['AI_Predicted_AnnualSalary'], bins=30, alpha=0.5, label='Predicted')
    ax.set_xlabel('Annual Salary')
    ax.set_ylabel('Number of Employees')
    ax.legend()
    st.pyplot(fig)

    st.subheader(":chart_with_upwards_trend: Actual vs. Predicted Salary Scatter")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df['Actual_AnnualSalary'], df['AI_Predicted_AnnualSalary'], alpha=0.5)
    ax2.plot([df['Actual_AnnualSalary'].min(), df['Actual_AnnualSalary'].max()],
             [df['Actual_AnnualSalary'].min(), df['Actual_AnnualSalary'].max()],
             'r--', label='Perfect Prediction')
    ax2.set_xlabel('Actual Annual Salary')
    ax2.set_ylabel('Predicted Annual Salary')
    ax2.legend()
    st.pyplot(fig2)
    st.markdown("""
    - The histogram compares the distribution of actual and predicted salaries.
    - The scatter plot shows how close the AI predictions are to the real salaries.
    """)

elif page == "⚙️ Model Training":
    st.title("Model Training")
    st.write("Retrain the AI model or adjust model parameters.")
    st.markdown("""
    - The current model is a Random Forest Regressor trained on employee features.
    - You can extend this page to allow users to select features, change model type, or upload labeled data for retraining.
    - For now, the model is retrained automatically each time the data changes.
    """)
    st.info("Advanced: Add controls for hyperparameters, cross-validation, or model explainability here.")

elif page == "🎯 Skill Rating":
    st.title("Skill Rating")
    st.write("View or edit employee skill ratings.")
    if 'Skills' in df.columns and 'Skill Ratings' in df.columns:
        st.dataframe(df[['EmployeeNumber', 'Skills', 'Skill Ratings']], use_container_width=True)
        st.markdown("""
        - Skill ratings are randomly generated for demo purposes.
        - You can enhance this page to allow manual editing or import real skill assessments.
        """)
    else:
        st.warning("Skill data not available in this dataset.")

st.info("This dashboard uses a Random Forest AI model to predict employee salary based on their features and performance. You can further enhance the model or add more AI features as needed!") 