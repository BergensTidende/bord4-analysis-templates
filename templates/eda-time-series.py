# %% [markdown]
# # EDA Time Series
#
# Inspect a date/value series, optionally split by category.

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
date_col = "date"
value_col = "value"
category_col = None
rolling_window = 7

df = pd.read_csv(data_path, parse_dates=[date_col])
df = df.sort_values(date_col).dropna(subset=[date_col, value_col]).copy()

# %%
if category_col:
    df["rolling_value"] = df.groupby(category_col)[value_col].transform(
        lambda s: s.rolling(rolling_window, min_periods=1).mean()
    )
else:
    df["rolling_value"] = df[value_col].rolling(rolling_window, min_periods=1).mean()

df.tail(10)

# %%
fig, ax = plt.subplots(figsize=(10, 5))

if category_col:
    sns.lineplot(data=df, x=date_col, y="rolling_value", hue=category_col, ax=ax)
else:
    sns.lineplot(data=df, x=date_col, y=value_col, alpha=0.3, ax=ax)
    sns.lineplot(data=df, x=date_col, y="rolling_value", color="black", ax=ax)

ax.set_title(f"{value_col} over time")
sns.despine()
plt.show()

# %%
sort_cols = [category_col, date_col] if category_col else [date_col]
df.sort_values(sort_cols).groupby(category_col).tail(5) if category_col else df.tail(5)
