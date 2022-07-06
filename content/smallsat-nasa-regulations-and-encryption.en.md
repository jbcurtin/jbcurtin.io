+++
title = "Smallsat NASA Regulations about Amature CubeSats"
template = "page.html"
date = 2020-07-06T15:00:00Z
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = "Overview of possible CDH implementations."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

In my research on SmallSat deployment using CubeSat Platforms, I've started to find myself gravitaing towards the Command and Data Handling subsystem design. What peaked my interest was a thought experiment around implemening secure command reception and actknowledgement for satellite communication using unencypted payloads.

When communicating with a smallsat, multiple factors have to be taken into consideration for successful operation. For brevarity and scenero construction, lets focus and create some assumptions about how communication is established between a ground station and an orbiting SmallSat. You've setup a ground station on the top of your roof and it just so happens to fall within the ground track of the smallsat you've successfully launched into low earth orbit(LEO). From here you have about 10 minutes of continuos communcication with your smallsat per day. The smallsat also has enough power to provide continues communication at 2mbs. Commands sent to and received only take about 100k at max, but the problem you run into is that your smallsat won't be accessable for another 24 hours, until it fully orbits the earth.

The form factor for the smallsat is 3U, the mimimum nessicary for stablization and propuslion systems to be included in the CubeSat(smallsat) payload. Now we have a bus with strict hardware/payload considerations. We've allocated 1U for the Data Processing Unit and 1/2U for propulsion. Our mission is scientific in nature, which requires stabalization of the CubeSat. We'll be observing wheather patters using an optical camera. Specifically, we're interested in creating a map of Cloud Coverage over a section of the Earth. Let's focus on examing Cloud Coverage over 日本( Japan ).

* Research Points
    - Mission(s) analysisng Cloud Coverage over a section of the Planent
    - Types of Sensors used in 3U CubeSat to capture photos
    - Types of Data Processing Units used to store content until it can be transmitted to a Ground Station
    - Mission Design