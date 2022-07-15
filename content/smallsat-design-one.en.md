+++
title = "SmallSat Design - One"
template = "page.html"
# date = 2020-07-06T15:00:00Z - Started
date = 2020-07-15T11:00:00Z
# draft = false
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = "In my research on SmallSat deployment using CubeSat Platforms, I've started to find myself gravitaing towards the Command and Data Handling subsystem design. What peaked my interest was a thought experiment around implemening secure command reception and actknowledgement for satellite communication during unencypted transmission."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++


## Introduction

In my research on SmallSat design and CubeSat Platforms, I've started to find myself gravitaing towards Command and Data Handling SubSystems. What peaked my interest was a thought experiment around implemening secure command reception and acknowledgement for satellite communication during unencypted transmission.

This post is not a mission plan, instead it was posted for two reasons. First, to help those behind me piece together how to develop an understanding of satellite design. If you find yourself a university student or someone interested in launching a satellite into space. I hope you find this content helpful. Secondly, its to assist with collecting feedback from those more involved and more active in the space industry, creating a fourm for feedback so I might have an oppertunity to correct my misunderstandings as I work out how everything works together. The format of this post is meant to (eventually) resemble a mission plan.

This post is parsed into the following sections,
* Mission Objective & Overview
* Satellite
* Ground Station
* SmallSat Security
* Policies and Licensing
* Database and Instrument Processing Unit
* Security & Verification Module

## Mission Objective & Overview

The objective our mission is to collect data about cloud coverage and other environmental factors over Japan. Specifically, we're interested in creating a map of Cloud Coverage over Japan which will provide us with information on how climate change is effecting Japan's typhoon season.

As typhoon season approaches, we'll want to extend our observations from mainland-Japan into the sorrounding seas. CubeSat 3U will orbit Earth in [Low Earth Orbit](https://en.wikipedia.org/wiki/Low_Earth_orbit), providing us with the ability to image the same region(s) of Earth up to twelve times in a single day. Six times with sunlight and six times without sunlight.

### Earth Observation

The science data we are expecetding to extract from our images include depth of cloud calculation based on how much light is reflected from clouds. We're also interested in knowing how much percipitation is being dropped in a region at any given point in time. Lastly we want to come up with a percentage figure of how cloud coverage is in a given image, providing us with the ability to approximate how much cloud coverage Japan recieves on any given day.

### Orbital Plan

CubeSat 3U will be launched into Low Earth Orbit ( LEO ). It just so happens the satellite ground track passes over our ground station just right. We'll recieve a strong signal from our hardware, providing a downlink of 2MB/sec and uplink of 500KB/sec. The full orbit will be about 100 minutes, providing our ground station with 15 minutes of continuous communication to send commands and recieve telemetry. CubeSat 3U will fly at about 600 meters above Earth's surface. To correct orbital line, reaction wheels will activate on three axis to reduce angular momentum, stablize optical sensors when observing, and point the sensors towards Earth.

## Satellite

When communicating with CubeSat 3U, multiple factors have to be taken into consideration for successful operation. Lets focus and create some assumptions about how communication is established between CubeSat 3U Ground Station and the orbiting CubeSat 3U satellite. We've setup a ground station on the top of our roof. CubeSat 3U has enough power to provide continues communication and perform mission critical operations at the same time.

The platform we'll use for smallsat is CubeSat 3U. CubeSat 3U bus has strict hardware/payload considerations.

### Software Operating System

In order to save resources and time, we'll use a minimal Linux Kernel to manage and develop new software. There are [resources](https://github.com/fishinabarrel/linux-kernel-module-rust) today, available for implementing new kernel modules using [Rust](https://www.rustlang.com/).

### Guidance Navigation & Control ( GN&C )

Guidance will include numerious varibles in the code written. Taking in sensor data from various sensors, Control will provide numerical values for calculations in the GN subsystem.

### Command SubSystem ( CS )

Command accepts uplink commands sent from an authenticated ground station. Data Handling prepares data for download to a ground station. Security & Verification provides a security framework onboard the satellite to make sure agents and actors are properly authenticated and authorized.

CS controls the actions of CubeSat 3U. Having direct interaction between all functioning components within the vehicle. Capable of receiving uplink commands from a ground station. When a command is recieved, it is first verified to make sure the command came from an authorized ground station. When accepted, CSM then proceeds to decide what kind of command was sent.

* Security & Verification
* Attitude & Articulation Determination and Control SubSystem ( ADCS )
    * Orbit adjustment command
    * EO Tracking adjustemnt Command
* Data Handling
    * Instrument Data Processor Unit
    * Instrument Modulation
    * Inflight Firmware Updates
* Communication
    * Uplink & Downlink SubSystem
    * Telemetry SubSystem

### Attitude & Articulation Determination and Control SubSystem ( AADCS )

In order for CubeSat 3U to take images of Earth while passing over Japan, we'll need to stablize the optical camera in a single direction for long periods of time. In order to do this, we'll also need to know which direction Earth is, which section of the Earth we're pointing at. Tagging the data appriatly while we're doing this. It'll require design of a custom tagging database along with figuring out when images are taken and at which time. We'll then corrate the images with the GN&C subsystem to determine which section of the sky was imaged at that percise moment in time.

Comand Subsystem provides the interface to alter the dynamics of the space vehicle. Capable of changing the orbit and orienting the satellite towards a specific Earth coordinate. It is up to AADCS to carry out those alterations to the flight path of CubeSate 3U.

The controls for AADCS are divided into algorithms which produce outputs for select actuator input. 

Maneuvers:
* Momentum Dumping - Usage of magnetorquer to reduce reaction wheel saturation
* Orbit Raising Maneuver - Increases altitude using reaction wheels
* Orbit Lowering - Reduces altitude using reaction wheels
* De-Spin - Use of magnetorquer and reaction wheel to cease spin
* Deceleration - performed periodically by increasing friction with magnetorquer

### Security & Verification SubSystem ( SVS )

All commands sent, are routed through the Security & Verification Hardware Module for command verification and ground station authorization. Ensuring only authorized ground stations can alter the dynamics of the space vehicle.

Software checks will be designed, providing a verification through a Hardware Security Module ( HSM ). Data-Payloads will be sent to the HSM and a Secure Hash Digest ( SHD ) will be provided to the consumer of the API. Data will than be transmitted in clear view of anyone observing. The only concern while transmitting telemetry, we're looking to mitigate is making sure data we recieve is correct and un-altered. Insecure data, or altered data will be immediatly disposed of.

CS will also run simular tests for command verification from uplink transmission, using isolated hardware processer & memory. Offloading responsibility from the primary Data Processing and Handling module. Security & Verification Module will remain isolated, it is safer and more secure not to share hardware or software resources with other subsystems. Reducing the protential for actors to gan access to hardware secured secrets.

### Data Handling SubSystem ( DHS )

Due to our ground station being within the observation zone of CubeSat 3U, we'll have to automate the process of preparing the data to be transmitted while Earth Observation is underway. The process of doing this includes generating and assigning a signature and subsequent hash using cryptographic algorthims. This allows for the system to send a data-payload in a complete form. All data will be transmitted over radio waves, we'll have to develop a protocol which is fast enough to run on microprocessors and is capable of retransmiting information from platform to ground station.

An Instrument Data Processing Unit ( IDPU ) will prepare data for transmission. Taking complete photograghs stored in compressed format. Chunking the data and signing each chunk with a verification signature for the reciever to verify the integrety of data. Images captured for Earth Observation will remain in storage until transmitted. In order to track image transmission, we'll have an onboard database tracking photograph metadata. Including metrics on transmission and failures, success, and deletion of data onboard. We'll also design a subsystem within the IDPU which track diagnostic metrics for each teletmerty gathering instrument.

## Ground Station

CubeSat 3U Ground Station will be able to track CubeSat 3U as it enters radio apature of CubeSat 3U Ground Station range. CubeSat 3U is equiped with a powerful-enough high-gain antenna which allows for high-powered downlink capability. For this simulation, we'll assume the Ground Station is equiped also with both a Tracking Antenna and Parbolic Antenna which can be pointed at CubeSat 3U. The Hyperbolic Tracking Antenna will locate and triangulate the location of CubeSat 3U when it comes into range, transmit coordinates to the Parbolic Antenna to point and establish a stronger uplink/downlink signal.

The signal between CubeSat 3U and CubeSat 3U Ground Station will be strong enough to send a consistent 2MB per second, allowing downlink transmission rate of of 1,800MB ( 1.8GB ) over fifteen minutes while CubeSat 3U is in range. During that communication, an Uplink will also be established, but restructed to 100KB per second, recieved by a secondary antenna on CubeSat 3U. The Uplink will transmit Commands and Acknowledgment of downlink payload.

## SmallSat Security

Amature SmallSats are required to broadcast payloads in a plain transmission. Encrypting data is strictly prohibited by NASA and FCC regulations. Due this this constraint, we'll design a Security & Verification Module, to pervent a SpaceCraft Takeover Event. CubeSat 3U will be able to recieve commands and have the ability to identify which commands are sent by an authorized Ground Station.

There isn't much we can do about radio jamming. If an actor decides to flood CubeSat 3U with radio waves, we'll have to wait until the attack is suspended. In the event of that happening, CubeSat 3U will be able to notify CubeSat 3U Ground Station that the onboard hardware is processing incomming radio, but unable to parse or find a command to run onboard. In order to prevent radio hardware damage, if the hardware begins to overheat, the hardware will be shut off for a random amount of time based on a random-seed specified and secured before launch. This will provide CubeSat 3U Ground Station with the ability to predict the random event and subsequently know when to establish communication at a later time.

## Policies and Licensing

For an Ameture License, FCC requires all transmissions must be in plain text. Transmission of data cannot be encrytped in any way, all transmissions must be sent in plain form, meaning nothing is kept secret. NASA requires all satellites with propulsive capabilities encrypt transmissions to and from ground stations. We'll have to apply for an Experimental License because CubeSat 3U has actuators; we're preforming Earth Observation; we don't classify as Commercial or as a Government unit.

FCC requires all satellites with a transmitter to be licensed. For the sake of this simulation, we'll assume that all licensing is complete/approved. [ARRL](http://arrl.org/) provides a PDF of [Amateur FCC Part 97](http://www.arrl.org/files/file/Regulatory/March%208,%202018.pdf). Refer to [ecfr.gov](https://ecfr.gov/) for [Experimental FCC Part 5](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-5). NOAA must also be contacted in the event any remote sensing is taking place within the space vehicle. NOAA might have licensing specific to the "type of sensor activity" being done.

Special thanks to the creaters of [State of the Art of Small Spacecraft Technology](https://www.nasa.gov/smallsat-institute/sst-soa/communications#9.5.5) for providing this information. In order to operate a Ground Station, someone at the facility needs to be an Amateur Radio Licensed Operator. There is also [CubeSat 101](https://www.nasa.gov/sites/default/files/atoms/files/nasa_csli_cubesat_101_508.pdf), providing a fantastic guide on how to plan your first CubeSat build.

### Encryption

We want to maximize the data download link, and we don't really care much about protecitng the data while in transmission. However, we must maintain strict encryption for both command messages and data verification processing. Meaning, we'll need to install a Hardware Security Module ( HSM ) which will manage secure communication between the space vehicle and ground station.

## Database and Instrument Processing Unit

The Database and Instrument Processing Unit ( DIPU ) will be made up of multiple subsystems. The Database subsystem will use [rocksDB](http://rocksdb.org/) at the core since it can be stored on flash storage and is optimized for performance using modern OTC SSD technology. We'll enhance and provide an API using [Rust](https://docs.rs/rocksdb/latest/rocksdb/). The new API will be simular in design to most other [document databases](https://en.wikipedia.org/wiki/Document-oriented_database). A key-value pair will be passed as a string-object. [Rust Structs](https://doc.rust-lang.org/rust-by-example/custom_types/structs.html) will be able to inherit traits and perform operations on the embedded database.

For stabliziation and flight, we'll also need to collect metrics for all subsystems and store them. Each database record will have a prefix relative to which subsystem the data is being stored for. That way, we'll be able to iterate over all subsystems and transmite telemetry data with ease.

### Earth Observation

The optical camera used to take photos of Earth has device storage upwards of 128gb, which is more than enough for 4 minutes of image capture. We'll leave the photos taken as is, on that device and use DIPU to track, tag, and transmit a compressed data stream over the downlink without using any additional long-term storage device. Once the DIPU determines a photo has been recieved in full by CubeSat 3U Ground Station, it will be removed from device storage. Data backups will be managed on Earth.

### Instruments
Collect operational statistics for Actuators, Sensors, RF Communication, Command, and Security Verification Module

## Security & Verification Module

Per NASA Regulations, and space vehicle with propuslive ability must encrypt all sensative communication. We're also interested in keeping CubeSat 3U safe from take over or accident. 

Security & Verification Module (SVM) will be a 10cm x 10cm x 3cm ( 0.3U ) board equiped with a state of the art Integrated Security Circuit (ISC) providing authentication and authorization requests via I2C data channel. The SVM will a operate a minimul operating system with the ability to listen for and respond to requests for autherization and authentication. The ISC will retain all memory, entropy-generation, and processing within the ISC. ISC will also provide secure methods of swaping out access keys while remaining resistant to physical and virtual tampering.

### Command

We'll use a network capable tool to communicate with SVM. Data transmissions will be heard and decoded using a pre-assigned signature which is unique to both CubeSat 3U and CubeSat 3U Ground Station. All other transmissions will be ignored. Once the data-packets been reiceved and understood, the next stop on the trip through the Command Subsystem is to verifiy that the command is from CubeSat 3U Groud Station. If the command is verified, it is then registered in the log as valid and immediatly acted upon.

### Data Verification

Ensuring data collected is communicated in full, every data-packet will be signed with a unique, reproducable signature using an SVM-available cryptographic hash function. The hash, along with the data-packet will be transmitted and it is then up to CubeSate 3U Ground Station to verify the contents have in fact transmitted and are not tampered with. Once verified, a command will be sent back to CubeSat 3U indicating that the data-packet has been recieved and the DIPU will erase meta-data and photos, freeing up space to store more data.