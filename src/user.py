import pandas as pd

def authenticate_user(username, password):
    try:
        df = pd.read_csv("data/Credentials.csv", delimiter='\t')

        match = df[(df['username'] == username) & (df['password'] == password)]
        if not match.empty:
            return match.iloc[0]['role']
        return None
    except Exception as e:
        print("Error reading Credentials.csv:", e)
        return None