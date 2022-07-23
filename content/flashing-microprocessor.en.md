+++
title = "Building a Circuit around a Cortex M0+ microprocessor and programming it"
template = "page.html"
date = 2020-07-16T11:00:00Z
draft = false
[taxonomies]
categories = ["CubeSat", "smallsat"]
[extra]
summary = ""
mathjax = "tex-mml"
author = 'Joseph Curtin'
+++

## Introduction
Welcome to my website. I've decided to design and develop a 3U CubeSat from scratch. When starting this endeavor, I knew almost nothing about satellite design, development, testing, and deployment. My goal is to learn enough about developing and building a circuit while I teach myself orbital machanics. It'll take time for me to learn these concepts, and I'll post here as often as I can while I work to achieve my goal.

Ardunio & Raspberry PI have revolutionalized the way makers produce and develop tools to control anything. I've always been curious about how to build a board like Ardunio from scratch, in this post I'll develop a microcontroller development board for the Cortex M0+ microprocessor with simular capabilities as Ardunio & Raspberry PI, but not nearly as strong. This iteration is based on the youtube video by [Gary Explains](https://www.youtube.com/c/GaryExplains), "How to [build your own ardunio like board](https://www.youtube.com/watch?v=4PMj8LfR2m8)".

For the new design, here is the product list of items you'll have order or have in your workshop.

* [32-bit ARM ® Cortex ®-M0+ microcontroller](https://www.mouser.com/ProductDetail/NXP-Semiconductors/LPC812M101JD20FP?qs=WQO6Kzcwo2HNstrFk%2FzTow%3D%3D&countryCode=US&currencyCode=USD)
* [SOP20, SSOP20, TSSOP20 to DIP Microcontroller adapter](https://www.amazon.com/KeeYees-Adapter-SOT223-TQFP100-2-54mm/dp/B085L8SK7Z/)
* [PCB Adapter for Microcontroller](https://www.amazon.co.jp/-/en/uxcell-Adapter-SSOP16-TSSOP16-0-65mm/dp/B00O9W6RLQ/)
* [Breadboard](https://www.amazon.co.jp/-/en/gp/product/B0838VV2X3/)
* [Breadboard Jumper Wires](https://www.amazon.co.jp/dp/B07CJYSL2T)
* [Resister Kit](https://www.amazon.co.jp/-/en/dp/B07RQ4J41V/)
* [LED Kit](https://www.amazon.co.jp/dp/B0739RYXVC)
* [Capacitor Kit](https://www.amazon.co.jp/-/en/gp/product/B07R12TBM5/)
* [LDO Voltage Regulator](https://www.mouser.com/ProductDetail/Microchip-Technology-Atmel/MCP1700-3302E-TO?qs=sGAEpiMZZMsGz1a6aV8DcBHlmKLodU9v0iw1k6QUB7Y%3D)
* [USB -> TTL Serial Converter Adapter Module](https://www.amazon.co.jp/dp/B00IJXZQ7C)
* [KKHMF Single Row Terminal Pin Header Strip](https://www.amazon.co.jp/-/en/2-54mm-40-Pin-Terminal-Compatible-Ardunio/dp/B0829W3T8Q/)


This post will be split up into sections
* Prototyping using a Breadboard
* Soldering a Cortex M0+ microprocessor
* Programming the microprocessor

* Designing an schematic for our development board
* Prototyping the integrated circuit using a Breadboard
* Programming the microprocessor on Breadboard
* Converting the schematic into a PCB using EasyEDA
* Building and soldering components to PCB
    * Mini USB
    * Jumper Pins
    * Voltage Regulator
    * Capacitors
    * FTDI-FT232RL
    * Cortex M0+
* Programming the microprocessor on the PCB

* Programming the microprocessor using Rust?

## Prototype using a Breadboard

We'll first test a circut with a FTDI USB Adapter, simular to how the circuit was designed in Gary Explain's [video](https://www.youtube.com/watch?v=4PMj8LfR2m8). Using a mulitmeter, make sure the current between the black wire and red wire on the left side is a constant 3.3v.

If you're like me, and you're learning this all from the start. I recommend you spend a lot of time thinking about how circuits are meant to be managed. A circuit is a closed loop of electricity, and the components inside that closed loop act upon the moving electrons in different ways. For example, a resistor will reduce the current of the flowing electrons by blocking the flow with non-conductive material. A capacitor will smooth out the flow of electrons, making the current more stable for the next component. 

A voltage regulator will smooth out the voltage, providing a consistent voltage to the circut. In our case, we're using a MCP1700-3302E/TO, which takes a varible input between 2.3v -> 6.0v and outputs 1.2v, 1.8v, 2.5v, 2.8v, 2.9v, 3.0v, 3.3v, or 5.0v relative to what is being passed into the voltage regulator. We can work this out with a formula provided by the MCP1700-3302E/TO datasheet. Using a desk, we could measure the outputs of the voltage regulator. Instead, we'll take advantage of the assumption that 5.0v should output 3.3v for the Cortex-M0+ microprocessor.

### Light Emiting Diode

The circuit here we're implementing is simple, it also brings a gread deal of knowledge to be learned to simply understand and achieve an implementation.

#### Understanding Ohm's Law
Fitting the correct resistor to a red LED was harder than I had expected. The concept was straight forward, what hung me up was the units I used to calculate the resistance. In my first attempt, I had assumed a circuit with input of 5.0-volts, 2.5watts, and 0.5-amperage, which are the units provided for USB 2.0 power supply. My calculations kept coming up with unexpected numbers. To correct my miss understandings, I sat down and built the circuit with a red LED and measured the voltage three times with three different values of resistance.

* 0Ω - 5 volts
* 300Ω - 2.1-volts
* 1200Ω - 1.85-volts

![red-LED-300ohms-resistance](/images/microprocessor-circuit/red-LED-910ohms-resistance.jpg)

By finding the above values, I was able to determine how my calculation for amperage running through the LED was incorrect. I was assuming 0.5A, or 500mA would run through an LED. Here is the correct series of calculations to step from 5.0V down to 1.8V. First, we need to find numbers which work for the red LED. From a datasheet, I pulled that 20mA is ideal for amperage running through a red LED at 1.8v. Which means we'll need to find the inverse-resistance of those values.

* $E = 1.85$
* $I = 0.0015 $

Using the equation $R = E \div{} I$, let's plug these figures in. $1233.333 = 1.85 \div{} .0015$. Much better, the values add up and corrospond to what a multimeter output.

{% round_circuit_note(title="I struggled a lot here.") %}
It took me some time to bend my mind around what exactly was happening. I kept writing the equation with 500mA as instead of 15mA. The unit 500mA comes from USB 2.0 power supply and it didn't occur to me I should look at a datasheet for the red LED to find the operating amperage. To solve this descriptency, created the circuit on a bread board using 0Ω, 300Ω, and 1200Ω. I measured the voltage running through the red LED each time and found that the outputs to be 5.0V, 2.0V, and 1.89V sequentially.
{% end %}

* https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all
* https://www.sparkfun.com/engineering_essentials
* https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-resistor-color-code


#### Applying Ohm's Law

The circut between Cortex M0+ and the LED is 3.3V if no resistors are added. We'll want to step that down from 3.3v to 1.89V. From our experiment above, we know that a resistor between 900Ω and 1300Ω should work. I've connected the same 1200Ω resistor and the voltage output is 1.84V.

![red-LED-test-circuit](/images/microprocessor-circuit/red-LED-test-circuit.jpg)

### Capacitors

Capacitors have three primary funcitons when designing a circut. **Power Supply Smoothing, Timing, and Filtering.** Using two capacitors between the FTDI-FT232RL board and Cortex M0+ chip, both will be performing Power Supply Smoothing. We connect the first 100nF capacitor in front of the Voltage Regulator and behind the VCC input wire. The second capacitor is placed after the Voltage Regulator 3.3V output pin, joining the positive and negative rails of the breadboard. Which completes the simple power supply to step voltage down from 5.0V to 3.3V.

Capacitors work by having two conducting materials close to enough to each other, transfering current from one side to the other. Most often from positive to negative. When enough charge is stored for discharge, the opposing conductive material will transfer electrical change as needed. This is how the power smoothing supports a continuous supply of DC current. Access current is stored in the postiive side of the capacitor, when the electricity drops down, the charge is discharged and smooths DC current.

* https://electronics.stackexchange.com/a/12544
* https://www.electronics-notes.com/articles/analogue_circuits/power-supply-electronics/capacitor-smoothing-circuits.php

{% round_circuit_note(title="The exact math to explain this,") %}
is something I'm still coming up to speed with. I also don't have an oscilloscope to measure the sin-wave of the electricity.. I'll leave expanding this topic anymore for a later blog-post.
{% end %}

### Voltage Regulator

Using a Voltage Regulator is fairly straight forward. If a chip or other device requires a constant voltage, and the current voltage is to high. Using a Voltage Regulator will step down the current from 5.0V to 3.3V in our case, making it possible to power the Cortex M0+ microprocessor and attached LED.

{% round_circuit_note(title="Understanding") %}
what the Voltage Regulator was doing took some time to cement into my mind. I understood that the current was being adjusted from 5.0V -> 3.3V, also smoothing out the current was happening too by capacitors, but I couldn't wrap my head around how that was happening until after I understood what the GND terminal was doing by measuring it with a multimeter.
{% end %}

* https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-use-voltage-regulators-in-a-circuit

## Soldering a Cortex M0+

Cortex M0+ uses an SSOP interface, which is really only compatable with PCB. We'll need to convert it to a DIP interface and solder it into place. Lay the pins laid out, place the PCB to bo solder to the Cortex M0+ on the pins and begin soldering the connections. Be sure not to connect different pins to each other, that might lead to shorts, or worse, unpredictable functionality when it comes to controlling external devices.

![breadboard prototype with soldered pins](/images/microprocessor-circuit/breadboard-prototype.jpg)

With the PCB adapter soldered to the pins. Its now time to place a Cortex M0+ microprocessor on the PCB. Make sure the slots aling, orienting the microprocessor with the PCB board. Without adding solder, heat the PCB board through the microprocessor pins and gently let the pins settle into the PCB.

![breadboard prototype with soldered Cortex M0+](/images/microprocessor-circuit/breadboard-prototype.jpg)

## Programming the Cortex M0+

In order to program the Cortex M0+ with a USB connector using the FTDI-FT232RL Adapter, we'll need to connect the TXD and RXD to the PO.0 and PO.4. To power the Cortex M0+ microprocessor, route VCC from FT232RL Adapter to the breadboard positive rail. In between, put a voltage regulater and two capacitors to futher smooth out current flow. The voltage regulator will step the current down from 5.0v to 3.3v and pip the access current into GND.

{% round_circuit_note(title="When putting these curcits together,") %}
I felt I was missing quite a bit of information around how the circuit was connecting. For instance, a voltage regulator and capacitor was provided between FTDI-FT232RL->VCC and Cortex M0+->VDD. What I learned is VCC is meant to indicate that power is being supplied while VDD indicates that power is meant to be recieved. VSS is meant to be connected to ground point.
{% end %}

With everything connected, its now time to download the software we'll use to program the Cortex M0+ microprocessor.

### MCUXpresso

Downloading and installing MCUXpresso was a task. The online forums asked for everything I could give them, from phone number to company affiliation. Including address and other personal details. Aside from the UX of the website not working well, it seems everything else is well constructed. Which is good, having that information redilly available in a database is kind of meh at this day in age.. but I've digressed. Until I find a better IDE solution(Rust), I'll follow the path and install MCUXpresso.... reluctantly.

* https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE

### LPC810 Codebase

The next step to start programing for the Cortex M0+ is to download some source code from github. [Download a zip file from this repository.](https://github.com/microbuilder/lpc810_codebase).

![LPC810_Codebase-zip-download](/images/microprocessor-circuit/LPC810_Codebase-zip-download.png)

With the source code downloaded, head over to MCUXpressor and import the project. On the bottom left, under "Create or import project", select "Import project(s) from file system".

![Import project(s) from file system](/images/microprocessor-circuit/MCUxpresso-import-projects-from-file-system.png)

With the import dialog open, navigate to the downloaded LPC810_CodeBase-master.zip file and click finish.

![Select LPC810_CodeBase-master.zip](/images/microprocessor-circuit/MCUxpresso-import-LPC810_Codebase.png)

With the project open, using the File Explorer on the left, expand `LPC810_CodeBase/src` and select `main.c`. Scroll down to line 47 and alter `LED_LOCATION` from `2` to `17`.

![main-c-file-led-location-to-po17](/images/microprocessor-circuit/MCUxpresso-main-c-file-led-location-to-po17.png)

Its time to alter `int main(void)`. Scroll to the bottom of the file, we're going to change line 120 and 124. First alteration change line 120 from `mrtDelay(500)` to `mrtDelay(2000)`. Which will delay execution of the program for two seconds. Next alter line 124 from `mrtDelay(500)` to `mrtDelay(250)`, which will delay the program by 250ms.

![main-c-mrtDelay-adjustments](/images/microprocessor-circuit/MCUxpresso-main-c-mrtDelay-adjustments.png)

Okay, lets build the project.

![MCUXpresso-build-project.png](/images/microprocessor-circuit/MCUXpresso-build-project.png)
![MCUXpresso-build-project.png](/images/microprocessor-circuit/MCUXpresso-project-building.png)

Great, in the File Explorer, expand `Release` and look for a file called `LPC810_CodeBase.hex`. Right click, select `Properties`. Find a button on the right which will open System File Explorer to the directory of the `LPC810_CodeBase.hex` file. We'll import the file into Flash Magic shortly.

![MCUXpresso-LPC810_CodeBase-Properties.png](/images/microprocessor-circuit/MCUXpresso-LPC810_CodeBase-Properties.png)
![MCUXpresso-LPC810_CodeBase-System-Explorer.png](/images/microprocessor-circuit/MCUXpresso-LPC810_CodeBase-System-Explorer.png)

### Flash Magic

Dowload and install Flash Magic. 

* https://www.flashmagictool.com/download.html

Time to load `LPC810_CodeBase.hex` into Flash Magic. 

## Designing a Cortex M0+ development board

Having a Cortex M0+ on the same PCB as the FTDL-FT232RL will require an understanding of the USB -> TTL Adapter board. Enough information is available in data sheets which allows us from having to disassemble the board.

### From USB Mini peripheral to FTDI-FT232RL IC

To complete this section of our circuit, we'll need to include a USB Mini Type-B Female peripheral and attach it directly to the FTDI-FT232RL IC.

* VCC connects to VCC and VCCIO
* D+ connected to USBDP
* D- connected to USBDM

Connect ID and GND to from USB Mini Type-B Female to a GND wire.

{% round_circuit_note(title="More about the USB 2.0 Protocol:") %}
Using a USB Mini Type B Female connector, I asked why does the connector have 5 pins instead of only four? Turns out the USB specification added the capacity for USB 2.0 to switch between sender/reciever of information. For chips capable of sending a signal back to the USB requesting the ability to send information, the "ID" pin is used.

<br\>
* [On-The-Go Protocol](https://electronics.stackexchange.com/a/35468)
* [Where is the Micro-A USB Plug?](https://electronics.stackexchange.com/a/242575)

{% end %}

### From FTDI-FT232RL to USB Cortext M0+

Connecting the FTDI-FT232RL to Cortex M0+ is fairly straight forward. Since power is being routed through another section of the circuit, the only connections to me made are the TX/RX pins.

* TXD connects to PO.0
* RXD connects to PO.4

## Designing an schematic for our development board

A core design decisions for this cirucit is to remove the need of having two or more PCB boards. We want to retain the ability to program a Cortex M0+ microprocessor while also exposing the PO-pins for external control of various devices. We'll do this by purchasing a FTDI-FT232RL chip and emebedding it directily on the same PCB as the Cortex M0+. To power the board, a USB mini connector will be used to provide 5v of power to the circuit.

![complete-circuit](/images/microprocessor-circuit/ftdl-cortext-schematic-whole.png)

### FTDI-FT232RL IC Schematic

When integrating the FT232RL chip, only transmission to Cortex M0+ is nessicary. Communication back into the USB can be ignored for the most part, which means we'll leave a majority of the UART0 pins unconnected. The PCB won't be capable of programming up over USB. We'll connect the RXD and TXD directily to Cortext M0+. !RXLED and !TXLED will be connected to LEDS, providing the ability to know if data is being transmitted to Cortex M0+. USBDP and USBDM are directly connected to Mini USB D+ and D- accordingly.

![FTDI-FT232RL-schematic](/images/microprocessor-circuit/FTDI-FT232RL-schematic.png)

### Cortex M0+ IC Schematic

Having as many PO pins available to connect pheripherials is important. VDD is a 3.3v input and requires power modulation between the USB VCC 5v power supply. With power connected, it is now possible to program and operate the Cortex M0+ microprocessor. To switch between those two modes, programming and operation, the design incorporates a pin-jumper which will connect PO.1(Pin-12) to GND when we're ready for the microprocessor to enter ISP mode. when in ISP mode, we can send a program over USB through the FTDI-FT232RL chip which will than be flashed onto the Cortex M0+ microprocessor. We can than test our program, by connected a PO-N pin, in our case we'll test with PO.17(Pin 1) by connected and blinking an LED.

![Cortex M0+ schematic](/images/microprocessor-circuit/CortexM0+-schematic.png)

### Power Supply

I'm fairly new to designing power-circuits, the circuit for power modulation took me some time to understand. I welcome any kind of feedback on this schematic. The Contex M0+ VDD(Pin-15) accepts 3.3v in. To step the current from 5v down to 3.3v, install a LDO voltage regulator. The MCP1700-3302E/TO(voltage regulator) output will be then feed into the Cortex M0+ VDD(Pin-15). For the ground circut of the MCP1700-3302E/TO, on the opposite side of VCC/Voltage Regulator input, attach a capacitor to transfer left over current to GND. Finally attach another wire from GND after the capacitor to the negative rail on the breadboard.

![Cortex M0+ schematic](/images/microprocessor-circuit/PowerModulation-schematic.png)

## Prototyping the integrated circuit using a Breadboard

Here is the breadboard prototype of the circuit we designed. Its important to prototype this as well, because there might be some slight differences between the prototype with the HeLetgo USB Adapter which aren't immediately apparent by only looking at the adapter.

![breadboard prototype schematic](/images/microprocessor-circuit/breadboard-prototype-schematic.jpg)

## Programming Cortex M0+ using USB Adapter



