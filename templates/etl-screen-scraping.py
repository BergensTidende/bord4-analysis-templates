# %% [markdown]
# # Screen scraping
#
# Sometimes we need to fetch the data ourselves.
#
# This example fetches a table from Bergen municipality's 2023 budget. It uses Selenium to render the page and BeautifulSoup for parsing.
#
# Example inspired by https://medium.com/free-code-camp/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251
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
# Data manipulation and scraping
import pandas as pd
from bs4 import BeautifulSoup
from pakkenellik.dataframe.clean_column_headers import clean_column_headers
from selenium import webdriver
from selenium.webdriver.common.by import By

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# %% [markdown]
# ## Fetch url

# %%
url = "https://pub.framsikt.net/2023/bergen/bm-2023-kortversjon_23-26_/#/"

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

# %%
# After opening the url above, Selenium clicks the specific budget link for schools
school_link = driver.find_element(By.XPATH, "//a[div/h3[text()='01B-Skole']]")
school_link.click()

# %% [markdown]
# ## Beautiful Soup

# %%
# Selenium hands the page source to Beautiful Soup
beta_soup = BeautifulSoup(driver.page_source, "lxml")

# %%
h3_tag = beta_soup.find(attrs={"tooltiptext": "Investeringsbudsjett"})
if h3_tag is None:
    raise ValueError("Could not find the investment budget section")

tables = h3_tag.find_all("table")

# %%
df = pd.read_html(str(tables), header=0)

# %%
# The first dataframe contains headers over two rows, so merge them.
line1 = df[0].iloc[0].reset_index()
line1.columns = ["first", "second"]
line1 = line1.replace("Unnamed: 0", "")
line1 = line1.replace(r"\.\d", "", regex=True)
line1["column_header"] = line1["first"].astype(str) + " " + line1["second"].astype(str)

df[1].columns = line1["column_header"].to_list()
df[1] = clean_column_headers(df[1])

# %%
school_df = df[1]

# %%
driver.quit()

# %%
