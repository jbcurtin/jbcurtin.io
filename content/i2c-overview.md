+++
title = "An overview of data interfaces"
template = "page.html"
date = 2020-07-29T11:00:00Z
draft = true
[taxonomies]
categories = []
[extra]
summary = ""
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

# $I^2C$ Overview

https://github.com/ryanrightmer/lis3mdl

## $I^2C$

$I^2C$ provides the ability to scale the amount of controllers well beyond the physical peripheral limit. Communication occurs on SCK and SDA peripherals.

https://learn.sparkfun.com/tutorials/i2c/all

https://learn.sparkfun.com/tutorials/i2c/all


## RTS / CTS

RTS / CTS extends UART protocol and RTS recieves while CTS transmits.
https://www.lairdconnect.com/support/faqs/uart-flow-control-rtscts-necessary-proper-operation-wireless-modules

## CAN

* https://en.wikipedia.org/wiki/CAN_bus

IC2, UART, LVDS, SPI, PC, CAN


( Develope a breakout board for LIS3MDL )
* https://github.com/ryanrightmer/lis3mdl
* https://www.mouser.com/ProductDetail/STMicroelectronics/LIS2MDLTR?qs=5aG0NVq1C4wS0n6b5NiBNQ%3D%3D

( Include Example in Rust Code using STM32 )

* https://www.mouser.com/pdfdocs/tn15_spi_interface_specification.PDF
* https://cortex-m.com/spi/