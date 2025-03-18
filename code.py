#include <LiquidCrystal.h>

// LCD setup
LiquidCrystal lcd(PA0, PA1, PA2, PA3, PA4, PA5); // RS, Enable, D4, D5, D6, D7

// Pin configuration
#define HALL_SENSOR_PIN PA7    // Pin for Hall sensor
#define LIGHT_SENSOR_PIN PA15  // Pin for light sensor
#define BUZZER_PIN PA11        // Pin for buzzer
#define RST_BUTTON_PIN PA8     // Pin for reset button
#define MODE_BUTTON_PIN PA6    // Pin for mode change button

// Wheel circumference in meters
#define WHEEL_CIRCUMFERENCE 2.2
#define MEASUREMENT_INTERVAL 3000 // Measurement interval (3 seconds)
#define LOW_LIGHT_THRESHOLD 300   // Low light threshold (analog value)
#define BUZZER_PAUSE 180000       // Pause between alarms (3 minutes)

// Variables for speed
volatile unsigned long lastPulseTime = 0; // Time of the last magnet pass
volatile unsigned long pulseInterval = 0; // Interval between two pulses
float speedBuffer[5] = {0, 0, 0, 0, 0};     // Buffer for measured speeds
unsigned long lastMeasurementTime = 0;      // Time of the last measurement
int bufferIndex = 0;                        // Current index in the buffer

// Variables for distance traveled
volatile float totalDistance = 0.0; // Total distance traveled in km
unsigned long lastLightCheckTime = 0; // Last time the light was checked
int currentMode = 1; // Current mode: 1 = Speed and Distance, 2 = Gears and RPM

void hallISR() {
  unsigned long currentTime = micros(); // Read current time in microseconds
  pulseInterval = currentTime - lastPulseTime; // Calculate interval between pulses
  lastPulseTime = currentTime; // Update the time of the last pulse

  // Update distance traveled
  totalDistance += WHEEL_CIRCUMFERENCE / 1000.0; // Add distance in km
}

void setup() {
  // Initialize LCD
  lcd.begin(16, 2);
  lcd.print("Viteza: 0 km/h");

  // Configure pins
  pinMode(HALL_SENSOR_PIN, INPUT);        // Hall sensor
  pinMode(LIGHT_SENSOR_PIN, INPUT);         // Light sensor
  pinMode(BUZZER_PIN, OUTPUT);              // Buzzer
  pinMode(RST_BUTTON_PIN, INPUT_PULLUP);    // Reset button
  pinMode(MODE_BUTTON_PIN, INPUT_PULLUP);   // Mode change button

  // Set up interrupt for the Hall sensor
  attachInterrupt(digitalPinToInterrupt(HALL_SENSOR_PIN), hallISR, FALLING);

  // Serial for debugging (optional)
  Serial.begin(9600);
}

void loop() {
  unsigned long currentTime = millis();

  // Reset distance traveled and RPM when the button is pressed
  if (digitalRead(RST_BUTTON_PIN) == LOW) {
    totalDistance = 0.0;  // Reset distance
    pulseInterval = 0;    // Reset pulse interval
    lastPulseTime = 0;    // Reset time of last pass
    shortBuzz();          // Short beep on button press
    delay(200);           // Button debounce
  }

  // Switch modes when the button is pressed
  if (digitalRead(MODE_BUTTON_PIN) == LOW) {
    currentMode = (currentMode % 2) + 1; // Switch to the next mode
    shortBuzz();                       // Short beep on button press
    delay(200);                        // Button debounce
  }

  // Check for low light
  if (currentTime - lastLightCheckTime >= BUZZER_PAUSE) {
    int lightLevel = analogRead(LIGHT_SENSOR_PIN); // Read light level
    if (lightLevel < LOW_LIGHT_THRESHOLD) {
      lcd.clear();
      lcd.print("Aprinde luminile!"); // "Turn on the lights!"
      soundBuzzer(); // Buzzer sound for warning

      lastLightCheckTime = currentTime; // 3-minute pause between alarms
    }
  }

  // Record speed every 3 seconds
  if (currentTime - lastMeasurementTime >= MEASUREMENT_INTERVAL) {
    float speed = calculateSpeed(); // Calculate current speed
    updateSpeedBuffer(speed);        // Update buffer with current speed

    // Calculate average speed from the buffer
    float averageSpeed = calculateAverageSpeed();

    // Display data based on mode
    lcd.clear();
    if (currentMode == 1) {
      // Mode 1: Speed and Distance
      lcd.setCursor(0, 0);
      lcd.print("Viteza: ");
      if (averageSpeed > 0) {
        lcd.print(averageSpeed, 2); // Display average speed with 2 decimals
        lcd.print(" km/h");
      } else {
        lcd.print("STOP");
      }

      lcd.setCursor(0, 1);
      lcd.print("Distanta: ");
      lcd.print(totalDistance, 2); // Display distance traveled
      lcd.print(" km");
    } else if (currentMode == 2) {
      // Mode 2: Gears and RPM
      lcd.setCursor(0, 0);
      lcd.print("Trepte: ");
      lcd.print(determineGear(averageSpeed));

      lcd.setCursor(0, 1);
      lcd.print("RPM: ");
      lcd.print(calculateRPM(), 2); // Display RPM
    }

    lastMeasurementTime = currentTime;
  }
}

// Function to calculate current speed
float calculateSpeed() {
  if (pulseInterval == 0 || micros() - lastPulseTime > 2000000) {
    return 0.0;
  }
  float timeInSeconds = pulseInterval / 1000000.0;
  float rotationsPerSecond = 1.0 / timeInSeconds;
  return (rotationsPerSecond * WHEEL_CIRCUMFERENCE * 3600) / 1000;
}

// Function to calculate RPM
float calculateRPM() {
  if (pulseInterval == 0) return 0.0;
  return 60.0 / (pulseInterval / 1000000.0);
}

// Function to determine the recommended gear
String determineGear(float speed) {
  if (speed < 5.0) return "1:1";
  if (speed < 10.0) return "1:3";
  if (speed < 15.0) return "2:5";
  if (speed < 25.0) return "3:5";
  return "3:7";
}

// Function for a short beep
void shortBuzz() {
  digitalWrite(BUZZER_PIN, HIGH);
  delay(200); // Duration of the sound
  digitalWrite(BUZZER_PIN, LOW);
}

// Function for buzzer warning
void soundBuzzer() {
  for (int i = 0; i < 3; i++) {
    shortBuzz();
    delay(200); // Pause between beeps
  }
  delay(1000); // Pause between series
}

// Function to update the buffer
void updateSpeedBuffer(float speed) {
  speedBuffer[bufferIndex] = speed;
  bufferIndex = (bufferIndex + 1) % 5;
}

// Function to calculate the average speed
float calculateAverageSpeed() {
  float sum = 0.0;
  for (int i = 0; i < 5; i++) {
    sum += speedBuffer[i];
  }
  return sum / 5.0;
}
