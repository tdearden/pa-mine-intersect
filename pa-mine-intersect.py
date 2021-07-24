#%matplotlib notebook

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

plt.ion()

#spatial intersection using spatial index
def intersect_sindex(source, intersecting):
    source_sindex = source.sindex
    possible_matches_index = []

    for other in intersecting.itertuples():
        bounds = other.geometry.bounds
        c = list(source_sindex.intersection(bounds))
        possible_matches_index += c

    # Get unique candidates
    unique = list(set(possible_matches_index))
    possible_matches = source.iloc[unique]

    # Conduct the intersect
    result = possible_matches.loc[possible_matches.intersects(intersecting.unary_union)]
    return result


#Load PA data
pa = gpd.read_file('data_files/WDPA_DRC_2021_proj.shp')
pa = pa.to_crs('epsg:32733')

#Load mine data and transform to UTM
mines = gpd.read_file('data_files/osm_rd_congo_infrastructures_mining_fabrication.geojson')
mines = mines.to_crs('epsg:32733')


#Extract point features from mining dataset
mines_points = mines.loc[mines['geomtype']=="points"]


#Save selection GeoJSON to SHP and load data
mines_points.to_file("data_files/osm_congo_mining_points.shp")
mines_shp = gpd.read_file("data_files/osm_congo_mining_points.shp")


#intersect using spatial index and count intersections
pa_mine_intersect = intersect_sindex(source=mines_shp, intersecting=pa)
intersection_cnt = gpd.sjoin(pa, mines_shp).groupby('NAME').size().reset_index()
intersection_cnt.head()

#First product: national map with all mines and protected areas, intersecting mines in red, basemap features, legend
pa_map, ax = plt.subplots(1, 1, figsize=(12, 12), subplot_kw=dict(projection=ccrs.Mercator()))

xmin, ymin, xmax, ymax = pa.total_bounds
ax.set_extent([xmin, xmax, ymin, ymax], crs=ccrs.Mercator())

ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)
pa_h = pa.plot("DESIG_ENG", legend=True, ax=ax, cmap="Greens", legend_kwds={'loc': 'lower left'})
mines_shp.plot(marker='o', ax=ax, color="blue", markersize=2, legend = True)
pa_mine_intersect.plot(marker='o', ax=ax, color="red", markersize=10)

pa_map.suptitle('Designated Protected Areas, Mining, and Mining Intersections in the Democratic Republic of Congo')
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
plt.savefig('drc_pas_mines_intersect.png',dpi=300)

#Merge intersections and plot
intersection_cnt = intersection_cnt.rename(columns={0: 'intersection_cnt'})
pa = pa.merge(intersection_cnt, on='NAME')
print(pa.head)
pa.to_csv('pa_mine_intersection_cnt.csv', header=True)

#print maps with mines intersecting over PA

pa_maps = pa.groupby('NAME')

plt.figure()

for i, (name, pa_gdf) in enumerate(pa_maps):
    # create subplot axes in a 3x3 grid
    ax = plt.subplot(3, 3, i + 1)
    # plot the pa on these axes
    pa_gdf.plot(ax=ax, column='NAME', cmap='jet')
    pa_mine_intersect.plot(ax=ax, color="red", markersize=2, marker='o')
    # set the title
    ax.set_title(name, fontsize='7')
    # set the extent
    xmin, ymin, xmax, ymax = pa_gdf.total_bounds
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # plots have the same axes size
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_axis_off()

plt.tight_layout()
plt.show()

plt.savefig('drc_pa.png',dpi=300)


