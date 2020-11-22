# Watershed & Stream Delineation Tool

This tool allows a user to delineate watersheds and streams using Digital Elevation Model (DEM) raster(s) and outlet point(s) provided by as an input in ArcGIS pro. The tool is built on ArcPy module, an ESRI Python package to extend the functionalities of ArcGIS products. It is suitable for hydrologists, researchers and scientists working with watershed, hydrologic and engineering projects and studies.

There are two ways in which outlet(s) (pour points) can be provided to delineate watersheds and streams: 1) user can load their own shapefile containing point feature(s) or 2) user can select point(s) on any base map (for reference) using the pencil tool next to drop down button.    

# How to use the tool?

Go to this [link](https://1drv.ms/u/s!Ak8N6yOD29xEqT4ax-ypDd4LoWWj?e=NgI3S1) to download the zipped workspace.

Open `Watershed-Stream-Delineation.aprx`. From catalog pane expand `Watershed-Stream-Delineation.tbx` under `Toolboxes`. Double click `Watershed Stream Delineation Tool`.  

## Inputs

##### Elevation raster(s)

Select a single or multiple Digital Elevation Model (DEM) raster(s) of the geographical area you are interested. Multiple rasters are automatically joined to create a single raster. DEMs should be located from your local drive and file path should not contain any spaces to avoid error. 

A few example DEMs are provided in the `data` folder for testing purpose. The folder `test_1` has a single DEM from an area in Wake County, NC. The folder `test_2` has 4 DEMs that geographically align next to each other. `test_2` files can be used to test inputting multiple rasters. 

More DEMs can be found at USGS's [National Map](https://viewer.nationalmap.gov/basic/#/) service 


##### Outlet(s)

There are two ways to load outlet points. 
1. Load a shapefile containing point feature(s) from your local drive.
2. 
*Note - Outlet(s) should be near point

## Outputs

## Run 2 test modes

# How to configure ArcGIS pro to run the tool?

This section is for users who are only interested in using the .py script in their projects. 

## Parameters

## Symbology

# How are folders organized?

# How the tool works?

Step by step process

# Notes

User can check the status of the tool by clicking on View Details under Messages.

Coordinate reference systems of all inputs, intermediary files and output are changed  based on the first DEM selected in the tool.

# 