import pandas as pd
from datetime import date

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
]]

df_new.rename(columns={
    'Vaccine Doses Administered': 'total_doses',
    'People Vaccinated with at least One Dose': 'one_dose',
    'People Fully Vaccinated': 'vaccinated',
}, inplace=True)

# Load existing data and append today's data
filename = "docs/vaccine/data.csv"
df = pd.read_csv(filename, index_col=['county', 'date'], parse_dates=['date'])

df_merged = pd.concat([df, df_new])
df_merged = df_merged[~df_merged.index.duplicated(keep='last')]
df_merged.sort_index(inplace=True)

df_merged.to_csv(filename, float_format='%d', date_format='%Y-%m-%d')
