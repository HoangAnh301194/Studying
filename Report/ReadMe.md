[D23_Nguyễn Hữu Hoàng Anh]
#Báo cáo lớp ESP ngày 17/01/2025
## A) Kiến thức đã học

### IC 74HC595
- Sơ đồ chân
  ![](https://github.com/user-attachments/assets/9d8c256a-6ef7-4761-9e64-dcd399b7b0be)
  - trong đó các chân từ Q0 đến Q7 để xuất tín hiệu bit 0 hoặc 1, chân Q7' để nối với IC khác,
  - 3 chân Data, ST-CP và SH-CP để nhận dữ diệu, ghi và chốt dữ liệu
  - chân OE kính hoạt mức thấp và MR kích hoạt mức cao 
- cách hoạt động
  - Chân data chịu trách nhiệm nhận đầu vào dữ liệu khi có xung cạnh tích cực của xung nhịp và nó tiếp tục nhận dữ liệu. Những dữ liệu từ thanh ghi dịch chỉ di chuyển sang thanh ghi lưu trữ khi chúng ta kích tín hiệu mức cao của chân Latch để chốt chân đầu vào. Từ đó chuyển tín hiệu xuất ra các chân Q1 - Q7, Q7'.
    ![](https://blog.mecsu.vn/wp-content/uploads/2021/10/Nguyen-ly-lam-viec-cua-thanh-ghi-dich-74HC595.gif)

## Debounce Button
- cách đấu nối:
  ta nối 1 đầu button vào GND , 1 đầu nối với trở và kéo lên VCC, trích tín hiêu giữ nút bấm và trở để chân điều khiển đọc:
  ![image](https://github.com/user-attachments/assets/ea7633ea-e3be-463d-9924-e10c6e4b25b2)

- Nguyên lý hoạt động
  Nút nhất khi hoạt động, chuyển trạng thái thì sẽ có 1 khoảng thời gian rất nhỏ bị mất ổn định trạng thái vì nhiễu, vì vậy để loại bỏ nhiễu ta chỉ cần bỏ qua quãng thời gian bị nhiễu , ta sử dụng hàm millis() bỏ qua quãng thời gian đó.
- ứng dụng với hàm ngắt Interrupt()
  vì trong hàm loop việc ta delay thời gian để bấm nút nếu sử dụng nhiều sẽ dẫn đến việc chương trình bị delay, và quá trình chạy chương trình cũng theo hướng tuyến tính từ trên xuống nên việc đọc nút bấm sẽ phải đợi phần chương trình phía trên hoạt động xong thì nút bấm mới được đọc, từ đó ta sẽ sử dụng hàm ngắt , trong khi chương trình hoạt động ta có thể đọc nút bấm bất kì lúc nào mà nó đổi trạng thái .
  ```cpp
      int buttonPin =2 ; // chân hỗ trợ ngắt của arduino là 2 và 3
      int  ledPin =4;
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
   void setup(){
      pinMode(buttonPin , INPUT);
        attachInterrupt(digitalPinToInterrupt(buttonPin), countPressing , FALLING); // khi nút bẩm đổi trạng thái từ Cao xuống thấp thì thực hiện hàm cộng số lần bấm lên 1
  }
  ```
## Led 7 đoạn
- Phân loại
  - có 2 loại led 7 đoạn: chung Anot và chung Catot:
  - Chung Anot ( chung dương) : các đèn đều có chân dương chung với nhau:
  - ![image](https://github.com/user-attachments/assets/249fe7fe-fcb5-41a5-aaeb-c0724eefe1b7)

  - Chung Catot ( Âm chugn) : các đèn có chân Âm chugn với nhau:
  - ![image](https://github.com/user-attachments/assets/3c761fd8-345c-4e11-b2f4-4a326c9e4b0b)

- cách đấu nối
  ví dụng đối với led Âm chung:
  Chân âm chung sẽ nối đất, các led đoạn sẽ nối tới chân tín hiệu thông qua trở ( bài nì em lười lấy 8 con trở nên lấy 1 con cho chugn cả :3 ) 
  ![image](https://github.com/user-attachments/assets/d991d0bc-8510-4d6d-91ed-829c776f557a)

- cách điều khiển
để đèn sáng ta chỉ cần xuất tín hiệu mức cao vào chân của thanh led đó
```
byte value = 0b01111111; xuất tín hiệu mức cao vào cả 7 chân led
void loop(){
   digitalWrite(latchPin1, LOW);
  shiftOut(dataPin1, clockPin1, MSBFIRST, value);
  digitalWrite(latchPin1, HIGH);
}
```
## B) Bài tập về nhà
- điều khiển 8 led với IC 74hc595
  - code nguyên lý 
  - link code :
- điều khiển led 4 số với IC 74hc595
  - code nguyên lý
  - link code:
- video demo ( em mô phỏng cả 3 bài tập về button, nháy led , và chạy led 7 đoạn 1 và 4 số cùng 1 video luon ạ )
  [link Video YTB](https://youtu.be/-V8d1MRvUI0)
## C) Khó khăn 
- quy luật dịch bit của các hiệu ứng em chưa nghĩ được nên chỉ làm được hiệu ứng mưa thoi ạ
## D) linh kiện mượn của CLB
- Không
