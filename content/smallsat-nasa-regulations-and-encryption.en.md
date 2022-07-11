+++
title = "CubeSat Regulations, Amature License, & Encryption"
template = "page.html"
date = 2020-07-06T15:00:00Z
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = "Overview of possible CDH implementations."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++


## Introduction

In my research on SmallSat deployment using CubeSat Platforms, I've started to find myself gravitaing towards the Command and Data Handling subsystem design. What peaked my interest was a thought experiment around implemening secure command reception and actknowledgement for satellite communication using unencypted payloads.

This post is not a mission plan, instead it is posted for two reasons. First, to help those behind me piece together how to develop mission plans. If you find yourself a university student or someone interested in launching a space vehicle into space. I hope you find this content helpful. Secondly, its to assist with collecting feedback from those more involved and more active in current space-related industry, creating a fourm for feedback so I can have an oppertunity to correct my misunderstandings as I work out how everything works together. The format of this post is meant to (eventually) resemble a mission plan.

This post is parsed into four sections, first two sections are dedicated to detailinng the composition of CubeSat 3U, providing enough detail to understand the Mission Objective and hardware integration. The final three sections will focus on designing a subsystem for Command, Command Verification, and Data Transmission.

* Mission Objective & Overview
* Space Vehicle & Ground Station Components
* CubeSat Regulations & License Requirements
* Unencrypted Command & Integrity Verification
* Unencrypted Data Transmission & Integrity Verification

## Mission Objective & Overview

The objective our mission is to collect data about cloud coverage and other environmental factors over Japan. Specifically, we're interested in creating a map of Cloud Coverage over Japan which will provide us with information on how climate change is effecting Japan's typhoon season.

As typhoon season approaches, we'll want to extend our observations from mainland-Japan into the sorrounding seas. CubeSat 3U will orbit Earth in [Low Earth Orbit](https://en.wikipedia.org/wiki/Low_Earth_orbit), providing us with the ability to image the same region(s) of Earth up to twelve times in a single day. Six times with sunlight and six times without sunlight.

### Earth Observation

The science data we are expecetding to extract from our images include depth of cloud calculation based on how much light is reflected from clouds. We're also interested in knowing how much percipitation is being dropped in a region at any given point in time. Lastly we want to come up with a percentage figure of how much cloud is in a given image, providing us with the ability to approximate how much cloud coverage Japan recieves on any given day.

### Data Processing

Data onboard CubeSat 3U will be store in a compressed format. Images will be taken and compressed in a data-bank aproximently 128GB in size. Data Handling algorthims will check the integrity of the data while the satellite is outside of the imaging bounding box. After files have been verified and a downlink is establised, data will be sent to a ground station, verified transmission as a success, and the image data is deleted from the onboard storage device.

### Orbital Plan

CubeSat 3U will be launched into Low Earth Orbit ( LEO ). It just so happens the satellite ground track passes over our ground station just right. We'll recieve a strong signal from our hardware, providing a downlink of 2MB/sec and uplink of 500KB/sec. The full orbit will be about 100 minutes, providing our ground station with 15 minutes of continuous communication to send commands and recieve telemetry. CubeSat will fly at about 600 meters above Earth's surface. To correct the Orbit, reaction wheels will activate on three axis to reduce angular momentum and stablize optical sensors and point the sensors towards Earth.

## Space Vehicle & Ground Station Components

### Space Vehicle

When communicating with a smallsat, multiple factors have to be taken into consideration for successful operation. Lets focus and create some assumptions about how communication is established between a ground station and an orbiting CubeSat 3U. You've setup a ground station on the top of your roof. The smallsat also has enough power to provide continues communication and perform mission critical operations at the same time.

The platform we'll use for smallsat is CubeSat 3U. CubeSat 3U bus has strict hardware/payload considerations. 2/3U goes to Optical Imaging, 1/3U goes to Data Processing and Command Control.

#### Software Operating System

In order to save resources and time, we'll use a Linux Kernel to manage and develop new software. There are [resources](https://github.com/fishinabarrel/linux-kernel-module-rust) today, available for implementing new kernel modules using [Rust](https://www.rustlang.com/).

#### Guidance Navigation & Control ( GN&C )

Guidance will include numerious varibles in the code written. Taking in sensor data from various sensors, Control will provide numerical values for calculations in the GN subsystem.

##### Attitude Determination & Control ( AD&C )

In order for CubeSat 3U to take images of Earth while passing over Japan, we'll need to stablize the optical camera in a single direction for long periods of time. In order to do this, we'll also need to know which direction Earth is, which section of the Earth we're pointing at. Tagging the data appriatly while we're doing this. It'll require design of a custom tagging database along with figuring out when images are taken and at which time. We'll than corrate the images with the GN&C subsystem to determine which section of the sky was imaged at that percise moment in time.

###### Reaction Wheel

To stablize and manage CubeSat 3U, we'll engineer a 1U payload with three reaction wheels which will provide angular momentum to despin the craft and momentum dumping capabilities.

###### Magnetometer

A magnetometer will be mounted in the top-section of the Cubsat, taking up the top-half of the CubeSat vehicle. It'll take measurements of Earth's Magnetic Field, which will be sent to AD&C subsystem for attidute adjustments to be carried out by the responding astern reaction wheels.

###### Light Sensing Diodes


#### Command, Data Handling, Security & Verification ( CDHSV )

The remaining 1 and 1/3U of the CubeSat 3U will be reserved for onboard Processing for Command, Data Handling, and Security & Verification hardware. Command accepts uplink commands sent from an authenticated ground station. Data Handling prepares data for download to a ground station. Security & Verification provides a security framework onboard the satellite to make sure agents and actors are properly authenticated and authorized.

##### Command

Command Software Module ( CSM ) controls the actions of CubeSat 3U. Having direct interaction between all functioning components within the vehicle. Capable of receiving uplink commands from a ground station. When a command is recieved, it is first verified to make sure the command came from an authorized ground station. When accepted, CSM then proceeds to decide what kind of command was sent.

If the command sent was a flight related command, it'll be sent to Satellite Attitude Determination and Control System ( ADCS ).

If the command sent was for an alteration to capture a different section of Earth Observation

If the command sent was for a data download request or data stop request, the command is sent to Instrument Data Processor Unit ( IDPU ).

All commands sent, are routed through the Security & Verification Hardware Module for command verification and ground station authorization. Ensuring only authorized commands can alter the state of the space vehicle.

###### Satellite Attitude & Articulation Determination and Control System ( AADCS )

Comand provides the interface to alter the dynamics of the space vehicle. Capable of changing the orbit and orienting the satellite towards the correct spot on Earth. Command Flight Control provides the capability to change the mission design while in flights as well.

The controls for CubeSat 3U are divided into algorithms.

* Momentum Dumping
* Orbit Raising Maneuver - increases the semi-major axis. Examples include drag makeup (DMU) maneuvers, which counteract the effects of atmospheric drag and re-initialize the circulation orbit for a satellite; some types of risk mitigation maneuvers (RMMs) are executed to avoid orbital debris; and ascent maneuvers for putting new satellites into the mission's orbital location.
* Orbit Lowering Maneuver - decreases the semi-major axis. Examples include braking maneuvers used to avoid exiting theconstellation control box; some types of risk mitigation maneuvers (RMMs) are executed to avoid orbital debris; and exit maneuvers for satellites leaving their nominal orbital location.
* De-Spin
* Inclination adjust maneuve - performed periodically to maintain the mission's Mean Local Time (MLT) in a pre-specified range


##### Data Handling
##### Security & Verification

Security & Verification module will provide a high-level API available to other components of the satellite. Complete messages will be sent to the Hardware Security Module ( HSM ) and resigned for uplink data transmission and data onboard the device will be signed for downlink transmission.

#### Command

Commands recieved from a ground station will be validated using Security & Validation Subsystem. 

When a command is accepted, the command module takes the command and interprets the command into an action. For example, the attitude of the satellight might be off by 25km, making an adjustment using Reaction Wheels to dump forward momentum and than desaturate the momentum wheels by dumping the stored momentum would take two commands. Controlls for the Satelight will be tightly bound to the ground station, each command will be ran through a simulation prior transmission in order to make sure model and unit stay in sync.


Commands recieved from a ground station will first be validated using Security & Verification 
Commands recieved and transmitted from CubeSat3U will contain cryptograhic signatures, signed using onboard hardware and subsequently hashed.

Data Handling -> Verification

Security Hardware 

Software checks will be designed, providing a verification through a Hardware Security Module ( HSM ) desgined by industry leaders. Data-Payloads will be sent into the HSM and a Secure Hash Digest ( SHD ) will be provided to the consumer of the API. Data will than be transmitted in clear view of anyone observing. The only objective we're looking to maintain is that the data we recieve is correct and un-altered in any way. Insecure data, or altered data will be immediatly disposed of.

Onboard C&DH will also run simular tests for command validation and uplink transmission, using isolated hardware processer & memory. Offloading responsibility from the primary Data Processing and Handling module. Security & Verification module will remain isolated, it is safer and more secure not to share hardware or software resources with other subsystems. Reducing the protential for actors to gan access to hardware secured secrets.

#### Command
#### Data Handling
#### Security & Verification
### Ground Station
## CubeSat Regulations & License Requirements
## Unencrypted Command & Integrity Verification
## Unencrypted Data Transmission & Integrity Verification