import pandas as pd
import matplotlib.pyplot as plt

def generate_statistics():
    try:
        df = pd.read_csv("data/Patient_data.csv", delimiter=',')
        fig, ax = plt.subplots()
        df['Race'].value_counts().plot(kind='bar', ax=ax, title="Patient Race Distribution")
        fig.savefig("output/statistics_plot.png")
        return "output/statistics_plot.png"
    except Exception as e:
        return f"Error generating statistics: {e}"