# Texas COVID-19 Hospital Resource Usage

Regional COVID-19 hospital resource usage in Texas based on [Department of State Health Services](https://dshs.texas.gov/) data. Powered by [D3.js](https://d3js.org/). Hosted on [GitHub Pages](https://pages.github.com/).

https://covid-texas.csullender.com/

## Sources

* Hospitalization and COVID-19 data from [Texas DSHS](https://www.dshs.state.tx.us/coronavirus/additionaldata/)
* Average staffed hospital bed occupancy rate for Texas as reported by [NCHS](https://www.cdc.gov/nchs/index.htm) in [_Health, United States, 2017_](https://www.cdc.gov/nchs/hus/contents2017.htm#Table_091).

## About the Data

Hospital data reported daily by the [Texas Department of Health State Services](https://dshs.texas.gov/) are used for all metrics. The "Statewide Total" is manually calculated by aggregating values from all available [trauma service areas](https://www.dshs.texas.gov/emstraumasystems/etrarac.shtm) (TSAs). This aggregation is incomplete for bed counts prior to May 29, 2020, because of fragmented reporting from TSA-F (Paris) and TSA-R (Galveston). All data is incomplete between July 23 to July 28 [due to a transition in hospital reporting](https://www.kxan.com/news/coronavirus/hospitalizations/18-of-texas-hospitals-arent-reporting-complete-data-dshs-says/) to comply with new federal requirements.

The unmodified daily data is available in [`data.csv`](data.csv). A cleaned version of the data removing inconsistencies that interfere with graph generation is available in [`docs/data.csv`](docs/data.csv). Datapoints were manually excluded if they differed significantly from the preceding or following day and resulted in extreme graph values. These manual curations can be seen in the update script [`fetch.py`](fetch.py).
