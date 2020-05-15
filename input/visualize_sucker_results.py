import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("autoscout_datasucker_stat_2.csv", sep=";", usecols=["model", "make", "run_time", "images", "errors"])

df = df.groupby("make").sum()
df = df.sort_values(by=['images'], ascending=False)
df = df.head(10)

labels = df.index.tolist()
img = df["images"].tolist()

plt.bar(labels, df["images"], label="Num. of images")
plt.plot(df["run_time"], 'y', label="Run time in sec")
plt.plot(df["errors"], 'r', label="Errors")

plt.legend()
plt.xticks(rotation=90)
plt.gcf().subplots_adjust(bottom=0.3)
plt.show()