import pandas as pd
from market_salary import get_market_salary

# Example mapping of skills to job roles (should be expanded for real use)
ROLE_SKILL_MAP = {
    'Data Scientist': ['Python', 'Machine Learning', 'Statistics', 'Data Analysis'],
    'Software Engineer': ['Python', 'Java', 'C++', 'Algorithms'],
    'Product Manager': ['Leadership', 'Communication', 'Strategy'],
    'HR Specialist': ['Recruitment', 'Onboarding', 'Employee Relations'],
    'Business Analyst': ['Excel', 'Data Analysis', 'Reporting'],
}

def assign_suitable_role(skills: list) -> str:
    """
    Assign the most suitable job role based on the candidate's top skills.
    """
    role_scores = {}
    for role, req_skills in ROLE_SKILL_MAP.items():
        score = len(set(skills) & set(req_skills))
        role_scores[role] = score
    # Return the role with the highest score
    return max(role_scores, key=role_scores.get)

def analyze_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze candidates: assign suitable role, compare salary, compute suitability score.
    Returns a DataFrame with added columns: 'Assigned Role', 'Market Salary', 'Salary Comparison', 'Suitability Score'.
    """
    results = []
    for _, row in df.iterrows():
        skills = [s.strip() for s in row['Skills'].split(',')]
        skill_ratings = [int(r.strip()) for r in row['Skill Ratings'].split(',')]
        assigned_role = assign_suitable_role(skills)
        market_salary = get_market_salary(assigned_role)
        expected_salary = float(row['Expected Salary'])
        salary_comparison = expected_salary - market_salary if market_salary else None
        # Suitability score: based on skill match and salary expectation
        skill_score = sum(skill_ratings) / (len(skill_ratings) * 10) * 70  # up to 70 points
        salary_score = 30 if market_salary and expected_salary <= market_salary else max(0, 30 - (expected_salary - market_salary) / market_salary * 30) if market_salary else 0
        suitability_score = round(skill_score + salary_score, 2)
        results.append({
            **row,
            'Assigned Role': assigned_role,
            'Market Salary': market_salary,
            'Salary Comparison': salary_comparison,
            'Suitability Score': suitability_score
        })
    return pd.DataFrame(results)

def get_top_candidates_by_role(df: pd.DataFrame, top_n: int = 3) -> dict:
    """
    Return a dictionary of top N candidates per assigned job role, sorted by suitability score.
    """
    grouped = df.groupby('Assigned Role')
    top_candidates = {}
    for role, group in grouped:
        top = group.sort_values('Suitability Score', ascending=False).head(top_n)
        top_candidates[role] = top.to_dict(orient='records')
    return top_candidates 