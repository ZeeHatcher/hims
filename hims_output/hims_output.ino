// Pin definitions
#define RS 12
#define EN 11
#define D4 5
#define D5 4
#define D6 3
#define D7 2
#define BUZZER 6

#define COL 16
#define ROW 2

#include <LiquidCrystal.h>

const int VOLUME = 60;
const int SPEED = 300;
const int PAUSE_TIME = 2000;

LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);
String str;
char c[COL + 1];

void setup() {
  lcd.begin(COL, ROW);
  Serial.begin(9600);

  pinMode(BUZZER, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String in;
    
    while (Serial.available() > 0) {
      in = Serial.readString();
    }
    
    if (in.compareTo(str) != 0) {
      analogWrite(BUZZER, VOLUME);
      delay(100);
      analogWrite(BUZZER, 0);
      
      str = in;
    }
    
    lcd.clear();
  }
  
  lcd.setCursor(0, 0);
  lcd.write("---| TO BUY |---");
  
  lcd.setCursor(0, 1);
  
  if (str.length() > COL) {
    int extra = str.length() - COL;
    
    for (int i = 0; i <= extra; i++) {
      str.substring(i, COL + i).toCharArray(c, 17);
     
      lcd.write(c);
      
      if (i == 0) delay(PAUSE_TIME);
      
      delay(SPEED);
      
      lcd.setCursor(0, 1);
    }
    
    delay(PAUSE_TIME);
  } else {
    str.toCharArray(c, 17);
    lcd.write(c);
  }
}
