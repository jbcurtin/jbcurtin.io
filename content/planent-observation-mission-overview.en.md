+++
title = "Planent Observation Mission Overview"
template = "page.html"
# date = 2020-07-25T11:00:00Z
date = 2020-07-26T11:00:00Z
draft = false
[taxonomies]
categories = ["astronomy", "remote sensing", "mercury", "landsat"]
[extra]
summary = "Determining and building the correct array of instruments for your satellite is a fairly involved process. For each instrument, you'll need to teach hardware engineers enough about your realm of science in order to have an instrument built. In the case of remote sensing, there is already a large array of instruments from past missions we can pull from."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

Determining and building the correct array of instruments for your satellite is a fairly involved process. For each instrument, you'll need to teach hardware engineers enough about your realm of science in order to have an instrument built. In the case of remote sensing, there is already a large array of instruments from past missions we can pull from.

Hi, and welcome to my website. I'm teaching myself how to build small satellites. Part of the process is identifing and understanding what a small satellite or CubeSat could be used for. Highlighting a focus on the mission design for such satellites. This article is meant to broaden my understanding of what is built vs what is delivered to a scientist so I may better understand the data pipeline from sensor-to-data product.

At the heart of every scientific-focused mission is the output of data corrolated to the a unique implementation of science product. We'll walk through a number of spacecraft and determine the output of each as we look for ideas on how to observe Earth and other planets.

This article has the following sections
* Earth Observation
* Interplanetary Observation

## Earth Observation

Earth Observation is a blanket term for describing the process of sensing various forms of anomaly using remote sensing capability. Some examples include detecting cloud coverage and movement, land mapping, magnetic field mapping, solar wind mapping, or ozone mapping.

### CloudSat

CloudSat's primary mission is to track clouds over planet earth. Using an instrument specifically designed to measure distance between the spacecraft and clouds, the remote sensor is capable of capturing distance data between the two objects. Scientstists are then able to cross reference the satellite location with LiDAR point cloud data and determine how clouds move over the surface of the earth and how that movement influances larger patterns such as hurricane development and el nino weather patterns.

#### Data Product
CloudSat sits in a [Sun-synchronous Orbit](https://en.wikipedia.org/wiki/Sun-synchronous_orbit), currently apart of a large satellite constellation including [Aqua](https://aqua.nasa.gov/), [PARASOL](https://parasol.cnes.fr/en/PARASOL/index.htm), and [Aura](https://aura.gsfc.nasa.gov/). Following the product name, [this table](https://cloudsat.atmos.colostate.edu/data) can be used to find which [data product](https://www.cloudsat.cira.colostate.edu/) you maybe interested in. Its possible to find a [complete guide](https://www.cloudsat.cira.colostate.edu/cloudsat-static/info/dl/2b-cldclass-lidar/2B-CLDCLASS-LIDAR_PDICD.P1_R05.rev0_.pdf) on how the data product is put together.

#### Additional CloudSat Details
* [https://eospso.nasa.gov/missions/cloudsat](https://eospso.nasa.gov/missions/cloudsat)


### Landsat 8 & 9

Landsat's primary mission is to image earth using an optical camera in tandum with imaging earth using an infered sensor. The two sensors, Operational Land Imager (OLI) and the Thermal Infrared Sensor (TIRS) image Earth and provide coincident images, surface images of costal lines, polar ice, islands and continental areas. Landsat 9 a continuation of the Landsat 8 mission.

#### Data Product

Most data product for the Landsat satellites can be accessed from [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/). Under the tab DataSets, using the Data Set Search bar enter the works "Landsat". When selected, it'll highlight and select some Landsat data sets. Goto the Results tab, make sure Landsat is selected. 

{% round_circuit_note(title="This is the best I could figure out the user interface,") %}
I'm not sure why they don't offer something which allows you to export the current bounding box of the map for OLI data or TIRS data. - Try accessing the data without any parameters input in the search query.
{% end %}

#### Additional Landsat 8 & 9 Details
* [https://eospso.nasa.gov/missions/landsat-8](https://eospso.nasa.gov/missions/landsat-8)
* [https://eospso.nasa.gov/missions/landsat-9](https://eospso.nasa.gov/missions/landsat-9)
* [https://landsat.gsfc.nasa.gov/data/data-details/](https://landsat.gsfc.nasa.gov/data/data-details/)

#### Lava Mapping

Paraphrasing a paper from 2004, "Mapping recent lava flows at Westdahl Volcano, Alaska, using radar and optical satellite imagery", 'We combined information from synthetic aperture radar (SAR) images with multispectral Landsat-7 data to differentiate the 1991–1992 flow from the 1964 flow and a pre-1964 flow, and to calculate the flow areas (8.4, 9.2, and 7.3 km2, respectively).'

* [https://pubs.er.usgs.gov/publication/70027032](https://pubs.er.usgs.gov/publication/70027032)

## Interplanetary Observation

When sensors perform well and enough science is known to create map. We send that technology via probe to another planent. Some properties of rocky planents include a magnetic field which helps block electro magnetic radiation from the sun; the iron core is spinning and produces what is called a [dynamo](https://en.wikipedia.org/wiki/Dynamo_theory). Dynamos create a magnetic field which will reflect radiation from the surface of the planet. 

On the BepiColombo Transfer Module, are two Orbitors. Mercury Planet Orbitor(MPO) and Mercury Magnetospheric Orbitor(MMO). MPO is focused on measuring and mapping the terrain of Mercury while the MMO is focused on measuring and mapping properties of the magnetosphere around Mercury.

* [https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Transfer_Module](https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Transfer_Module)
* [https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Journey_to_Mercury](https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Journey_to_Mercury)


### Mercury Planetary Orbitor
BepiColombo Laser Altimeter (BELA) is used to map the surface of the planet. The output of this product is a point-cloud from a laser focused at mapping the elevation of the surface directly under the probe. This information along with the acceleration and position in the magnetic field can be cross-correlated to develop data product with enough detail to find rover landing sites on the surface of Mercury.

* [https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Planetary_Orbiter](https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Planetary_Orbiter)

### Mercury Magnetospheric Orbitor
Understanding the protections Mercury provides while on the surface is important, as it may influance how probes might be created for the planent. The Mercury Magnetospheric Orbitor measures properties of the magnetosphere in orbit around the planent and its interaction with the magnetic field. From understanding how solar wind affects the magnetosphere to understanding how the magnetic field reinforces the magneticsphere, the orbitor is equiped to measure the intensity of solar wind and dynamo producing electric fields from the core of the planent.

* [https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Magnetospheric_Orbiter](https://www.esa.int/Science_Exploration/Space_Science/BepiColombo/Mercury_Magnetospheric_Orbiter)