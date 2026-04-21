from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR.parent / "15-04-26" / "data" / "iris.csv"
NUMERIC_COLUMNS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]
SPECIES_ORDER = ["setosa", "versicolor", "virginica"]


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="A small matplotlib and seaborn exploration of the Iris dataset")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA_PATH, help="Path to the iris CSV file")
    parser.add_argument("--output", type=Path, default=BASE_DIR / "figures", help="Folder for saved plots")
    return parser


def load_iris_data(data_path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        data_path,
        header=None,
        names=["sepal_length", "sepal_width", "petal_length", "petal_width", "species"],
    )
    df["species"] = df["species"].str.replace("Iris-", "", regex=False)
    return df


def prepare_output_dir(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_matplotlib_figure(fig: plt.Figure, output_dir: Path, filename: str) -> Path:
    path = output_dir / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_species_counts(df: pd.DataFrame, output_dir: Path) -> Path:
    counts = df["species"].value_counts().reindex(SPECIES_ORDER)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.bar(counts.index, counts.values, color=["#264653", "#2a9d8f", "#e9c46a"])
    ax.bar_label(bars, padding=3)
    ax.set_title("Species count in the Iris dataset")
    ax.set_xlabel("Species")
    ax.set_ylabel("Number of samples")
    ax.set_ylim(0, counts.max() + 12)
    return save_matplotlib_figure(fig, output_dir, "01_species_counts.png")


def plot_feature_means(df: pd.DataFrame, output_dir: Path) -> Path:
    summary = df.groupby("species")[NUMERIC_COLUMNS].mean().reindex(SPECIES_ORDER)
    x_positions = np.arange(len(NUMERIC_COLUMNS))
    width = 0.24

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#264653", "#2a9d8f", "#e76f51"]

    for index, species in enumerate(summary.index):
        ax.bar(
            x_positions + (index - 1) * width,
            summary.loc[species].values,
            width=width,
            label=species,
            color=colors[index],
        )

    ax.set_title("Average measurements by species")
    ax.set_xlabel("Feature")
    ax.set_ylabel("Average value")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([name.replace("_", " ").title() for name in NUMERIC_COLUMNS])
    ax.legend(frameon=False)
    return save_matplotlib_figure(fig, output_dir, "02_feature_means.png")


def plot_feature_distributions(df: pd.DataFrame, output_dir: Path) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    for ax, column in zip(axes.flat, NUMERIC_COLUMNS):
        sns.histplot(data=df, x=column, bins=16, color="#2a9d8f", ax=ax)
        ax.set_title(column.replace("_", " ").title())
        ax.set_xlabel("")
        ax.set_ylabel("Count")

    fig.suptitle("Feature distribution snapshots", fontsize=14)
    return save_matplotlib_figure(fig, output_dir, "03_feature_distributions.png")


def plot_boxplots(df: pd.DataFrame, output_dir: Path) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))

    for ax, column in zip(axes.flat, NUMERIC_COLUMNS):
        sns.boxplot(data=df, x="species", y=column, order=SPECIES_ORDER, ax=ax)
        ax.set_title(column.replace("_", " ").title())
        ax.set_xlabel("")

    fig.suptitle("Boxplots by species", fontsize=14)
    return save_matplotlib_figure(fig, output_dir, "04_boxplots_by_species.png")


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    corr = df[NUMERIC_COLUMNS].corr()
    sns.heatmap(corr, annot=True, cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Correlation between numeric features")
    return save_matplotlib_figure(fig, output_dir, "05_correlation_heatmap.png")


def plot_pairplot(df: pd.DataFrame, output_dir: Path) -> Path:
    grid = sns.pairplot(
        df,
        hue="species",
        corner=True,
        diag_kind="hist",
        palette="Set2",
        plot_kws={"alpha": 0.8, "s": 40},
    )
    grid.fig.suptitle("Pairplot of the Iris measurements", y=1.02)
    path = output_dir / "06_pairplot.png"
    grid.savefig(path, dpi=160, bbox_inches="tight")
    plt.close("all")
    return path


def print_summary(df: pd.DataFrame) -> None:
    print("Iris dataset loaded successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print()

    grouped = df.groupby("species")[NUMERIC_COLUMNS].mean().round(2)
    print("Average values by species:")
    print(grouped.to_string())
    print()

    corr = df[NUMERIC_COLUMNS].corr().round(2)
    print("Correlation matrix:")
    print(corr.to_string())


def main() -> None:
    args = build_parser().parse_args()
    sns.set_theme(style="whitegrid", context="notebook")

    if not args.data.exists():
        raise FileNotFoundError(f"Could not find the dataset at {args.data}")

    output_dir = prepare_output_dir(args.output)
    iris_df = load_iris_data(args.data)

    print_summary(iris_df)

    saved_files = [
        plot_species_counts(iris_df, output_dir),
        plot_feature_means(iris_df, output_dir),
        plot_feature_distributions(iris_df, output_dir),
        plot_boxplots(iris_df, output_dir),
        plot_correlation_heatmap(iris_df, output_dir),
        plot_pairplot(iris_df, output_dir),
    ]

    print()
    print("Saved figures:")
    for path in saved_files:
        print(f"- {path}")


if __name__ == "__main__":
    main()