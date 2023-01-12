import pandas as pd
from datetime import date

# Load new data from Texas DSHS
url = "https://www.dshs.texas.gov/sites/default/files/LIDS-Immunize-COVID19/COVID%20Dashboard/County%20Dashboard/COVID-19%20Vaccine%20Data%20by%20County.xlsx"
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
    'People Vaccinated with at least One Booster Dose'
]]

df_new.rename(columns={
    'Vaccine Doses Administered': 'total_doses',
    'People Vaccinated with at least One Dose': 'one_dose',
    'People Fully Vaccinated': 'vaccinated',
    'People Vaccinated with at least One Booster Dose': 'boosted'
}, inplace=True)

# Load existing data and append today's data
filename = "docs/vaccine/data.csv"
df = pd.read_csv(filename, index_col=['county', 'date'], parse_dates=['date'])

df_merged = pd.concat([df, df_new])
df_merged = df_merged[~df_merged.index.duplicated(keep='last')]
df_merged.sort_index(inplace=True)

cols = df_merged.columns
df_merged[cols] = df_merged[cols].apply(pd.to_numeric)

df_merged.to_csv(filename, float_format='%d', date_format='%Y-%m-%d')
