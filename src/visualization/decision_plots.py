"""
Phase 5 - Decision comparison plots.

It handles 3 questions (1) hybrid framework follows cluster logic or 
rule logic more closely; (2) where do the three frameworks differ; (3) 
Which clusters show stable decisions (a single dominant technology) vs 
clusters with unceertain decisions (a mixed distribution of technologies).

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_technology_counts(df, column, title, output_path):
    """Bar plot of technology counts for a given decision column."""
    counts = df[column].value_counts()

    plt.figure(figsize=(6, 4))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title(title)
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_cluster_technology_heatmap(df, tech_column, output_path):
    """Heatmap of sample counts by Cluster x technology column."""
    heatmap_data = pd.crosstab(df["Cluster"], df[tech_column])

    plt.figure(figsize=(7, 5))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Cluster vs {tech_column}")
    plt.ylabel("Cluster")
    plt.xlabel("Technology")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_agreement_rates(agreement_df, output_path):
    """Bar plot comparing pairwise agreement rates between frameworks."""
    values = agreement_df.loc["Agreement_Rate"]

    plt.figure(figsize=(6, 4))
    sns.barplot(x=values.index, y=values.values)
    plt.ylim(0, 1)
    plt.ylabel("Agreement Rate")
    plt.xlabel("Decisions")
    plt.title("Decision Agreement Comparison")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_decision_flow(df, output_path):
    """Stacked bar chart of technology counts per cluster for each decision framework."""
    flow = (
        df.groupby("Cluster")[
            [
                "Final_Tech_ClusterOnly",
                "Final_Tech_RuleOnly",
                "Final_Conversion_Technology"
            ]
        ]
        .value_counts()
        .unstack(fill_value=0)
    )

    flow.plot(kind="bar", stacked=True, figsize=(8, 8))
    plt.title("Decision Distribution Across Frameworks")
    plt.ylabel("Sample Count")
    plt.xlabel("Cluster")
    plt.legend(title="Technology")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
