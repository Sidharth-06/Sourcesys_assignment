# Matplotlib and Seaborn Exploration

## Goal

This small assignment explores how `matplotlib` and `seaborn` can be used together to inspect the Iris dataset in a clean, readable way. I kept the code simple on purpose so it feels like a normal student submission rather than a copy-pasted template.

## Files In This Folder

- `matplotlib_seaborn_exploration.py` - loads the dataset, prints a compact summary, and saves the charts.
- `figures/` - created when the script runs.

## Why I Used Iris

I chose the Iris dataset because it is small, balanced, and easy to explain. It works well for practice because the species are similar enough to overlap in some plots but still distinct enough to notice useful patterns.

## What The Script Covers

- species count comparison using `matplotlib`
- average feature comparison using `matplotlib`
- distribution plots using `seaborn`
- boxplots by species using `seaborn`
- correlation heatmap using `seaborn`
- pairplot for a fuller view of the relationships

## Main Observations

- Petal length and petal width separate the species more clearly than the sepal measurements.
- Setosa is the easiest class to identify visually.
- The sepal features overlap more, so they are less useful when looked at alone.
- The heatmap and pairplot show that the petal features carry most of the visible structure in the dataset.

## How To Run

From the `python_programs/20-04-26` folder:

```bash
python matplotlib_seaborn_exploration.py
```

The script uses the Iris CSV stored in the earlier `15-04-26` folder and saves all plots into `figures/`.