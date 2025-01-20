/*
shiftOut với 8 LED bằng 1 IC HC595
*/
//chân ST_CP (Chân 12) của 74HC595
int latchPin = 11;
//chân SH_CP (Chân 11) của 74HC595
int clockPin = 12;
//Chân DS (chân 14) của 74HC595
int dataPin = 13;

const int buttonPin = 3; // Chân kết nối nút nhấn
int pressCount = 0;      // Biến đếm số lần nhấn nút
void  countPressing() {
  static unsigned long lastInterruptTime = 0; // Thời gian xảy ra ngắt lần cuối
  unsigned long interruptTime = millis();    // Thời gian hiện tại

  // Nếu thời gian giữa hai lần ngắt lớn hơn ngưỡng debounce
  if (interruptTime - lastInterruptTime > 50) { 
    pressCount++; // Tăng biến đếm
  }
  lastInterruptTime = interruptTime; // Cập nhật thời gian ngắt cuối
}

//Trạng thái của LED, hay chính là byte mà ta sẽ gửi qua shiftOut
byte ledStatus = 0;
void setup() {
  //Bạn BUỘC PHẢI pinMode các chân này là OUTPUT
  pinMode(buttonPin, INPUT);
    attachInterrupt(digitalPinToInterrupt(buttonPin), countPressing , FALLING);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}
int x=0;
void rainy(){
    ledStatus = 1<<x;
  //ShiftOut ra IC
  shiftOut(dataPin, clockPin, MSBFIRST, ledStatus);  
  digitalWrite(latchPin, HIGH);//các đèn LED sẽ sáng với trạng thái vừa được cập nhập
  delay(100);
    digitalWrite(latchPin, LOW);//các đèn LED sẽ sáng với trạng thái vừa được cập nhập
    x++;
    if(x==9){
      ledStatus = 0;
      x=0;
    }
}
void loop() { 
  digitalWrite(2,LOW);
  if(pressCount %2==0){
    rainy();
  }

}