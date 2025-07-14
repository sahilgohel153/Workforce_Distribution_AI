import pandas as pd
from typing import List, Dict

REQUIRED_COLUMNS = ['Name', 'Skills', 'Skill Ratings', 'Preferred Job Role', 'Expected Salary']

def load_candidates_from_csv(file_path: str) -> pd.DataFrame:
    """
    Load candidate data from a CSV file and validate required columns.
    """
    df = pd.read_csv(file_path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df

def load_candidates_from_form(form_data: List[Dict]) -> pd.DataFrame:
    """
    Load candidate data from a list of dictionaries (form input) and validate required columns.
    """
    df = pd.DataFrame(form_data)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df 