import pandas as pd
from datetime import date
import requests
from bs4 import BeautifulSoup
import json
import re

# Load new data from Texas DSHS
url = "https://www.dshs.state.tx.us/immunize/covid19/COVID-19-Vaccine-Data-by-County.xls"
df = pd.read_excel(url, sheet_name="By County", index_col=[0], engine='openpyxl')
df.drop('Federal Long-Term Care Vaccination Program', inplace=True) # Drop the federal data
df.drop('Federal Pharmacy Retail Vaccination Program', inplace=True)
df.drop('Other', inplace=True) # Drop the unknown county data
df.rename(index={"Texas": "Statewide"}, inplace=True)
df.index.names = ['county']

# Add current date as second level of MultiIndex
df['date'] = pd.to_datetime(date.today())
df.set_index('date', append=True, inplace=True)

# Extract desired columns into new dataframe and rename
df_new = df.loc[:, [
    'Vaccine Doses Administered', 
    'People Vaccinated with at least One Dose', 
    'People Fully Vaccinated',
    'Total Doses Allocated'
]]

df_new.rename(columns={
    'Vaccine Doses Administered': 'total_doses',
    'People Vaccinated with at least One Dose': 'one_dose',
    'People Fully Vaccinated': 'vaccinated',
    'Total Doses Allocated': 'allocated'
}, inplace=True)

# Scrapes shipped doses metric from Tableau dashboard
url = "https://tabexternal.dshs.texas.gov/t/THD/views/COVID-19VaccineinTexasDashboard/Summary"
r = requests.get(url, params={":embed": "y"})
soup = BeautifulSoup(r.text, "html.parser")
tableauData = json.loads(soup.find("textarea", {"id": "tsConfigContainer"}).text)
dataUrl = f'https://tabexternal.dshs.texas.gov{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'
r = requests.post(dataUrl, data={"sheet_id": tableauData["sheetId"]})
shipped = re.findall("Doses Shipped  (\d{1,}(?:\,?\d{3})*)", r.text)
df_new.loc["Statewide", "distributed"] = int(shipped[0].replace(",", ""))

# Load existing data and append today's data
filename = "docs/vaccine/data.csv"
df = pd.read_csv(filename, index_col=['county', 'date'], parse_dates=['date'])

df_merged = pd.concat([df, df_new])
df_merged = df_merged[~df_merged.index.duplicated(keep='last')]
df_merged.sort_index(inplace=True)

df_merged.to_csv(filename, float_format='%d', date_format='%Y-%m-%d')
