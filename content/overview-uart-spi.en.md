+++
title = "An overview of UART and SPI"
template = "page.html"
date = 2020-08-02T11:00:00Z
#date = 2020-07-29T11:00:00Z
draft = false
[taxonomies]
categories = ["data interface", "uart", "spi"]
[extra]
summary = "As a software engineer learning hardware development, I found myself first gravitating towards understanding how information is transmitted between devices. This article is part of an ongoing series meant to teach myself satellite design and eventurally develop functioning prototypes which can be launched into space. From the group up, I'll explore what is required to transition from software development into hardward development, learning from the internet as questions come to mind."
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

## Introduction
As a software engineer learning hardware development, I found myself first gravitating towards understanding how information is transmitted between devices. This article is part of an ongoing series meant to teach myself satellite design and eventurally develop functioning prototypes which can be launched into space. From the group up, I'll explore what is required to transition from software development into hardward development, learning from the internet as questions come to mind.

## UART

UART stands for Universal Asynchronous Receiver Transmitter. There are TX and RX ports on chips indicating information can be sent and recieved. When connecting two chips together, its important to understand which way data is being transfered. In example, when flashing a microprocessor. Connecting a FT232RL chip TX to a Cortex M0+ microprocessor allows for data serialization from USB -> MicroProcessor. Due to the transmission being async, its important to note that the baud-rate must be set and transmitted prior to data transmission.

![uart0-uart1-connection-block-diagram.png](/images/overview-data-interfaces/uart0-uart1-connection-block-diagram.png)

Data transmission takes on the form of an envolop, a start bit indicates a binary payload is about to be transmitted, the following 5->9 bits are data, followed by a parity bit, and 1->2 ending bits.

### Data Transmission Envolope

**Start Bit** is normally held in "high" position while idle. When the connected recieving device detects the Start Bit flipping from high -> low, it'll start reading bytes being sent.

**Data Bits** are transmitted with the Least Significant bit first, followed by up-to 8 or 9 bits.

**Parity Bit** adds the ability to validate data being sent. When Parity Bit is set to "high", the chip is supposed to check the bits sent and make sure that all "high" bits in Data Bits are odd. While, if the Parity Bit is set to "low", the chip should validate that all "high" Data Bits are even.

**Ending Bits** returns the voltage to "high", using either one or two clock cycles. Recieving chip will understand that another transmission packet might be coming, but it won't read the data until a **Start Bit** is sent with a "low".

![data-transmission-envolope.png](/images/overview-data-interfaces/data-transmission-envolope.png)

If you're interested in a more in-depth overview of UART, but with some dated language. [More details can be found here.](https://www.analog.com/en/analog-dialogue/articles/uart-a-hardware-communication-protocol.html)

## SPI

Serial Peripheral Interface(SPI) is capable of synchronously transmitting and recieving 4.5MB/s. The protocol creates a data-loop between controller and peripheral's involved in communication between the two chips. Allowing for fast, syncroinous transmission of communication between the two chips. SPI requires a minimun of three pins to communicate.

SCK controls when data is meant to be read. It provides a change from high to low or low to high, of which each change in voltage signifies a bit should be read by SDI of the peripheral device. The output of the signal comes from SDO of the controlling device.

* SCK for Serial ClocK
* SDO/COPI/MOSI for Serial Data Output
* SDI/CIPO/MISO for Serial Data Input

![sck-sdo-sdi-interaction.png](/images/overview-data-interfaces/spi-data-transmission-block-diagram.png)

Transmission between controller and a single peripheral device connects the Controllor:SDO -> Peripheral:SDI and the Peripheral:SDO -> Controllor: SDI. Which allows for syncronious communication between the two devices. The user can access the data-transmission interface using SSPBUF, by adding data to and reading data from the buffer along the information connection. When a complete set of data bits are transmitted, the bits are transfered from SSPSR -> SSPBUF for user software to access.

![spi-data-transfer.png](/images/overview-data-interfaces/spi-data-transfer-block-diagram.png)

{% round_circuit_note(title="Depricated MISO, MOSI, SS") %}
Earlier in the millennium, a new resolution was raised for naming of MISO, MOSI, and SS to be depricated. Most, if not all terms using Master/Slave termonology should be recycled for more modern language. In the case of SPI, MOSI -> COPI, MISO -> CIPO.
{% end %}
* [https://www.oshwa.org/a-resolution-to-redefine-spi-signal-names/](https://www.oshwa.org/a-resolution-to-redefine-spi-signal-names/)