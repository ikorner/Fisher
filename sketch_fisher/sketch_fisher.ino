#include <Keyboard.h>
#define LED_PIN SS

// задание необходимых переменных
char inChar; 
char F1 = KEY_F1; 
char F2 = KEY_F2;
char F3 = KEY_F3;
char F4 = KEY_F4;
char F5 = KEY_F5;


void setup() {
  pinMode(LED_PIN, OUTPUT); // Инициализация светодиода
  Serial.begin(115200); // Инициализация Serial - порта
  Keyboard.begin(); // Инициализация Клавиатуры
}

void loop() {
  if (Serial.available() > 0)
  {
    inChar = Serial.read();
    if (inChar=='e') // e - Enable - включить светодиод. Начало "рыбалки" - нажатие F1
    {
      digitalWrite(LED_PIN,HIGH);
      Keyboard.press(F1);
      delay(100);
      Keyboard.releaseAll();
      inChar = '1';
    }
  }
  
    else if (inChar=='d') // d - Disable - выключить светодиод. "Подтягивание" рыбы - нажатие F2
    {
      digitalWrite(LED_PIN,LOW);
       Keyboard.press(F2);
       delay(100);
      Keyboard.releaseAll();
      inChar = '1';
    }
  
    else if (inChar=='b')  // b - Blink - выключить режим мигания. "Подсекание" рыбы - Нажатие F3
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

    else if (inChar=='1') // После каждого действия отправляем нажатие F4 и F5, где настроено "секретное действие"
    {
      Keyboard.press(F4);
      delay(300);
      Keyboard.releaseAll();
      Keyboard.press(F5);
      delay(300);
      Keyboard.releaseAll();
      inChar = '2';
    }
    }
}
