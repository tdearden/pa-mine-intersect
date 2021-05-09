import os
import pywdpa
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.feature as cfeature

# Set WDPA_KEY - replace with your own token
os.environ["WDPA_KEY"]="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Check your token validity
pywdpa.get_token()

# Look up country 3-letter ISO code using pycountry
pycountry.countries.lookup('cd')

# Get protected areas from country from API and read head
pywdpa.get_wdpa("COD")

pa_COD = gpd.read_file("WDPA_COD_ALL.shp")
pa_COD.head()

# fetch the number of PA's under each category
pa_type = pa_COD.groupby('type')['wdpa_id'].nunique()
print(pa_type)

# Remove World Heritage Sites
pa_no_WHS = pa_COD.loc[pa_COD['type']!="World Heritage Site (natural or mixed)"]
print(pa_no_WHS)

#Save file for use in main tool
pa_no_WHS.to_file("WDPA_COD.shp")