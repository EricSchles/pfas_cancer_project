# Understanding the Link Between Cancer and PFAS

The goal of this project is to see if there is a correlation between cancer rates and elevated levels of PFAS due to nearby dumping facilities.

Note:

All results in this repository are _preliminary_, the facts have not been verified in a rigourous way as of yet.  

Be skeptical and don't trust this yet.

# Data Sources

https://echo.epa.gov/ is the source for [Facilities in Industries That May Be Handling PFAS](https://github.com/EricSchles/pfas_cancer_project/blob/main/data/Facilities%20in%20Industries%20that%20May%20be%20Handling%20PFAS%20Data%2007-20-2021.xlsx)

https://statecancerprofiles.cancer.gov/ is the source for [uscs_cancer_incidence](https://github.com/EricSchles/pfas_cancer_project/blob/main/data/uscs_map_incidence_all.csv) - this download is the 2013 data.

https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html is the source for [census data 2019](https://github.com/EricSchles/pfas_cancer_project/blob/main/data/2019_Census_US_Population_Data_By_State_Lat_Long.csv)

## Docker

Docker steps:

* `docker build -t build_file .`
* `docker run -d build_file`