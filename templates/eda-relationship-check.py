# %% [markdown]
# # EDA Relationship Check
#
# Check whether two datasets join cleanly and whether selected numeric columns move together.

# %%
import logging
import os
import sys
from pathlib import Path

import pakkenellik.config as conf
from dotenv import load_dotenv
from pakkenellik.log import logger

PROJECT_DIR = Path.cwd().resolve()
if PROJECT_DIR.name in {"templates", "notebooks"}:
    PROJECT_DIR = PROJECT_DIR.parent

project_path = str(PROJECT_DIR)
if project_path not in sys.path:
    sys.path.insert(0, project_path)

load_dotenv(PROJECT_DIR / ".env")
config = conf.Config(project_path)
logger.setLevel(logging.INFO)

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.options.display.max_columns = 80
pd.options.display.max_rows = 40
sns.set_theme(style="whitegrid", context="notebook")

# %% [markdown]
# ## Inputs

# %%
left_path = config.get_processed_file("left.csv")
right_path = config.get_processed_file("right.csv")

join_key = "id"
x_col = "x_value"
y_col = "y_value"
group_col = None

left = pd.read_csv(left_path)
right = pd.read_csv(right_path)

# %% [markdown]
# ## Join Coverage

# %%
merged = left.merge(
    right,
    on=join_key,
    how="outer",
    indicator=True,
    suffixes=("_left", "_right"),
)

join_coverage = (
    merged["_merge"]
    .value_counts(dropna=False)
    .rename_axis("status")
    .reset_index(name="rows")
)
join_coverage["share"] = join_coverage["rows"] / len(merged)
join_coverage

# %%
joined = merged[merged["_merge"] == "both"].copy()
joined[[join_key, x_col, y_col]].head()

# %% [markdown]
# ## Relationship

# %%
plot_df = joined.dropna(subset=[x_col, y_col]).copy()

fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(data=plot_df, x=x_col, y=y_col, scatter_kws={"alpha": 0.65}, ax=ax)
ax.set_title(f"{x_col} vs {y_col}")
sns.despine()
plt.show()

plot_df[[x_col, y_col]].corr(method="pearson")

# %%
numeric_cols = joined.select_dtypes(include="number").columns.tolist()
selected_cols = [col for col in [x_col, y_col] if col in numeric_cols]

if group_col and group_col in joined.columns:
    sns.pairplot(joined[selected_cols + [group_col]].dropna(), hue=group_col)
else:
    sns.pairplot(joined[selected_cols].dropna())

# %% [markdown]
# ## Outliers

# %%
outlier_df = plot_df[[join_key, x_col, y_col]].copy()
outlier_df["x_z"] = (outlier_df[x_col] - outlier_df[x_col].mean()) / outlier_df[
    x_col
].std()
outlier_df["y_z"] = (outlier_df[y_col] - outlier_df[y_col].mean()) / outlier_df[
    y_col
].std()
outlier_df["max_abs_z"] = outlier_df[["x_z", "y_z"]].abs().max(axis=1)
outlier_df.sort_values("max_abs_z", ascending=False).head(20)
