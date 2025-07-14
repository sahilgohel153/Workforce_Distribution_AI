# Example market salaries (can be expanded or loaded from a config/database)
MARKET_SALARIES = {
    'Data Scientist': 120000,
    'Software Engineer': 110000,
    'Product Manager': 130000,
    'HR Specialist': 80000,
    'Business Analyst': 90000,
}

def get_market_salary(job_role: str) -> float:
    """
    Return the average market salary for a given job role.
    If the role is not found, return None.
    """
    return MARKET_SALARIES.get(job_role) 