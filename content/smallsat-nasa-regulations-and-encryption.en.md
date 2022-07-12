+++
title = "CubeSat Regulations, Amature License, & Encryption"
template = "page.html"
date = 2020-07-06T15:00:00Z
# draft = false
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = "Overview of possible CDH implementations."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++


## Introduction

In my research on SmallSat deployment using CubeSat Platforms, I've started to find myself gravitaing towards the Command and Data Handling subsystem design. What peaked my interest was a thought experiment around implemening secure command reception and actknowledgement for satellite communication during unencypted transmission.

This post is not a mission plan, instead it is posted for two reasons. First, to help those behind me piece together how to develop an understanding of satellite design. If you find yourself a university student or someone interested in launching a space vehicle into space. I hope you find this content helpful. Secondly, its to assist with collecting feedback from those more involved and more active in the space industry, creating a fourm for feedback so I might have an oppertunity to correct my misunderstandings as I work out how everything works together. The format of this post is meant to (eventually) resemble a mission plan.

This post is parsed into sections,
* Mission Objective & Overview
* Space Vehicle
* Ground Station
* CubeSat Regulations & License Requirements
* Security & Verification
* Unencrypted Command Verification
* Unencrypted Data Transmission Verification

## Mission Objective & Overview

The objective our mission is to collect data about cloud coverage and other environmental factors over Japan. Specifically, we're interested in creating a map of Cloud Coverage over Japan which will provide us with information on how climate change is effecting Japan's typhoon season.

As typhoon season approaches, we'll want to extend our observations from mainland-Japan into the sorrounding seas. CubeSat 3U will orbit Earth in [Low Earth Orbit](https://en.wikipedia.org/wiki/Low_Earth_orbit), providing us with the ability to image the same region(s) of Earth up to twelve times in a single day. Six times with sunlight and six times without sunlight.

### Earth Observation

The science data we are expecetding to extract from our images include depth of cloud calculation based on how much light is reflected from clouds. We're also interested in knowing how much percipitation is being dropped in a region at any given point in time. Lastly we want to come up with a percentage figure of how much cloud is in a given image, providing us with the ability to approximate how much cloud coverage Japan recieves on any given day.

### Data Processing

Data onboard CubeSat 3U will be store in a compressed format. Images will be taken and compressed in a data-bank aproximently 128GB in size. Data Handling algorthims will check the integrity of the data while the satellite is outside of the imaging bounding box. After files have been verified and a downlink is establised, data will be sent to a ground station, verified transmission as a success, and the image data is deleted from the onboard storage device.

### Orbital Plan

CubeSat 3U will be launched into Low Earth Orbit ( LEO ). It just so happens the satellite ground track passes over our ground station just right. We'll recieve a strong signal from our hardware, providing a downlink of 2MB/sec and uplink of 500KB/sec. The full orbit will be about 100 minutes, providing our ground station with 15 minutes of continuous communication to send commands and recieve telemetry. CubeSat will fly at about 600 meters above Earth's surface. To correct the Orbit, reaction wheels will activate on three axis to reduce angular momentum and stablize optical sensors and point the sensors towards Earth.

### Space Vehicle

When communicating with a smallsat, multiple factors have to be taken into consideration for successful operation. Lets focus and create some assumptions about how communication is established between a ground station and an orbiting CubeSat 3U. You've setup a ground station on the top of your roof. The smallsat also has enough power to provide continues communication and perform mission critical operations at the same time.

The platform we'll use for smallsat is CubeSat 3U. CubeSat 3U bus has strict hardware/payload considerations. 2/3U goes to Optical Imaging, 1/3U goes to Data Processing and Command Control.

#### Software Operating System

In order to save resources and time, we'll use a Linux Kernel to manage and develop new software. There are [resources](https://github.com/fishinabarrel/linux-kernel-module-rust) today, available for implementing new kernel modules using [Rust](https://www.rustlang.com/).

#### Guidance Navigation & Control ( GN&C )

Guidance will include numerious varibles in the code written. Taking in sensor data from various sensors, Control will provide numerical values for calculations in the GN subsystem.

#### Attitude Determination & Control ( AD&C )

In order for CubeSat 3U to take images of Earth while passing over Japan, we'll need to stablize the optical camera in a single direction for long periods of time. In order to do this, we'll also need to know which direction Earth is, which section of the Earth we're pointing at. Tagging the data appriatly while we're doing this. It'll require design of a custom tagging database along with figuring out when images are taken and at which time. We'll than corrate the images with the GN&C subsystem to determine which section of the sky was imaged at that percise moment in time.

#### Command, Data Handling, Security & Verification ( CDHSV )

The remaining 1 and 1/3U of the CubeSat 3U will be reserved for onboard Processing for Command, Data Handling, and Security & Verification hardware. Command accepts uplink commands sent from an authenticated ground station. Data Handling prepares data for download to a ground station. Security & Verification provides a security framework onboard the satellite to make sure agents and actors are properly authenticated and authorized.

##### Command

Command Software Module ( CSM ) controls the actions of CubeSat 3U. Having direct interaction between all functioning components within the vehicle. Capable of receiving uplink commands from a ground station. When a command is recieved, it is first verified to make sure the command came from an authorized ground station. When accepted, CSM then proceeds to decide what kind of command was sent.

* Security & Verification
* Attitude & Articulation Determination and Control SubSystem ( ADCS )
    * Orbit adjustment command
    * EO Tracking adjustemnt Command
* Data Handling
    * Instrument Data Processor Unit
    * Uplink & Downlink SubSystem
    * Telemetry SubSystem

##### Security & Verification SubSystem ( SVS )

All commands sent, are routed through the Security & Verification Hardware Module for command verification and ground station authorization. Ensuring only authorized commands can alter the state of the space vehicle.

Software checks will be designed, providing a verification through a Hardware Security Module ( HSM ) desgined by industry leaders. Data-Payloads will be sent into the HSM and a Secure Hash Digest ( SHD ) will be provided to the consumer of the API. Data will than be transmitted in clear view of anyone observing. The only objective we're looking to maintain is that the data we recieve is correct and un-altered in any way. Insecure data, or altered data will be immediatly disposed of.

Onboard C&DH will also run simular tests for command validation and uplink transmission, using isolated hardware processer & memory. Offloading responsibility from the primary Data Processing and Handling module. Security & Verification module will remain isolated, it is safer and more secure not to share hardware or software resources with other subsystems. Reducing the protential for actors to gan access to hardware secured secrets.

##### Attitude & Articulation Determination and Control SubSystem ( AADCS )

Comand provides the interface to alter the dynamics of the space vehicle. Capable of changing the orbit and orienting the satellite towards a specific Earth coordinate. Command Flight Control provides the capability to change the mission design while in flights as well.

The controls for CubeSat 3U are divided into algorithms which produce outputs for select actuator input. 

Maneuvers:
* Momentum Dumping - Usage of magnetorquer to reduce reaction wheel saturation
* Orbit Raising Maneuver - Increases altitude using reaction wheels
* Orbit Lowering - Reduces altitude using reaction wheels
* De-Spin - Use of magnetorquer and reaction wheel to cease spin
* Deceleration - performed periodically by increasing friction with magnetorquer

##### Data Handling

Due to our ground station being within the observation zone of CubeSat 3U, we'll have to automate the process of preparing the data to be transmitted while Earth Observation is underway. The process of doing this includes generating and assigning a signature and subsequent hash using cryptographic algorthims. This allows for the system to send a data-payload in a complete form. All data will be transmitted over radio waves, we'll have to develop a protocol which is fast enough to run on microprocessors and is capable of retransmiting information from platform to groundstation.

An Instrument Data Processing Unit ( IDPU ) will prepare data for transmission. Taking complete photograghs stored in compressed format. Chunking the data into 100KB in size and signing each chunk with a verification signature for the reciever to verify the integrety of data. Images captured for Earth Observation will remain in storage until transmitted. In order to track image transmission, we'll have an onboard database tracking photograph metadata. Including metrics on transmission and failures, success, and deletion of data onboard. We'll also design a subsystem within the IDPU which track diagnostic metrics for each teletmerty gathering instrument.

## Ground Station

CubeSat 3U Ground Station will be able to track CubeSat 3U as it enters radio apature of CubeSat 3U Ground Station range. CubeSat 3U is equiped with a powerful-enough high-gain antenna which allows for high-powerd downlink capability. For this simulation, we'll assume the Ground Station is equiped also with both a Tracking Antenna and Parbolic Antenna which can be pointed at our space craft. The Hyperbolic Tracking Antenna will locate and triangulate the location of CubeSat 3U when it comes into range, and transmit coordinates to the Parbolic Antenna to point and recieve a stronger signal.

The signal between CubeSat 3U and CubeSat 3U Ground Station will be strong enough to send a consistent 2MB per second, allowing downlink transmission rate of of 1,800MB ( 1.8GB ) over fifteen minutes while CubeSat 3U is in range. During that communication, an Uplink will also be established, but restructed to 100KB per second, recieved by a secondary antenna on CubeSat 3U. The Uplink will transmit Commands and Acknowledgment of downlink payload.

## CubeSat Security
Amature CubeSats are required to broadcast payloads in a plain transmission. Encrypting data is strictly prohibited by NASA and FCC regulations. Due this this constraint, we'll design a Security & Verification Module, designed to pervent a Vehical Takeover Event. CubeSat3 will be able to recieve commands and have the ability to identify which commands are sent by our ground station vs a malicious actor trying a take over.

There isn't much we can do about radio jaming. If an actor decides to flood CubeSat 3U with radio waves, we'll have to wait until the attack is suspended. In the event of that happening, CubeSat 3U will be able to notify CubeSat 3U Ground Station that the onboard hardware is processing incomming radio, but unable to parse or find a command to run onboard. In order to prevent radio hardware damage, if the hardware begins to overheat, the hardware will be shut off for a random amount of time based off a seed specified before launch. This will provide CubeSat 3U Ground Station with the ability to predict the random event and establish communication at a later time.

If such hostile events are to happen; events will be reported to the approiate authorities for further investigation.

### Policies and Licensing

FCC requires all amature satellites with a transmitter to be licensed. For the sake of this simulation, we'll assume that all licensing is complete. [ARRL](http://arrl.org/) provides a PDF of [Amateur FCC Part 97](http://www.arrl.org/files/file/Regulatory/March%208,%202018.pdf). Refer to [ecfr.gov](https://ecfr.gov/) for [Experimental FCC Part 5](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-5). NOAA must also be contact in the event any remote sensing is taking place within the space vehicle. NOAA might have licensing specific to the "type of sensor activity" being done.

Special thanks to the creaters of [State of the Art of Small Spacecraft Technology](https://www.nasa.gov/smallsat-institute/sst-soa/communications#9.5.5) for providing this information. In order to operate a Ground Station, someone at the facility needs to be an Amateur Radio Licensed Operator.

### Encryption

Encryption for command codes is required by NASA Regulation. This is where the Security & Verification module comes into use. In order to prevent CubeSat 3U from being taken over by a maliciosu actor, we'll encrypt all command communication to and from CubeSat 3U.

## Security & Verification

In this module, we'll design Security & Verfication hardware and software

## Encrypted Command Verification

In this module, we'll show to to use the Security & Verification hardware and software to sign and verify commands sent from a ground station to CubeSat 3U

## Unencrypted Data Transmission Verification

In this module, we'll show to to use the Security & Verification hardware and software to sign and transmitte data from the Space Craft to Ground Station