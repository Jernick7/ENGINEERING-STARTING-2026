void setup() {
  // Pin 3 is our audio output
}

void loop() {
  // Sweep up from 300Hz to 1500Hz
  for (int freq = 1300; freq <= 1500; freq += 10) {
    tone(3, freq);
    delay(5); // Controls how fast the sweep goes
  }
  
  delay(500); // Wait half a second at the top
}