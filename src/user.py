import pandas as pd

class User:
    def __init__(self, username, password):
        self.username = username.strip()
        self.password = password.strip()
        self.role = None

    def authenticate(self):
        try:
            df = pd.read_csv("data/Credentials.csv", delimiter=",")
            df["username"] = df["username"].astype(str).str.strip()
            df["password"] = df["password"].astype(str).str.strip()

            match = df[(df["username"] == self.username) & (df["password"] == self.password)]
            if not match.empty:
                self.role = match.iloc[0]["role"]
                return True
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
