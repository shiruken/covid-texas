import numpy as np
import pandas as pd


def read_date(date):
    """Convert date to datetime with handling for Excel date numbers"""
    try:
        date = int(date)

        # Manually handle weird date value in spreadsheet for August 8
        if date == 39668:
            return pd.to_datetime('2020-08-08')
        else:
            return pd.to_datetime('1899-12-30') + pd.to_timedelta(date, 'D')
    except:
        return pd.to_datetime(date[0:10])


def fix_date_index(df):
    """Convert date index strings to datetime objects"""
    date_index = df.index.levels[2].to_series()
    date_index_fixed = date_index.apply(read_date)
    df.index.set_levels(date_index_fixed, level=2, inplace=True)


# Load hospital capacity data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasHospitalCapacityoverTimebyTSA.xlsx'
df = pd.read_excel(url, sheet_name=None, header=2, index_col=[0, 1], nrows=23)

# Parse total available beds
df['Total Available Beds'].replace('--', np.nan, inplace=True)
df['Total Available Beds'] = df['Total Available Beds'].apply(pd.to_numeric)
df['Total Available Beds'].loc['Total', 'Statewide Total'] = df['Total Available Beds'][:-1].sum()
df_total_beds_available = pd.DataFrame(df['Total Available Beds'].stack())
df_total_beds_available.rename(columns = {0: 'total_beds_available'}, inplace=True)
fix_date_index(df_total_beds_available)

# Parse total occupied beds
df['Total Occupied Beds'].replace('--', np.nan, inplace=True)
df['Total Occupied Beds'] = df['Total Occupied Beds'].apply(pd.to_numeric)
df['Total Occupied Beds'].loc['Total', 'Statewide Total'] = df['Total Occupied Beds'][:-1].sum()
df_total_beds_occupied = pd.DataFrame(df['Total Occupied Beds'].stack())
df_total_beds_occupied.rename(columns = {0: 'total_beds_occupied'}, inplace=True)
fix_date_index(df_total_beds_occupied)

# Parse available ICU beds
df['ICU Beds Available'].replace('--', np.nan, inplace=True)
df['ICU Beds Available'] = df['ICU Beds Available'].apply(pd.to_numeric)
df['ICU Beds Available'].loc['Total', 'Statewide Total'] = df['ICU Beds Available'][:-1].sum()
df_icu_beds_available = pd.DataFrame(df['ICU Beds Available'].stack())
df_icu_beds_available.rename(columns = {0: 'icu_beds_available'}, inplace=True)
fix_date_index(df_icu_beds_available)

#Parse occupied ICU beds
df['ICU Beds Occupied'].replace('--', np.nan, inplace=True)
df['ICU Beds Occupied'] = df['ICU Beds Occupied'].apply(pd.to_numeric)
df['ICU Beds Occupied'].loc['Total', 'Statewide Total'] = df['ICU Beds Occupied'][:-1].sum()
df_icu_beds_occupied = pd.DataFrame(df['ICU Beds Occupied'].stack())
df_icu_beds_occupied.rename(columns = {0: 'icu_beds_occupied'}, inplace=True)
fix_date_index(df_icu_beds_occupied)

# Load COVID-19 hospital data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasCOVID-19HospitalizationsOverTimebyTSA.xlsx'
df = pd.read_excel(url, sheet_name=None, header=2, index_col=[0, 1], nrows=23)

# Parse total COVID-19 inpatients
df['COVID-19 Hospitalizations'].loc['Total', 'Statewide Total'] = df['COVID-19 Hospitalizations'][:-1].sum()
df_covid_inpatients = pd.DataFrame(df['COVID-19 Hospitalizations'].stack())
df_covid_inpatients.rename(columns = {0: 'covid_inpatients'}, inplace=True)
fix_date_index(df_covid_inpatients)

# Parse ICU COVID-19 inpatients
df['COVID-19 ICU'].loc['Total', 'Statewide Total'] = df['COVID-19 ICU'][:-1].sum()
df_covid_icu_inpatients = pd.DataFrame(df['COVID-19 ICU'].stack())
df_covid_icu_inpatients.rename(columns = {0: 'covid_icu_inpatients'}, inplace=True)
fix_date_index(df_covid_icu_inpatients)

# Merge the datasets
df = [df_total_beds_available, df_total_beds_occupied, df_icu_beds_available, 
      df_icu_beds_occupied, df_covid_inpatients, df_covid_icu_inpatients]
df_merged = pd.concat(df, join='outer', axis=1).reindex(df_total_beds_available.index)

# Reset the index
df_merged.index.names = ['tsa', 'location', 'date']
df_merged.reset_index(inplace=True)
df_merged['tsa'] = df_merged['tsa'].apply(lambda x: x.replace('.', ''))

# Write unmodified data to CSV file
df_merged.to_csv('data.csv', index=False, float_format='%d', date_format='%Y-%m-%d')

# Manual removals of extreme values
df_merged.loc[(df_merged['tsa'] == 'N') & (df_merged['date'] == '2020-04-28'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'I') & (df_merged['date'] == '2020-05-31'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-06-07'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'B') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-07-23'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'E') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'I') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'L') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-23'), ['covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'P') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Q') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'S') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'T') & (df_merged['date'] == '2020-07-23'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-23'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-24'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'B') & (df_merged['date'] == '2020-07-24'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-07-24'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-07-24'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-24'), 'total_beds_available'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-24'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-24'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-24'), 'covid_inpatients'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'T') & (df_merged['date'] == '2020-07-24'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-24'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-25'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-07-25'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-07-25'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-25'), 'total_beds_available'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-25'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-25'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-25'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-25'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-26'), ['icu_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'B') & (df_merged['date'] == '2020-07-26'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'E') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'F') & (df_merged['date'] == '2020-07-26'), 'covid_icu_inpatients'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'I') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'L') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'N') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Q') & (df_merged['date'] == '2020-07-26'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'T') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'U') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-07-27'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-27'), 'total_beds_available'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-27'), 'covid_inpatients'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-27'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-27'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-27'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-07-28'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-07-28'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-28'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-28'), ['total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-29'), ['total_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-29'), ['total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-31'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Q') & (df_merged['date'] == '2020-07-31'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'U') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'F') & (df_merged['date'] == '2020-08-02'), 'icu_beds_occupied'] = np.nan

# Write cleaned data to CSV file
df_merged.to_csv('docs/data.csv', index=False, float_format='%d', date_format='%Y-%m-%d')
