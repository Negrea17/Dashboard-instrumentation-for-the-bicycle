# Dashboard-instrumentation-for-the-bicycle
This project is an instrumentation system for bicycles designed to measure and display key ride metrics such as speed, distance, RPM, and recommended gear ratios. It also features a low-light warning system to remind you to turn on your lights when necessary.

Features
Speed Measurement: Calculates and displays the current speed using data from a Hall sensor.
Distance Tracking: Keeps a running total of the distance traveled by the bicycle.
RPM Calculation: Computes the rotations per minute (RPM) of the wheel.
Gear Recommendation: Suggests a recommended gear ratio based on the current speed.
Low-Light Alert: Uses a light sensor and buzzer to alert you when ambient light is below a defined threshold.
Mode Switching: Allows you to switch between two display modes:
Mode 1: Displays speed and total distance.
Mode 2: Displays gear recommendation and RPM.
Reset Function: Provides a reset button to clear the distance and speed calculations.
Hardware Requirements
Microcontroller: An Arduino-compatible board (the code uses pins such as PA0, PA1, etc., which may correspond to specific microcontroller ports like those on an STM32 board).
LCD Display: A 16x2 LCD display connected via the LiquidCrystal library.
Hall Sensor: For detecting wheel rotations.
Light Sensor: For monitoring ambient light levels.
Buzzer: To provide audible alerts for low-light warnings and button interactions.
Push Buttons: Two buttons:
One for resetting the measurements.
One for switching between display modes.
Wiring and Breadboard: For connecting all components.
Software Setup
Install the Arduino IDE:
Download and install the latest version of the Arduino IDE.

Add Required Libraries:
Ensure the LiquidCrystal library is installed. This library is typically included with the Arduino IDE by default.

Configure the Board:
Set up your board in the Arduino IDE, making sure the selected board supports the pin configuration used in the code (e.g., PA0, PA1, etc.). You may need to modify the pin assignments if you are using a different board.

Upload the Code:
Copy the provided code into a new sketch in the Arduino IDE and upload it to your board.

Wiring Diagram
While no official wiring diagram is provided, the following pin assignments are used in the code:

LCD Display:

RS: PA0
Enable: PA1
D4: PA2
D5: PA3
D6: PA4
D7: PA5
Sensors and Actuators:

Hall Sensor: PA7
Light Sensor: PA15
Buzzer: PA11
Reset Button: PA8 (configured with INPUT_PULLUP)
Mode Change Button: PA6 (configured with INPUT_PULLUP)
Ensure that all components are connected according to these assignments. Adjust the wiring if using a different microcontroller.

Code Overview
Interrupt Service Routine (hallISR):
Captures the time interval between wheel rotations using a Hall sensor, updating both the pulse interval and total distance.

Main Loop (loop):
Continuously checks for button presses, manages mode switching, triggers light level alerts, and updates the LCD display at regular intervals (every 3 seconds).

Speed Calculation (calculateSpeed):
Converts the pulse interval from the Hall sensor into speed in km/h.

RPM Calculation (calculateRPM):
Computes the wheel's rotations per minute.

Gear Recommendation (determineGear):
Provides a suggested gear ratio based on the current speed.

User Feedback Functions (shortBuzz & soundBuzzer):
Handle audible feedback for button presses and low-light warnings.

Buffer Functions:
Maintain a rolling average of recent speed measurements for a smoother display.

Usage Instructions
Power Up:
Once the hardware is set up and the code is uploaded, power on your microcontroller. The LCD should display the initial speed ("Viteza: 0 km/h").

Riding:
As you ride, the system will calculate your current speed and update the total distance traveled. It automatically updates every 3 seconds.

Switching Modes:
Press the mode button to toggle between:

Mode 1: Displays current speed and distance.
Mode 2: Displays the recommended gear ratio and RPM.
Resetting:
Press the reset button to clear the current distance and reset speed measurements. A short beep will confirm the reset.

Low-Light Alert:
If the ambient light falls below the threshold, the LCD will prompt you to "Turn on the lights!" and the buzzer will sound an alert.

Future Improvements
Data Logging:
Integrate an SD card module to log ride data for post-ride analysis.

Bluetooth Connectivity:
Add Bluetooth support for real-time data transfer to a smartphone app.

Enhanced Display:
Upgrade to a larger or graphical LCD to display more detailed information and graphs.

Power Management:
Incorporate battery monitoring and power-saving features.

License
This project is open-source. Feel free to modify and distribute as needed. Contributions and suggestions are welcome!

Acknowledgements
This project uses the LiquidCrystal library for LCD interfacing.
Special thanks to the open-source community for their continued support and contributions to projects like this.
