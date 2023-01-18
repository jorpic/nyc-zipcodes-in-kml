#!/usr/bin/env python

import os
import sys
import geopandas

file = sys.argv[1]
(name, _) = os.path.splitext(file)

### read shapefiles
f = geopandas.read_file(file)
print(len(f), "shapes found")

# ZIP_CODE_040114 shapes use ESRI:102718 projection but
# KML by specification uses only EPSG:4326.
g = f.to_crs(epsg=4326)

### create KML
from simplekml import Kml, Color, Style, LineStyle, PolyStyle

colors = [
    Color.lightblue,
    Color.lightcoral,
    Color.lightcyan,
    Color.lightgoldenrodyellow,
    Color.lightgray,
    Color.lightgreen,
    Color.lightgrey,
    Color.lightpink,
    Color.lightsalmon,
    Color.lightseagreen,
    Color.lightskyblue,
    Color.lightslategray,
    Color.lightslategrey,
    Color.lightsteelblue,
    Color.lightyellow,
    Color.lime,
    Color.limegreen,
    Color.linen,
    Color.magenta,
    Color.maroon]


styles = list(map(lambda color: Style(
    # FIXME: don't know how to get nicer icons
    linestyle = LineStyle(width = 7, color = color),
    polystyle = PolyStyle(color = Color.changealpha('66', color))
    ), colors))


kml = Kml()
polygons = kml.newfolder(name="Polygons")
### add polygons
for i, p in g.iterrows():
    zipcode = p["ZIPCODE"]
    coords = p["geometry"].exterior.coords
    pol = polygons.newpolygon(name = zipcode, outerboundaryis = list(coords))
    pol.description = f"{zipcode}, {p['COUNTY']}, {p['PO_NAME']}"
    pol.style = styles[i%len(styles)]

### add points
points = kml.newfolder(name="Points")
for i, p in g.iterrows():
    zipcode = p["ZIPCODE"]
    center = p["geometry"].representative_point()
    pnt = points.newpoint(name = zipcode)
    pnt.description = f"{zipcode}, {p['COUNTY']}, {p['PO_NAME']}"
    pnt.coords = [(center.x, center.y)]

file = f"{name}.kml"
print("writing them to", file)
kml.save(file)
