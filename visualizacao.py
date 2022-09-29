from sys import displayhook
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

k = pd.read_csv('dados_letras.csv')
print(k)
df_dadinhos = sns.load_dataset('k')
sns.relplot(
    data=df_dadinhos,
    x="total_bill", y="tip", col="time",
    hue="smoker", style="smoker", size="size",
)
plt.show(df_dadinhos)
