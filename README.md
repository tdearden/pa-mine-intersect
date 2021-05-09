<h1>pa-mine-intersect Rationale</h1>
<p> This tool provides a method of finding intersects between mining points and protected area polygons in the Democratic Republic of Congo. This is achieved through the creating spatial indexes to examine intersections between the two files. The expected results include: a .png national-level map of protected areas, mining points and points of intersection; a CSV of all protected areas with the number of mining points intersecting the polygon; and a .png figure with subplots of the locations of the mines within the protected areas. This tool could be scalable to different countries and protected areas. </p>
<p> The rationale for creating this tool was to track and monitor voluntary GIS activity tagged as “mining” which could be occurring in areas with high biodiversity value.</p>

![screenshot](https://user-images.githubusercontent.com/41048297/116794842-8965c600-aad0-11eb-8384-f70d8b0506c5.png)


<h1>Installation</h1>
The requirement for running the code is to create a conda environment containing the packages needed to run the functions in python. After downloading or cloning the GitHub repository, from the conda command line use the environment.yml file to create the new conda environment. This can be done by using the following prompt: 

`conda env create -f /__yml file path__/environment.yml`

Replacing the _yml file path_ to location of the environment.yml file.  

The packages required to run the code are:
<ul><li>	cartopy.crs
</li><li>	cartopy.feature
</li><li>	geopandas
</li><li>	matplotlib
</li><li>	contextily
</li></ul>
Activate the newly created environment and use it to run the tool. For explanatory and visual purposes, a completed version of this code has been uploaded to the GitHub Repository as a Jupyter Notebook file: pa-mine-intersect-tutorial.ipynb. 

<h2>Data Preparation</h2>
The data for this example are available in the data_files folder. It is recommended to use this as an initial test, as it has been prepared specifically for this tool. However, if you wish to download the data from the source, or test it using different datasets, instructions for that are provided here. 

The Protected Planet <a href="https://www.protectedplanet.net/country/COD"> “World Database on Protected Areas”</a> data can be downloaded from the website, at a global, national, or protected area level, without restriction. For the purpose of this tool, the data was adapted to remove sites tagged as “UNESCO World Heritage Sites”, primarily because these are not necessarily related to high-value biodiversity areas. If you have an API token for the Protected Planet datset, the .py file in wdpa-api will assist in selecting country by ISO code and downloading and extracting shapefiles. 

The data required for the OSM mines file was downloaded from the DRC OSM team, through HDX <a href="https://data.humdata.org/dataset/democratic-republic-of-congo-drc-infrastructures-mining-and-fabrication-openstreetmap-export">at this link</a>. The data can also be extracted from Geofabrik or Planet.OSM. This data contains all OSM features within the boundaries of the Democratic Republic of Congo which have been tagged with the Thematic Variable = Infrastructures, Mining, Fabrication. This includes points, lines, polygons, and multipolygon features and can be downloaded as .CSV or .GeoJSON. While this data could be used unaltered, for the purpose of this tool point features were extracted and used exclusively for the intersect. 

<h1> Expected Results </h1>
<p>The expected results are: <ol>
<li>A 12 x 12 .png map of all the protected areas (by designation), with mining points, and a basemap for context.  
</li><li>A CSV of the PAs which have mining activity intersections, with the number of intersections of mining.  
</li><li>A .png figure of subplots of each of the polygon protected areas and the mining intersections. 
</li></ol></p>

<h1>Known Issues</h1>
<p>The following issues have been identified: <ul>
<li>When loading the packages, the following warning can be expected, which does not affect the expected result: 
<br><i>
UserWarning: The Shapely GEOS version (3.9.1-CAPI-1.14.2) is incompatible with the GEOS version PyGEOS was compiled with (3.9.0-CAPI-1.16.2). Conversions between both will be slow.
  warnings.warn(</i><br>This will not affect the expected results. </li>
<li>When converting the .geoJSON mining file to .shp, the following warning can be expected, which does not affect the expected result: 
<br>
<i>UserWarning: Column names longer than 10 characters will be truncated when saved to ESRI Shapefile. mines_points.to_file("data_files/osm_congo_mining_points.shp")
</i></li>
<li>Virguna National Park is mapped twice in the final subplots. This is because it has been registered as both a National Park and a Ramsar Heritage Site on Protected Planet, meaning there are two polygons to represent the same area. </li>

</ul>
</p>
