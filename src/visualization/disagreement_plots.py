"""Phase 6A - Disagreement / decision-interpretability visualizations."""

import os
from math import pi

import matplotlib.pyplot as plt
import seaborn as sns


def plot_boxplots(df, features, output_dir):
    """Boxplot of each feature, grouped by final hybrid technology (disagreement cases)."""
    os.makedirs(output_dir, exist_ok=True)

    for feature in features:
        plt.figure(figsize=(7, 4))
        sns.boxplot(data=df, x="Final_Conversion_Technology", y=feature)
        plt.title(f"{feature} by Hybrid Technology (Disagreement Cases)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{feature}_box.png")
        plt.close()


def plot_violinplots(df, features, output_dir):
    """Violin plot of each feature's distribution within the disagreement conflict space."""
    os.makedirs(output_dir, exist_ok=True)

    for feature in features:
        plt.figure(figsize=(7, 4))
        sns.violinplot(
            data=df, x="Final_Conversion_Technology", y=feature, inner="quartile"
        )
        plt.title(f"{feature} Distribution (Conflict Space)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{feature}_violin.png")
        plt.close()


def plot_scatter_boundary(df, x_feature, y_feature, output_path):
    """Scatter plot of two features, colored by final technology, to expose boundary conflicts."""
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=df, x=x_feature, y=y_feature,
        hue="Final_Conversion_Technology", style="Final_Conversion_Technology"
    )
    plt.title(f"{x_feature} vs {y_feature} (Decision Conflict Zone)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_radar_chart(df, features, output_path):
    """Radar (spider) chart of median feature values per final technology ('fingerprints')."""
    grouped = df.groupby("Final_Conversion_Technology")[features].median()

    labels = features
    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
    angles += angles[:1]

    plt.figure(figsize=(9, 6))
    ax = plt.subplot(111, polar=True)

    for tech, row in grouped.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, label=tech)
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids([a * 180 / pi for a in angles[:-1]], labels)
    plt.title("Hybrid Technology Fingerprints (Median Features)")
    plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.75), frameon=False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
