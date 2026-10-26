# %% [markdown]
# # Import from and save to Google Sheets
#

# %%
# Interactive Python config, environment and logging

import logging
import os
import sys
from pathlib import Path

import pakkenellik.config as conf
from dotenv import load_dotenv
from pakkenellik.log import logger

# Interactive editors can run with either the project root or the notebooks folder as cwd.
PROJECT_DIR = Path.cwd().resolve()
if PROJECT_DIR.name in {"templates", "notebooks"}:
    PROJECT_DIR = PROJECT_DIR.parent

project_path = str(PROJECT_DIR)
if project_path not in sys.path:
    sys.path.insert(0, project_path)

try:
    ipython = get_ipython()
except NameError:
    ipython = None

if ipython:
    if "autoreload" not in ipython.extension_manager.loaded:
        ipython.run_line_magic("load_ext", "autoreload")
    ipython.run_line_magic("autoreload", "2")

load_dotenv(PROJECT_DIR / ".env")

config = conf.Config(project_path)
logger.setLevel(logging.INFO)

# %%
# Data manipulation
import numpy as np
import pandas as pd

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# %%
# Google Sheets helpers
from pakkenellik.google.sheets import (
    format_worksheet,
    get_worksheet_as_dataframe,
    open_or_create_spreadsheet,
    save_dataframe_to_worksheet,
)

# %% [markdown]
# ## Read from spreadsheet

# %%
credentials_path = None
# Set credentials_path explicitly if this project uses a service-account JSON file.
# With None, pakkenellik uses GOOGLE_APPLICATION_CREDENTIALS or Application Default Credentials.

# %%
# Demo, uses historical football matches from the second tier in Norway
spreadsheet_key = "1ar2A28vr8iRIidzgkH16Z7RExDU2W_faYdr7bRpQIA8"
worksheet_name = "historical_obos_games"

df = get_worksheet_as_dataframe(
    spreadsheet_key,
    worksheet_name=worksheet_name,
    credentials_path=credentials_path,
)

# %%
df.head()

# %% [markdown]
# ## Write to Spreadsheet

# %%
new_worksheet = save_dataframe_to_worksheet(
    df,
    "Obos 1997 – 2021",
    "1Ks2h58ja7DmiovfTDEHPB-RNt1IQrf_Q",
    "games",
    include_index=False,
)

# %%
df.index

# %%
# Basic formatting.
# See https://github.com/robin900/gspread-formatting for tips.

text_cols = ["home_team", "away_team", "opponent_team", "home_away", "result"]
bold_text_cols = ["team"]
date_cols = ["date"]
int_cols = [
    "year",
    "month",
    "day",
    "_round",
    "season_game",
    "points",
    "team_goals",
    "team_conceded",
    "team_goals_half_time",
    "team_conceded_half_time",
]
float_cols = [
    "season_points_avg",
    "season_home_points_avg",
    "season_home_points_avg_before",
    "season_final_avg",
    "season_away_points_avg",
    "season_away_points_avg_before",
]

format_worksheet(
    new_worksheet,
    df,
    text_columns=text_cols,
    bold_text_columns=bold_text_cols,
    date_columns=date_cols,
    int_columns=int_cols,
    float_columns=float_cols,
    frozen_columns=2,
)

# %%
