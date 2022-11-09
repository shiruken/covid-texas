[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501307.svg)](https://doi.org/10.5281/zenodo.5501307)

# Texas COVID-19 Hospital Resource Usage

### _This website is no longer being regularly updated as of August 24, 2022, after Texas DSHS ended its daily data releases. Manual record requests may be used to intermittently update the data._

Regional COVID-19 hospital resource usage in Texas based on [Department of State Health Services](https://dshs.texas.gov/) data. Powered by [D3.js](https://d3js.org/). Hosted on [GitHub Pages](https://pages.github.com/).

https://covid-texas.csullender.com/

## Sources

* Hospitalization and COVID-19 data from [Texas DSHS](https://www.dshs.state.tx.us/coronavirus/additionaldata/)
* Historic hospital occupancy rate as reported by [NCHS](https://www.cdc.gov/nchs/index.htm) in [_Health, United States, 2017_](https://www.cdc.gov/nchs/hus/contents2017.htm#Table_091).

## About the Data

Hospital data reported daily by the [Texas Department of Health State Services](https://dshs.texas.gov/) are used for all metrics. The "Statewide Total" is manually calculated by aggregating values from all available [trauma service areas](https://www.dshs.texas.gov/emstraumasystems/etrarac.shtm) (TSAs). This aggregation is incomplete for bed counts prior to May 29, 2020, because of fragmented reporting from TSA-F (Paris) and TSA-R (Galveston). All data is incomplete between July 23 to July 28, 2020, [due to a transition in hospital reporting](https://www.kxan.com/news/coronavirus/hospitalizations/18-of-texas-hospitals-arent-reporting-complete-data-dshs-says/) to comply with new federal requirements.

The unmodified daily data is available in [`data.csv`](data.csv). A cleaned version of the data removing inconsistencies that interfere with graph generation is available in [`docs/data.csv`](docs/data.csv). Datapoints were manually excluded if they differed significantly from the preceding or following day and resulted in extreme graph values. These manual curations can be seen in the update script [`fetch.py`](fetch.py).

The "average annual occupancy rate" shown on the Statewide Hospital Bed Usage chart is based on the annual [_Health, United States_](https://www.cdc.gov/nchs/hus/index.htm) report by the [National Center for Health Statistics](https://www.cdc.gov/nchs/index.htm) (NCHS). [Table 91](https://www.cdc.gov/nchs/hus/contents2017.htm#Table_091) details the average annual occupancy rate in community hospitals for each state, with Texas reporting 60% occupancy in 2015. This number was further validated with the [Acute Care Hospitals report](https://dshs.texas.gov/chs/hosp/hosp5/) from the [Texas DSHS Center for Health Statistics](https://www.dshs.state.tx.us/chs/), which reported 60.4% staffed bed occupancy in 2016.


# Texas COVID-19 Vaccine Tracker

Texas COVID-19 vaccine distribution tracker based on [Department of State Health Services](https://dshs.texas.gov/) data. Powered by [D3.js](https://d3js.org/). Hosted on [GitHub Pages](https://pages.github.com/).

https://covid-texas.csullender.com/vaccine/

## Sources

* Vaccination data from [Texas DSHS](https://www.dshs.state.tx.us/coronavirus/additionaldata/)
  * Archive of daily Excel spreadsheets available [here](https://github.com/shiruken/covid-texas-data/tree/main/AccessibleVaccineDashboardData)
* Population data from [U.S. Census Bureau](https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-detail.html) and [Texas Demographic Center](https://demographics.texas.gov/Data/TPEPP/Estimates/)

## About the Data

Vaccination data [reported daily](https://tabexternal.dshs.texas.gov/t/THD/views/COVID-19VaccineinTexasDashboard/Summary) by the Texas Department of Health State Services are used for all metrics. The number of vaccine doses administered, number of people vaccinated with one dose, number of people fully vaccinated, and number of people with booster doses are aggregated by the *recipient's county of residence*. Weekly allocations/shipments to each county were stopped on the week of May 3, 2021, due to there being a sufficient supply of vaccine. These metrics have been removed from the tracker (final update available [here](https://github.com/shiruken/covid-texas/blob/73c6a5f41c4f01005f89c4dfdb43b8665307dc2b/data.csv)). Health care providers have 24 hours after a dose is administered to enter information into the Texas Immunization Registry (ImmTrac2). The daily data comes from vaccination records submitted by health care providers as of 11:59 PM the previous night. Population numbers are based on 2019 estimates from the [U.S. Census Bureau](https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-detail.html) and [Texas Demographic Center](https://demographics.texas.gov/Data/TPEPP/Estimates/).
