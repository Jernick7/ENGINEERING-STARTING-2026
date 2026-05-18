#include <Arduino.h>
#include "Talkie.h"
#include "vocab_us_large.h" // Modern 1.4.0 layout uses lowercase filenames!

Talkie voice;

void setup() {
    Serial.begin(9600); // Opens communication with your laptop
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        
        switch(command) {
            // Version 1.4.0 uses clear, modern lowercase naming structures!
            case 'h': voice.say(sp2_YELLOW); break;  
            case 'a': voice.say(sp2_ALERT); break;  
            case 'd': voice.say(sp2_DANGER); break; 
            case 'b': voice.say(sp3_BY); break;    
        }
    }
}