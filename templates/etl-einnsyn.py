# %% [markdown]
# # Get data from Einnsyn
#
# Fetch records from Einnsyn for a date range and public organization. Adjust the request body to match the search you need.
#
# ## Find organization id or request JSON
#
# * Go to einnsyn.no
# * Choose the organization from the list
# * Inspect the network traffic
# * Find the call to `https://einnsyn.no/api/result`
# * Look for the selected organization under `arkivskaperTransitive`
# * If you need multiple organizations, pass them as an array
# * For custom searches, build the search in Einnsyn and paste the request JSON into `data`
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
# Specific imports
from datetime import datetime
from time import sleep

import requests

# %%
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 1, 15)


# %%
def search_einnsyn(from_date, to_date, organization, offset=0):
    data = {
        "size": 50,
        "offset": offset,
        "aggregations": {
            "contentTypes": "type",
            "virksomheter": "arkivskaperTransitive",
        },
        "appliedFilters": [
            {
                "to": f"{to_date:%Y-%m-%d}||/d",
                "from": f"{from_date:%Y-%m-%d}||/d",
                "fieldName": "dokumentetsDato",
                "type": "rangeQueryFilter",
            },
            {
                "fieldName": "type",
                "fieldValue": ["JournalpostForMøte"],
                "type": "notQueryFilter",
            },
            {
                "fieldName": "arkivskaperTransitive",
                "fieldValue": [organization],
                "type": "postQueryFilter",
            },
        ],
        "sort": {"fieldName": "_score", "order": "ASC"},
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
    }

    response = requests.post(
        "https://einnsyn.no/api/result",
        json=data,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# %%
d = search_einnsyn(
    start_date,
    end_date,
    "http://data.einnsyn.no/virksomhet/oepeksport_content_provider_93",
    0,
)

# %%
dfs = []
for offset in range(0, d["hitCount"], 50):
    sleep(0.5)
    d = search_einnsyn(
        start_date,
        end_date,
        "http://data.einnsyn.no/virksomhet/oepeksport_content_provider_93",
        offset,
    )
    df_offset = pd.json_normalize(d["searchHits"])
    dfs.append(df_offset)
    logger.info("Fetched offset %s", offset)

df_all = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# %%
df_all.head(10)

# %%
df_all["sak_doknr"] = df_all["source.saksnummerGenerert"].str[2]
df_all["dokdato_str"] = df_all["source.dokumentetsDato"]
df_all["dokdato"] = pd.to_datetime(df_all.dokdato_str, format="%Y-%m-%d")
df_all["journaldato_einnsyn"] = pd.to_datetime(
    df_all["source.journaldato"], format="%Y-%m-%d"
)
df_all["publisertdato_einnsyn"] = pd.to_datetime(df_all["source.publisertDato"])
df_all["doktittel"] = df_all["source.offentligTittel"]
df_all["saktittel"] = df_all["source.parent.offentligTittel"]
df_all["journaltype"] = df_all["source.type"].str[0]

# %%
df_all.head(10)

# %%
df_all
