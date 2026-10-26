# %% [markdown]
# # EDA Compare Groups
#
# Compare one numeric value across groups.

# %%
import logging
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
import pandas as pd
import seaborn as sns

pd.options.display.max_columns = 80
sns.set_theme(style="whitegrid", context="notebook")

# %%
data_path = config.get_processed_file("dataset.csv")
group_col = "group"
value_col = "value"

df = pd.read_csv(data_path)
plot_df = df.dropna(subset=[group_col, value_col]).copy()

# %%
summary = (
    plot_df.groupby(group_col)[value_col]
    .agg(rows="count", mean="mean", median="median", min="min", max="max")
    .sort_values("median", ascending=False)
)
summary

# %%
order = summary.index.tolist()

fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(
    data=plot_df, x=group_col, y=value_col, order=order, showfliers=False, ax=ax
)
sns.stripplot(
    data=plot_df,
    x=group_col,
    y=value_col,
    order=order,
    color="black",
    alpha=0.45,
    ax=ax,
)
ax.set_title(f"{value_col} by {group_col}")
ax.tick_params(axis="x", rotation=30)
sns.despine()
plt.show()
