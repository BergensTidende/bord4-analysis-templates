# %% [markdown]
# # EDA Ranking
#
# Rank observations overall or within groups and inspect the top and bottom rows.

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
from pakkenellik.ssb import add_rank

pd.options.display.max_columns = 80
sns.set_theme(style="whitegrid", context="notebook")

# %%
data_path = config.get_processed_file("dataset.csv")
label_col = "name"
value_col = "value"
group_col = None
ascending = False

df = pd.read_csv(data_path)
ranked = add_rank(
    df,
    value_col=value_col,
    group_col=group_col,
    ascending=ascending,
    output_col="rank",
)

# %%
display_cols = [col for col in ["rank", group_col, label_col, value_col] if col]
ranked.sort_values(display_cols[:1]).loc[:, display_cols].head(20)

# %%
top = ranked.sort_values("rank").head(20).copy()

fig, ax = plt.subplots(figsize=(8, 7))
sns.barplot(data=top, y=label_col, x=value_col, hue=group_col, dodge=False, ax=ax)
ax.set_title(f"Top {len(top)} by {value_col}")
sns.despine()
plt.show()
