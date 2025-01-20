// Chân kết nối IC điều khiển LED 1 số
int latchPin1 = 11; // ST_CP
int clockPin1 = 12; // SH_CP
int dataPin1 = 13;  // DS

const int buttonPin = 2; // Chân kết nối nút nhấn
int pressCount = 0;      // Biến đếm số lần nhấn nút
void  countPressing() {
  static unsigned long lastInterruptTime = 0; // Thời gian xảy ra ngắt lần cuối
  unsigned long interruptTime = millis();    // Thời gian hiện tại

  // Nếu thời gian giữa hai lần ngắt lớn hơn ngưỡng debounce
  if (interruptTime - lastInterruptTime > 40) { 
    pressCount++; // Tăng biến đếm
  }
  lastInterruptTime = interruptTime; // Cập nhật thời gian ngắt cuối
}

// Chân kết nối IC điều khiển LED 4 số
int latchPin2 = 7;  // ST_CP
int clockPin2 = 9;  // SH_CP
int dataPin2 = 8;   // DS

// Chân chọn số cho LED 4 số
int digitSelect[] = {3, 4, 5, 6};

// Bảng mã hiển thị số trên LED 7 đoạn
const byte numbers[] = {
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111101, // 6
  0b00000111, // 7
  0b01111111, // 8
  0b01101111  // 9
};

void setup() {
  // Cấu hình các chân IC là OUTPUT
  pinMode(latchPin1, OUTPUT);
  pinMode(clockPin1, OUTPUT);
  pinMode(dataPin1, OUTPUT);
pinMode(buttonPin, INPUT);
  pinMode(latchPin2, OUTPUT);
  pinMode(clockPin2, OUTPUT);
  pinMode(dataPin2, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(buttonPin), countPressing , FALLING);
  // Cấu hình các chân chọn số cho LED 4 số là OUTPUT
  for (int i = 0; i < 4; i++) {
    pinMode(digitSelect[i], OUTPUT);
    digitalWrite(digitSelect[i], HIGH); // Tắt tất cả các số ban đầu
  }
}

// Hiển thị một chữ số trên LED 1 số
void displaySingleDigit(byte value) {
  digitalWrite(latchPin1, LOW);
  shiftOut(dataPin1, clockPin1, MSBFIRST, value);
  digitalWrite(latchPin1, HIGH);
}

// Hiển thị số trên LED 4 số
void displayFourDigits(int number) {
  // Tách các chữ số từ số nguyên `number`
  int digits[4];
  digits[0] = (number / 1000) % 10; // Hàng nghìn
  digits[1] = (number / 100) % 10;  // Hàng trăm
  digits[2] = (number / 10) % 10;   // Hàng chục
  digits[3] = number % 10;          // Hàng đơn vị

  // Quét qua từng chữ số
  for (int i = 0; i < 4; i++) {
    // Tắt tất cả các số
    for (int j = 0; j < 4; j++) {
      digitalWrite(digitSelect[j], HIGH);
    }

    // Hiển thị chữ số hiện tại
    digitalWrite(latchPin2, LOW);
    shiftOut(dataPin2, clockPin2, MSBFIRST, numbers[digits[i]]);
    digitalWrite(latchPin2, HIGH);

    // Chọn số hiện tại
    digitalWrite(digitSelect[i], LOW);

    // Giữ chữ số trong một khoảng thời gian ngắn
    delay(5);
  }
}
void run(){  
  for (int num = 1234; num <= 9999; num++) {
    // Hiển thị giá trị hàng nghìn trên LED 1 số
    // Hiển thị toàn bộ số trên LED 4 số
    displayFourDigits(num);

    // Đợi một khoảng thời gian
    delay(50); // Điều chỉnh tốc độ đếm
  }

}
void count() {
  for (int i = 0; i < 10; i++) {
    // Lấy byte tương ứng với số hiện tại
    byte x = numbers[i];
    displaySingleDigit(x);
    delay(100);
  }
}
void loop() {
if(pressCount %2 ==0){
  count();
}
else {
  run();
}
}
