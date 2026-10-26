# %% [markdown]
# # EDA Before After
#
# Compare the same entities before and after an event or date.

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
entity_col = "name"
period_col = "period"
value_col = "value"
before_label = "before"
after_label = "after"

df = pd.read_csv(data_path)

# %%
wide = df.pivot_table(
    index=entity_col, columns=period_col, values=value_col, aggfunc="mean"
)
wide = wide.dropna(subset=[before_label, after_label]).copy()
wide["change"] = wide[after_label] - wide[before_label]
wide["pct_change"] = wide["change"] / wide[before_label]
wide.sort_values("change", ascending=False).head(20)

# %%
plot_entities = wide["change"].abs().sort_values(ascending=False).head(20).index
plot_df = df[df[entity_col].isin(plot_entities)].copy()

fig, ax = plt.subplots(figsize=(8, 8))
sns.lineplot(data=plot_df, x=period_col, y=value_col, hue=entity_col, marker="o", ax=ax)
ax.set_title(f"Before/after change in {value_col}")
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
sns.despine()
plt.show()

# %%
fig, ax = plt.subplots(figsize=(7, 5))
sns.histplot(wide["change"], kde=True, ax=ax)
ax.axvline(0, color="black", linewidth=1)
ax.set_title("Distribution of changes")
sns.despine()
plt.show()
