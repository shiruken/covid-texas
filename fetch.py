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
    date_index_fixed = date_index.apply(read_date) + pd.DateOffset(1)
    df.index.set_levels(date_index_fixed, level=2, inplace=True)


def generate_date_range(index):
    """Generate DatetimeIndex using first and last dates from index column"""
    start = index[0].split()[-1]
    end = index[-1].split()[-1]

    if len(start) == 5:
        start = start + "-20"

    if len(end) == 5:
        end = end + "-21"

    return pd.date_range(start=start, end=end)


tsa_county_map = {
    'A.': ['Armstrong', 'Briscoe', 'Carson', 'Childress', 'Collingsworth', 'Dallam', 'Deaf Smith', 
          'Donley', 'Gray', 'Hall', 'Hansford', 'Hartley', 'Hemphill', 'Hutchinson', 'Lipscomb', 
          'Moore', 'Ochiltree', 'Oldham', 'Parmer', 'Potter', 'Randall', 'Roberts', 'Sherman', 
          'Swisher', 'Wheeler'],
    'B.': ['Bailey', 'Borden', 'Castro', 'Cochran', 'Cottle', 'Crosby', 'Dawson', 'Dickens', 'Floyd', 
          'Gaines', 'Garza', 'Hale', 'Hockley', 'Kent', 'King', 'Lamb', 'Lubbock', 'Lynn', 'Motley', 
          'Scurry', 'Terry', 'Yoakum'],
    'C.': ['Archer', 'Baylor', 'Clay', 'Foard', 'Hardeman', 'Jack', 'Montague', 'Wichita', 'Wilbarger', 'Young'],
    'D.': ['Brown', 'Callahan', 'Coleman', 'Comanche', 'Eastland', 'Fisher', 'Haskell', 'Jones', 
          'Knox', 'Mitchell', 'Nolan', 'Shackelford', 'Stephens', 'Stonewall', 'Taylor', 'Throckmorton'],
    'E.': ['Collin', 'Cooke', 'Dallas', 'Denton', 'Ellis', 'Erath', 'Fannin', 'Grayson', 'Hood', 
          'Hunt', 'Johnson', 'Kaufman', 'Navarro', 'Palo Pinto', 'Parker', 'Rockwall', 
          'Somervell', 'Tarrant', 'Wise'],
    'F.': ['Bowie', 'Cass', 'Delta', 'Hopkins', 'Lamar', 'Morris', 'Red River', 'Titus'],
    'G.': ['Anderson', 'Camp', 'Cherokee', 'Franklin', 'Freestone', 'Gregg', 'Harrison', 'Henderson', 
          'Houston', 'Marion', 'Panola', 'Rains', 'Rusk', 'Shelby', 'Smith', 'Trinity', 'Upshur', 
          'Van Zandt', 'Wood'],
    'H.': ['Angelina', 'Nacogdoches', 'Polk', 'Sabine', 'San Augustine', 'San Jacinto', 'Tyler'],
    'I.': ['Culberson', 'El Paso', 'Hudspeth'],
    'J.': ['Andrews', 'Brewster', 'Crane', 'Ector', 'Glasscock', 'Howard', 'Jeff Davis', 'Loving', 
          'Martin', 'Midland', 'Pecos', 'Presidio', 'Reeves', 'Terrell', 'Upton', 'Ward', 'Winkler'],
    'K.': ['Coke', 'Concho', 'Crockett', 'Irion', 'Kimble', 'Mason', 'Mcculloch', 'Menard', 'Reagan', 
          'Runnels', 'Schleicher', 'Sterling', 'Sutton', 'Tom Green'],
    'L.': ['Bell', 'Coryell', 'Hamilton', 'Lampasas', 'Milam', 'Mills'],
    'M.': ['Bosque', 'Falls', 'Hill', 'Limestone', 'Mclennan'],
    'N.': ['Brazos', 'Burleson', 'Grimes', 'Leon', 'Madison', 'Robertson', 'Washington'],
    'O.': ['Bastrop', 'Blanco' ,'Burnet' ,'Caldwell', 'Fayette', 'Hays', 'Lee', 'Llano', 'San Saba', 
          'Travis', 'Williamson'],
    'P.': ['Atascosa', 'Bandera', 'Bexar', 'Comal', 'Dimmit', 'Edwards', 'Frio', 'Gillespie', 
          'Gonzales', 'Guadalupe', 'Karnes', 'Kendall', 'Kerr', 'Kinney', 'La Salle', 'Maverick', 
          'Medina', 'Real', 'Uvalde', 'Val Verde', 'Wilson', 'Zavala'],
    'Q.': ['Austin', 'Colorado', 'Fort Bend', 'Harris', 'Matagorda', 'Montgomery', 'Walker', 'Waller', 'Wharton'],
    'R.': ['Brazoria', 'Chambers', 'Galveston', 'Hardin', 'Jasper', 'Jefferson', 'Liberty', 'Newton', 'Orange'],
    'S.': ['Calhoun', 'Dewitt', 'De Witt', 'Goliad', 'Jackson', 'Lavaca', 'Victoria'],
    'T.': ['Jim Hogg', 'Webb', 'Zapata'],
    'U.': ['Aransas', 'Bee', 'Brooks', 'Duval', 'Jim Wells', 'Kenedy', 'Kleberg', 'Live Oak', 
          'Mcmullen', 'Nueces', 'Refugio', 'San Patricio'],
    'V.': ['Cameron', 'Hidalgo', 'Starr', 'Willacy'],
    'Total': ['Total']
}


def map_county_to_tsa(county):
    """Map county name to TSA"""
    for k,v in tsa_county_map.items():
        if county.title() in v:
            return(k)


# Load combined hospital data
url = 'https://www.dshs.state.tx.us/coronavirus/CombinedHospitalDataoverTimebyTSA.xlsx'
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

# Load and parse total case count data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx'
df = pd.read_excel(url, sheet_name='Cases by County', index_col=[0], header=2, nrows=255)
new_date_range = generate_date_range(df.columns)
new_date_range = new_date_range.drop([pd.Timestamp('2020-03-07'), pd.Timestamp('2020-03-08'), pd.Timestamp('2020-03-14')])
df.columns = new_date_range
df = df.loc[:, df.columns > '2020-04-11']
df.insert(0, 'TSA ID', [map_county_to_tsa(county) for county in df.index])
df = df.groupby(['TSA ID']).sum()
tsa_location_map = dict(zip(df_total_beds_available.index.get_level_values(0).drop_duplicates(), 
                            df_total_beds_available.index.get_level_values(1).drop_duplicates()))
df['TSA AREA'] = [tsa_location_map[tsa] for tsa in df.index]
df.set_index('TSA AREA', append=True, inplace=True)
df_cases = pd.DataFrame(df.stack())
df_cases.rename(columns = {0: 'cases'}, inplace=True)

# Load and parse daily case count data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasCOVID-19NewCasesOverTimebyCounty.xlsx'
df = pd.read_excel(url, sheet_name='New Cases by County', index_col=[0], header=2, nrows=255)
new_date_range = generate_date_range(df.columns)
new_date_range = new_date_range.drop([pd.Timestamp('2020-03-07'), pd.Timestamp('2020-03-08'), pd.Timestamp('2020-03-14')])
df.columns = new_date_range
df = df.loc[:, df.columns > '2020-04-11']
df.insert(0, 'TSA ID', [map_county_to_tsa(county) for county in df.index])
df = df.groupby(['TSA ID']).sum()
df.loc['Total'] = df.sum(axis=0) # Add total category
df['TSA AREA'] = [tsa_location_map[tsa] for tsa in df.index]
df.set_index('TSA AREA', append=True, inplace=True)
df_cases_new = pd.DataFrame(df.stack())
df_cases_new.rename(columns = {0: 'cases_new'}, inplace=True)

# Load and parse total death data
url = 'https://www.dshs.state.tx.us/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx'
df = pd.read_excel(url, sheet_name='Fatalities by County', index_col=[0], header=2, nrows=256)
new_date_range = generate_date_range(df.columns)
df.columns = new_date_range
df_new = df.diff(axis=1) # Extract daily death count
df.drop(index='UNKNOWN', inplace=True)
df = df.loc[:, df.columns > '2020-04-11']
df.insert(0, 'TSA ID', [map_county_to_tsa(county) for county in df.index])
df = df.groupby(['TSA ID']).sum()
df[df_cases.index.get_level_values(2)[-1]] = df.iloc[:, -1] # Replicate last column to match date extent of case data
df['TSA AREA'] = [tsa_location_map[tsa] for tsa in df.index]
df.set_index('TSA AREA', append=True, inplace=True)
df_deaths = pd.DataFrame(df.stack())
df_deaths.rename(columns = {0: 'deaths'}, inplace=True)

# Parse daily death data
df_new = df_new.loc[:, df_new.columns > '2020-04-11']
df_new.insert(0, 'TSA ID', [map_county_to_tsa(county) for county in df_new.index])
df_new = df_new.groupby(['TSA ID']).sum()
df_new['TSA AREA'] = [tsa_location_map[tsa] for tsa in df_new.index]
df_new.set_index('TSA AREA', append=True, inplace=True)
df_deaths_new = pd.DataFrame(df_new.stack())
df_deaths_new.rename(columns = {0: 'deaths_new'}, inplace=True)

# Merge the datasets
df = [df_total_beds_available, df_total_beds_occupied, df_icu_beds_available, 
      df_icu_beds_occupied, df_covid_inpatients, df_covid_icu_inpatients, 
      df_cases, df_cases_new, df_deaths, df_deaths_new]
df_merged = pd.concat(df, join='outer', axis=1).reindex(df_total_beds_available.index)

# Reset the index
df_merged.index.names = ['tsa', 'location', 'date']
df_merged.reset_index(inplace=True)
df_merged['tsa'] = df_merged['tsa'].apply(lambda x: x.replace('.', ''))

# Write unmodified data to CSV file
df_merged.to_csv('data.csv', index=False, float_format='%d', date_format='%Y-%m-%d')

# Manual removals of extreme values
df_merged.loc[(df_merged['tsa'] == 'N') & (df_merged['date'] == '2020-04-28'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-05-16'), 'cases_new'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'I') & (df_merged['date'] == '2020-05-31'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-06-07'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2020-06-16'), 'cases_new'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-14'), 'cases_new'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'P') & (df_merged['date'] == '2020-07-17'), 'cases_new'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-07-17'), 'cases_new'] = np.nan

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
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-25'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-25'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-07-26'), ['total_beds_occupied', 'icu_beds_occupied', 'covid_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-26'), ['icu_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'B') & (df_merged['date'] == '2020-07-26'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'E') & (df_merged['date'] == '2020-07-26'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'F') & (df_merged['date'] == '2020-07-26'), ['covid_inpatients', 'covid_icu_inpatients']] = np.nan
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

df_merged.loc[(df_merged['tsa'] == 'B') & (df_merged['date'] == '2020-07-27'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-07-27'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-07-27'), 'total_beds_available'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-07-27'), 'covid_inpatients'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-07-27'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'N') & (df_merged['date'] == '2020-07-27'), 'cases_new'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-27'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-27'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-27'), ['total_beds_occupied', 'total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2020-07-28'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-07-28'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-28'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-28'), ['total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-07-29'), ['total_beds_occupied', 'covid_inpatients', 'covid_icu_inpatients']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'O') & (df_merged['date'] == '2020-07-29'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'V') & (df_merged['date'] == '2020-07-29'), ['total_beds_available', 'icu_beds_available']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-07-31'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Q') & (df_merged['date'] == '2020-07-31'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-07-31'), 'covid_inpatients'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-08-01'), 'cases_new'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'M') & (df_merged['date'] == '2020-08-01'), 'icu_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'U') & (df_merged['date'] == '2020-08-01'), ['icu_beds_occupied', 'cases_new']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'F') & (df_merged['date'] == '2020-08-02'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'P') & (df_merged['date'] == '2020-08-19'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-08-28'), 'total_beds_available'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'P') & (df_merged['date'] == '2020-09-16'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-09-30'), 'cases_new'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-10-09'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-10-20'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-10-21'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'Q') & (df_merged['date'] == '2020-11-01'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'Total') & (df_merged['date'] == '2020-11-01'), 'covid_inpatients'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'S') & (df_merged['date'] == '2020-11-02'), 'icu_beds_available'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'D') & (df_merged['date'] == '2020-11-11'), 'cases_new'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'K') & (df_merged['date'] == '2020-11-17'), 'cases_new'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'L') & (df_merged['date'] == '2020-11-17'), 'icu_beds_available'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'A') & (df_merged['date'] == '2020-11-27'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-12-10'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2020-12-17'), 'cases_new'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'R') & (df_merged['date'] == '2020-12-17'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2020-12-18'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'L') & (df_merged['date'] == '2021-01-02'), 'covid_icu_inpatients'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'T') & (df_merged['date'] == '2021-01-07'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'H') & (df_merged['date'] == '2021-01-08'), 'icu_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2021-01-10'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2021-01-10'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2021-01-10'), 'total_beds_occupied'] = np.nan

df_merged.loc[(df_merged['tsa'] == 'C') & (df_merged['date'] == '2021-01-11'), 'total_beds_occupied'] = np.nan
df_merged.loc[(df_merged['tsa'] == 'G') & (df_merged['date'] == '2021-01-11'), ['total_beds_occupied', 'icu_beds_occupied']] = np.nan
df_merged.loc[(df_merged['tsa'] == 'J') & (df_merged['date'] == '2021-01-11'), 'total_beds_occupied'] = np.nan

# Eliminate negative values from cases_new
df_merged.loc[df_merged['cases_new'] < 0, 'cases_new'] = np.nan

# Write cleaned data to CSV file
df_merged.to_csv('docs/data.csv', index=False, float_format='%d', date_format='%Y-%m-%d')
