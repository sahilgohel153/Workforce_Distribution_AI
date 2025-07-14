import pandas as pd
from data_loader import load_candidates_from_csv, load_candidates_from_form
from job_analysis import analyze_candidates, get_top_candidates_by_role
from filters import filter_by_skill, filter_by_salary, filter_by_role
import numpy as np

# Example: Load and process data from CSV
# df = load_candidates_from_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
# analyzed_df = analyze_candidates(df)
# top_candidates = get_top_candidates_by_role(analyzed_df)

# Functions for Streamlit integration

def transform_ibm_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the IBM HR dataset to the required format for the app.
    """
    # Use EmployeeNumber as Name
    names = df['EmployeeNumber'].astype(str)
    # Use JobRole, OverTime, EducationField as skills
    skills = df[['JobRole', 'OverTime', 'EducationField']].astype(str).agg(','.join, axis=1)
    # Assign random skill ratings (7-10) for each skill
    skill_counts = skills.str.count(',') + 1
    skill_ratings = skill_counts.apply(lambda n: ','.join([str(np.random.randint(7, 11)) for _ in range(n)]))
    # Use JobRole as Preferred Job Role
    preferred_job_role = df['JobRole']
    # Use MonthlyIncome * 12 as Expected Salary
    expected_salary = (df['MonthlyIncome'] * 12).astype(int)
    transformed = pd.DataFrame({
        'Name': names,
        'Skills': skills,
        'Skill Ratings': skill_ratings,
        'Preferred Job Role': preferred_job_role,
        'Expected Salary': expected_salary
    })
    return transformed

def process_csv(file_path: str) -> pd.DataFrame:
    """
    Load and analyze candidates from a CSV file. Auto-transform IBM dataset if needed.
    """
    try:
        df = load_candidates_from_csv(file_path)
    except ValueError as e:
        # If missing columns, try to transform IBM dataset
        raw_df = pd.read_csv(file_path)
        if set(['EmployeeNumber', 'JobRole', 'OverTime', 'EducationField', 'MonthlyIncome']).issubset(raw_df.columns):
            df = transform_ibm_dataset(raw_df)
        else:
            raise e
    return analyze_candidates(df)

def process_form(form_data: list) -> pd.DataFrame:
    """
    Load and analyze candidates from form input (list of dicts).
    """
    df = load_candidates_from_form(form_data)
    return analyze_candidates(df)

def get_top_candidates(df: pd.DataFrame, top_n: int = 3) -> dict:
    """
    Get top N candidates per job role.
    """
    return get_top_candidates_by_role(df, top_n=top_n)

def apply_filters(df: pd.DataFrame, skill: str = None, min_salary: float = None, max_salary: float = None, role: str = None) -> pd.DataFrame:
    """
    Apply filters to the candidate DataFrame.
    """
    if skill:
        df = filter_by_skill(df, skill)
    if min_salary is not None or max_salary is not None:
        df = filter_by_salary(df, min_salary, max_salary)
    if role:
        df = filter_by_role(df, role)
    return df

def load_default_dataset() -> pd.DataFrame:
    """
    Load and analyze the default dataset from 'WA_Fn-UseC_-HR-Employee-Attrition.csv'.
    Auto-transform if it's the IBM dataset.
    """
    return process_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# The above functions can be called from Streamlit to provide data for:
# - Candidates grouped by role
# - Skill distribution charts
# - Salary vs skill score plots
# - Filtering options 