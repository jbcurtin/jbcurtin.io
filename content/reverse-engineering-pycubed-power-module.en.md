+++
title = "Reverse Engineering PyCubed Power Module"
template = "page.html"
date = 2020-07-17T11:00:00Z
draft = true
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = ""
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

This walkthrough reverse engineering is less of a tutorial and more of structure notes on what it took me to understand how to design circutry and design a Solar/Batter charging circut. PyCubed just so happens to be well documented enough for me to understand the symbols. My notes here are meant as a guide to help those just getting started, to understand what the defferent parts of the curcicut will do. Please bear with me, as I learn how to build by own circuts.

This post is divided up into sections
* Figuring out which software to use
* Finding a schematic to load
* Breaking the Schematic into sections

## Figuring out which software to use

The two most promantent software packages which come to mind are [KiCad](https://www.kicad.org/download/)(open-source) and [EasyEDA](https://easyeda.com/). I'm not well experienced with either, from a quick glance EasyEDA has a massive component list. KiCad provides a considerable amount as well. For this write-up, I've decided to use KiCad to explore the schematics designed by [PyCubed's](https://pycubed.org/) author, [Max Holliday](https://github.com/maholli).

## Finding a schematic to load

With the software choosen, lets move to loading the latest schematic from PyCube's [hardware repository](https://github.com/pycubed/hardware/tree/master/mainboard-v05). Download [Power.sch](https://raw.githubusercontent.com/pycubed/hardware/master/mainboard-v05/Power.sch) and open it in KiCad.

## Breaking the Schematic into sections

With the schematic loaded, lets breakdown the components into groups which can be further researched, to help better understand the overall design.

## VSolar 9v to 40v
![vsolar-9v-to-40v](/images/VSolar-9v-to-40v.png)

## GPS Power

![gps power curicut](/images/GPS-Power.png)

## USB Charging two cell Li-On

![USB-Charging-for-two-cell-Li-On](/images/USB-Charging-for-two-cell-Li-On.png)

## Batter Power Monitor

![Batter-Power-Monitor](/images/Batter-Power-Monitor.png)

## Radio VDD Select and RF Regulator

![Radio-VDD-Select-and-RF-Regulator](/images/Radio-VDD-Select-and-RF-Regulator.png)

## One Shot Regulator Reset and Regulator 3.3V Out

![One-Shot-Regulator-Reset-and-Regulator-3-dot-3V-Out](/images/One-Shot-Regulator-Reset-and-Regulator-3-dot-3V-Out.png)