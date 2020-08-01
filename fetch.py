import numpy as np
import pandas as pd

# Load hospital capacity data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasHospitalCapacityoverTimebyTSA.xlsx'
df = pd.read_excel(url, sheet_name=None, header=2, index_col=[0, 1], nrows=23)

# Parse total available beds
df['Total Available Beds'].replace('--', np.nan, inplace=True)
df['Total Available Beds'] = df['Total Available Beds'].apply(pd.to_numeric)
df['Total Available Beds'].loc['Total', 'Statewide Total'] = df['Total Available Beds'][:-1].sum()
df_total_beds_available = pd.DataFrame(df['Total Available Beds'].stack())
df_total_beds_available.rename(columns = {0: 'total_beds_available'}, inplace=True)

# Parse total occupied beds
df['Total Occupied Beds'].replace('--', np.nan, inplace=True)
df['Total Occupied Beds'] = df['Total Occupied Beds'].apply(pd.to_numeric)
df['Total Occupied Beds'].loc['Total', 'Statewide Total'] = df['Total Occupied Beds'][:-1].sum()
df_total_beds_occupied = pd.DataFrame(df['Total Occupied Beds'].stack())
df_total_beds_occupied.rename(columns = {0: 'total_beds_occupied'}, inplace=True)

# Parse available ICU beds
df['ICU Beds Available'].replace('--', np.nan, inplace=True)
df['ICU Beds Available'] = df['ICU Beds Available'].apply(pd.to_numeric)
df['ICU Beds Available'].loc['Total', 'Statewide Total'] = df['ICU Beds Available'][:-1].sum()
df_icu_beds_available = pd.DataFrame(df['ICU Beds Available'].stack())
df_icu_beds_available.rename(columns = {0: 'icu_beds_available'}, inplace=True)

#Parse occupied ICU beds
df['ICU Beds Occupied'].replace('--', np.nan, inplace=True)
df['ICU Beds Occupied'] = df['ICU Beds Occupied'].apply(pd.to_numeric)
df['ICU Beds Occupied'].loc['Total', 'Statewide Total'] = df['ICU Beds Occupied'][:-1].sum()
df_icu_beds_occupied = pd.DataFrame(df['ICU Beds Occupied'].stack())
df_icu_beds_occupied.rename(columns = {0: 'icu_beds_occupied'}, inplace=True)

# Load COVID-19 hospital data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasCOVID-19HospitalizationsOverTimebyTSA.xlsx'
df = pd.read_excel(url, sheet_name=None, header=2, index_col=[0, 1], nrows=23)

# Parse total COVID-19 inpatients
df['COVID-19 Hospitalizations'].loc['Total', 'Statewide Total'] = df['COVID-19 Hospitalizations'][:-1].sum()
df_covid_inpatients = pd.DataFrame(df['COVID-19 Hospitalizations'].stack())
df_covid_inpatients.rename(columns = {0: 'covid_inpatients'}, inplace=True)

# Parse ICU COVID-19 inpatients
df['COVID-19 ICU'].loc['Total', 'Statewide Total'] = df['COVID-19 ICU'][:-1].sum()
df_covid_icu_inpatients = pd.DataFrame(df['COVID-19 ICU'].stack())
df_covid_icu_inpatients.rename(columns = {0: 'covid_icu_inpatients'}, inplace=True)

# Merge the datasets
df = [df_total_beds_available, df_total_beds_occupied, df_icu_beds_available, 
      df_icu_beds_occupied, df_covid_inpatients, df_covid_icu_inpatients]
df_merged = pd.concat(df, join='outer', axis=1).reindex(df_total_beds_available.index)

# Reset the index
df_merged.index.names = ['tsa', 'location', 'date']
df_merged.reset_index(inplace=True)
df_merged['tsa'] = df_merged['tsa'].apply(lambda x: x.replace('.', ''))

# Manual corrections
df_merged.loc[(df_merged['tsa'] == 'I') & (df_merged['date'] == '2020-05-31'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'N') & (df_merged['date'] == '2020-04-28'), 'total_beds_occupied'] = np.nan

# Write to CSV file
df_merged.to_csv('docs/data.csv', index=False, float_format='%d')
