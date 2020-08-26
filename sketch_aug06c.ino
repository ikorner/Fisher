#include <Keyboard.h>
#define LED_PIN SS

char inChar;
char F1 = KEY_F1;
char F2 = KEY_F2;
char F3 = KEY_F3;

void setup() {
  pinMode(LED_PIN, OUTPUT); // Инициализация светодиода
  Serial.begin(115200); // Инициализация Serial - порта
  Keyboard.begin(); // Инициализация Клавиатуры
}

void loop() {
  if (Serial.available() > 0)
  {
    inChar = Serial.read();
    if (inChar=='e') // e - Enable - включить
    {
      digitalWrite(LED_PIN,HIGH);
      Keyboard.press(F1);
      delay(100);
      Keyboard.releaseAll();
      inChar = '1';
    }
  }
  
    else if (inChar=='d') // d - Disable - выключить
    {
      digitalWrite(LED_PIN,LOW);
       Keyboard.press(F2);
       delay(100);
      Keyboard.releaseAll();
      inChar = '1';
    }
  
    else if (inChar=='b')  // b - Blink - выключить режим мигания
    {
      
      digitalWrite(LED_PIN,HIGH);
      delay(500);
      digitalWrite(LED_PIN,LOW);
      delay(500);
      Keyboard.press(F3);
      delay(300);
      Keyboard.releaseAll();
      inChar = '1';
    }
    
}
