# %% [markdown]
# # EDA Distribution
#
# Inspect one numeric distribution, percentiles and outliers.

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
value_col = "value"
label_col = None

df = pd.read_csv(data_path)
series = df[value_col].dropna()

# %%
percentiles = series.quantile([0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1])
percentiles.to_frame(name=value_col)

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(series, kde=True, ax=axes[0])
sns.boxplot(x=series, ax=axes[1])
axes[0].set_title(f"Distribution of {value_col}")
axes[1].set_title("Outlier check")
sns.despine()
plt.show()

# %%
iqr = series.quantile(0.75) - series.quantile(0.25)
lower = series.quantile(0.25) - 1.5 * iqr
upper = series.quantile(0.75) + 1.5 * iqr

cols = [value_col] + ([label_col] if label_col else [])
df.loc[df[value_col].lt(lower) | df[value_col].gt(upper), cols].sort_values(value_col)
