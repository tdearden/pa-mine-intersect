#%matplotlib notebook

import pandas as pd
import geopandas as gpd
import geoplot
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import shapely.geometry as shpgeo
import contextily as ctx


#spatial intersection using spatial index
def intersect_using_spatial_index(source_gdf, intersecting_gdf):
    source_sindex = source_gdf.sindex
    possible_matches_index = []

    # 'itertuples()' function is a faster version of 'iterrows()'
    for other in intersecting_gdf.itertuples():
        bounds = other.geometry.bounds
        c = list(source_sindex.intersection(bounds))
        possible_matches_index += c

    # Get unique candidates
    unique_candidate_matches = list(set(possible_matches_index))
    possible_matches = source_gdf.iloc[unique_candidate_matches]

    # Conduct the actual intersect
    result = possible_matches.loc[possible_matches.intersects(intersecting_gdf.unary_union)]
    return result

plt.ion()

#Load PA data
pa = gpd.read_file('data_files/WDPA_DRC_2021_proj.shp')

#Load mine data and transform to UTM
mines = gpd.read_file('data_files/osm_rd_congo_infrastructures_mining_fabrication.geojson')
mines = mines.to_crs('epsg:32733')
#print(mines.crs)


#Extract point features from mining dataset
mines_points = mines.loc[mines['geomtype']=="points"]
#print(mines_points.head)
#mines_points.man_made.unique()

#Save selection GeoJSON to SHP and load data
mines_points.to_file("data_files/osm_congo_mining_points.shp")
mines_shp = gpd.read_file("data_files/osm_congo_mining_points.shp")

## test plot METHOD 1
pa_map2, ax = plt.subplots(1, figsize=(10,8))
ax = pa.plot("DESIG_ENG", legend = True,ax=ax)
mines_shp.plot(ax=ax, color="red", markersize=1, legend = True)
pa_map2.suptitle('Protected Areas in the Democratic Republic of Congo and Mines')
ax.set_axis_off()
plt.show()

## test plot METHOD 2, no pa data, only some polygons

pa_map = plt.figure(figsize=(10, 10))
myCRS = ccrs.UTM(33, southern_hemisphere=True)
ax = plt.axes(projection=ccrs.Mercator())

#Add borders and coastline
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)

#Extent of map
xmin, ymin, xmax, ymax = pa.total_bounds
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

#Load PA data
pa_all = ShapelyFeature(pa['geometry'], myCRS,
                       edgecolor='black',
                       facecolor='palegreen',
                       linewidth=1)
ax.add_feature(pa_all)

mines_fig = ShapelyFeature (mines_shp['geometry'], myCRS,
                           edgecolor= 'red',
                           facecolor= 'red',
                           markersize=1)
ax.add_feature(mines_fig)

# test plot with
pa_map2, ax = plt.subplots(1, figsize=(10,8))
ax = pa.plot("DESIG_ENG", legend = True,ax=ax)
mines_shp.plot(ax=ax, color="red", markersize=1, legend = True)
pa_map2.suptitle('Protected Areas in the Democratic Republic of Congo and Mines')
ax.set_axis_off()
plt.show()

print(pa_map2)

#intersect using spatial index and count intersections
pa_mine_intersect = intersect_using_spatial_index(source_gdf=mines_shp, intersecting_gdf=pa)
intersection_cnt = gpd.sjoin(pa, mines_shp).groupby('NAME').size().reset_index()
intersection_cnt.head()

#Merge and plot
intersection_cnt = intersection_cnt.rename(columns={0: 'intersection_cnt'})
pa = pa.merge(intersection_cnt, on='NAME')
pa

#print maps with mines intersecting over PA

pa_maps = pa.groupby('NAME')
plt.figure()

for i, (name, pa_gdf) in enumerate(pa_maps):
    # create subplot axes in a 3x3 grid
    ax = plt.subplot(3, 3, i + 1)  # nrows, ncols, axes position
    # plot the continent on these axes
    pa_gdf.plot(ax=ax)
    # pa_mine_intersect.plot(ax=ax, color="blue")
    # set the title
    ax.set_title(name)
    # set the aspect
    # set extent
    # adjustable datalim ensure that the plots have the same axes size
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_axis_off()

plt.tight_layout()
plt.show()



