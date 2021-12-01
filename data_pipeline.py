import pandas as pd
import lxml.html
import requests

def read_data():
    df = pd.read_excel(
        "Facilities in Industries that May be Handling PFAS Data 07-20-2021.xlsx",
        sheet_name='Data'
    )
    return df

# facility name
# lat, lon
# echo id
# industries are different

lat = []
lon = [] 
for index, row in df.iterrows():
    uri = row["ECHO Facility Report"]
    if uri == "-":
        continue
    response = requests.get(uri)
    html = lxml.html.fromstring(response.text)
    latitude = html.xpath("//span[contains(@id, 'Latitude')]")
    #lat.append(latitude.strip())
    longitude = html.xpath("//span[contains(@id, 'Longitude')]")
    #lon.append(longitude.strip())

    import code
    code.interact(local=locals())
    
    
    

