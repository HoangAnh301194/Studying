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
- Nguyên lý hoạt động
- ứng dụng với hàm ngắt Interrupt()
## Led 7 đoạn
- Phân loại
- cách đấu nối
- cách điều khiển

## B) Bài tập về nhà
- điều khiển 8 led với IC 74hc595
- điều khiển led 4 số với IC 74hc595

## C) Khó khăn 
- quy luật dịch bit của các hiệu ứng em chưa nghĩ được nên chỉ làm được hiệu ứng mưa thoi ạ
## D) linh kiện mượn của CLB
- Không
