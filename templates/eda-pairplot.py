# %% [markdown]
# # EDA Pairplot
#
# Quick pairplot and correlation matrix for numeric columns, optionally split by a group column.

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
sns.set_theme(style="ticks", context="notebook")

# %%
data_path = config.get_processed_file("dataset.csv")
group_col = None
numeric_cols = []

df = pd.read_csv(data_path)
if not numeric_cols:
    numeric_cols = df.select_dtypes(include="number").columns[:6].tolist()

df[numeric_cols + ([group_col] if group_col else [])].head()

# %%
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
ax.set_title("Correlation matrix")
plt.show()

# %%
plot_cols = numeric_cols + ([group_col] if group_col else [])
plot_df = df[plot_cols].dropna()

if group_col:
    sns.pairplot(plot_df, hue=group_col, diag_kind="hist", corner=True)
else:
    sns.pairplot(plot_df, diag_kind="hist", corner=True)
