import pandas as pd
from typing import List, Optional

def filter_by_skill(df: pd.DataFrame, skill: str) -> pd.DataFrame:
    """
    Filter candidates who have the specified skill.
    """
    return df[df['Skills'].str.contains(skill, case=False, na=False)]

def filter_by_salary(df: pd.DataFrame, min_salary: Optional[float], max_salary: Optional[float]) -> pd.DataFrame:
    """
    Filter candidates within the specified salary range.
    """
    if min_salary is not None:
        df = df[df['Expected Salary'] >= min_salary]
    if max_salary is not None:
        df = df[df['Expected Salary'] <= max_salary]
    return df

def filter_by_role(df: pd.DataFrame, role: str) -> pd.DataFrame:
    """
    Filter candidates by assigned or preferred job role.
    """
    return df[(df['Assigned Role'] == role) | (df['Preferred Job Role'] == role)] 