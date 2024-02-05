import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

from scrapping.config import TECHNOLOGIES

subprocess.run(['scrapy', 'crawl', 'vacancies', '-O', 'djinni.csv'])

df = pd.read_csv("djinni.csv")

for tech in TECHNOLOGIES:
    df[tech] = df["stack"].apply(lambda x: 1 if tech in str(x) else 0)

tech_counts = df[TECHNOLOGIES].sum().sort_values(ascending=False).head(20)

plt.figure(figsize=(15, 12))
tech_counts.plot(kind='bar', color="skyblue")
plt.title(f"Top 20 Technologies for Python Developers")
plt.xlabel("Technologies")
plt.ylabel("Number of vacancies")
plt.savefig("visualisation/top-20-technologies.png")


def correlation_diagram() -> None:
    df["minSalary"] = df["salary"].str.extract('(\d+)', expand=False).astype(int)
    numbers = df[["experience_years", "minSalary", "applications"]]
    numbers = numbers.rename(columns={"minSalary": "salary", "experience_years": "experience"})
    plt.figure(figsize=(5, 3))
    ax = sns.heatmap(numbers.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=90)
    plt.title("Correlation Heatmap")
    plt.savefig("additional-visualisation/correlation-heatmap.png")


def generate_wordcloud() -> None:
    technologies = " ".join(tech_counts.index)

    wordcloud = WordCloud(
        width=1000, height=500, random_state=20, max_font_size=110
    ).generate(technologies)

    plt.figure(figsize=(5, 3))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("additional-visualisation/wordcloud.png")


if __name__ == "__main__":
    correlation_diagram()
    generate_wordcloud()
