# Texas COVID-19 Hospital Resource Usage

Regional COVID-19 hospital resource usage in Texas based on [Department of State Health Services](https://dshs.texas.gov/) data. Powered by [D3.js](https://d3js.org/). Hosted on [GitHub Pages](https://pages.github.com/).

https://covid-texas.csullender.com/

## Sources

* Data from the [Texas DSHS](https://www.dshs.state.tx.us/coronavirus/additionaldata/)
* Legend generated using [d3-legend by Susie Lu](https://d3-legend.susielu.com/)

## About the Data

Data from the Texas Department of Health State Services are used for all metrics. The "Statewide Total" is manually calculated by aggregating values from all available trauma service areas (TSAs). This aggregation is incomplete because TSA-F (Paris) and TSA-R (Galveston) are missing data prior to May 29, 2020.

The following datapoints have been manually set to `NaN` because of reporting inconsistencies that interfere with graph generation. In most cases, the value was significantly smaller than the preceding or following day, which results in anomalously high percentages.

* `TSA I` > `2020-05-31` > `icu_beds_occupied`
* `TSA N` > `2020-04-28` > `total_beds_occupied`