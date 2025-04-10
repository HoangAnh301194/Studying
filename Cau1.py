
import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import re
from datetime import datetime

# Lấy đường dẫn khi chạy exe hoặc script
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

DATA_FILE = resource_path("data/members.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Thành viên")
        self.geometry("700x500")
        self.frames = {}

        for F in (StartPage, InfoPage, MergePage, SortPage, SearchPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(x=0, y=0, width=700, height=500)

        self.show_frame(StartPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
def chuan_hoa_chuoi(s):
    return " ".join(word.capitalize() for word in s.strip().lower().split())
def chuan_hoa_mssv(mssv):
    return mssv.strip().upper()
# --- Start Page ---
class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Ứng dụng Quản lý Sinh viên", font=("Arial", 35)).pack(pady=75)
        tk.Button(self, text="Nhập Thông tin", command=lambda: master.show_frame(InfoPage), width=30).pack(pady=10)
        tk.Button(self, text="Ghép + Phân tích", command=lambda: master.show_frame(MergePage), width=30).pack(pady=10)
        tk.Button(self, text="Sắp xếp số", command=lambda: master.show_frame(SortPage), width=30).pack(pady=10)
        tk.Button(self, text="Tìm kiếm", command=lambda: master.show_frame(SearchPage), width=30).pack(pady=10)

# --- Info Page ---
class InfoPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Nhập Thông Tin Thành Viên", font=("Arial", 16)).pack(pady=10)

        self.entries = {}
        labels = {
            "name": "Họ và tên :",
            "mssv": "Mã số sinh viên :",
            "birth": "Ngày sinh (dd/mm/yyyy):",
            "hometown": "Quê quán:"
        }

        for key, label in labels.items():
            tk.Label(self, text=label).pack(pady=10)
            entry = tk.Entry(self, width=60)
            entry.pack()
            self.entries[key] = entry

        tk.Button(self, text="  Lưu   ", command=self.save_data).pack(pady=20, padx=80, side="top")  
        tk.Button(self, text="Quay lại", command=lambda: master.show_frame(StartPage)).pack(pady=10, padx=10, side="top")  

    def save_data(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        name = chuan_hoa_chuoi(self.entries["name"].get())
        mssv = chuan_hoa_mssv(self.entries["mssv"].get())
        birth = self.entries["birth"].get().strip()
        hometown = chuan_hoa_chuoi(self.entries["hometown"].get())

        # Kiểm tra bỏ trống
        if not name or not mssv or not birth or not hometown:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Kiểm tra định dạng ngày sinh dd/mm/yyyy
        try:
            datetime.strptime(birth, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày sinh không hợp lệ! Định dạng đúng: dd/mm/yyyy (VD: 01/02/2000)")
            return

        # Kiểm tra MSSV không có khoảng trắng
        if " " in mssv:
            messagebox.showerror("Lỗi", "Mã số sinh viên không được chứa khoảng trắng.")
            return

        # Lưu dữ liệu nếu hợp lệ
        member = {
            "name": name,
            "mssv": mssv,
            "birth": birth,
            "hometown": hometown
        }

        data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        data.append(member)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Thông báo", "Đã lưu thành công!")
# --- Merge Page ---
class MergePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Ghép MSSV + Ngày sinh và phân tích", font=("Arial", 16)).pack(pady=10)
        self.result = tk.Text(self, height=20, width=100)
        self.result.pack()
        tk.Button(self, text="Thực hiện", command=self.merge_data).pack(pady=5)
        tk.Button(self, text="Quay lại", command=lambda: master.show_frame(StartPage)).pack()

    def merge_data(self):
        if not os.path.exists(DATA_FILE): return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.result.delete("1.0", tk.END)
        total = len(data)
        self.result.insert(tk.END, f"Tổng số sinh viên: {total}\n\n")

        data.sort(key=lambda x: x['mssv'])

        for idx, member in enumerate(data, start=1):
            name = member['name']
            mssv = member['mssv']
            birth = member['birth'].replace("/", "")
            combined = f"{mssv}{birth}"
            combined_list = "[ " + ", ".join(ch for ch in combined) + " ]"


            # Lấy số và ký tự từ cả MSSV và ngày sinh
            all_text = mssv + birth
            digits = [int(ch) for ch in all_text if ch.isdigit()]
            chars = [ch for ch in all_text if not ch.isdigit()]

            self.result.insert(tk.END, f"{idx} - {name}\n")
            self.result.insert(tk.END, f"  → Chuỗi ghép : {combined_list}\n")
            self.result.insert(tk.END, f"  → Mảng số    : {digits}\n")
            self.result.insert(tk.END, f"  → Mảng ký tự : {chars}\n\n")

# --- Sort Page ---
class SortPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Sắp xếp mảng số giảm dần", font=("Arial", 16)).pack(pady=10)
        self.result = tk.Text(self, height=21, width=100)
        self.result.pack()
        tk.Button(self, text="Sắp xếp", command=self.sort_data).pack(pady=5)
        tk.Button(self, text="Quay lại", command=lambda: master.show_frame(StartPage)).pack()

    def sort_data(self):
        if not os.path.exists(DATA_FILE): return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.result.delete("1.0", tk.END)
        total = len(data)
        self.result.insert(tk.END, f"Tổng số sinh viên: {total}\n\n")

        data.sort(key=lambda x: x['mssv'])

        for idx, member in enumerate(data, start=1):
            mssv_digits = [int(ch) for ch in member['mssv'] if ch.isdigit()]
            birth_digits = [int(ch) for ch in member['birth'] if ch.isdigit()]
            all_digits = mssv_digits + birth_digits
            sorted_digits = sorted(all_digits, reverse=False)

            self.result.insert(tk.END, f"{idx} - {member['name']}\n")
            self.result.insert(tk.END, f"  → Mảng số gốc  : {all_digits}\n")
            self.result.insert(tk.END, f"  → Đã sắp xếp ↓ : {sorted_digits}\n\n")

# --- Search Page ---
class SearchPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Tìm kiếm thành viên", font=("Arial", 16)).pack(pady=10)
        self.query = tk.Entry(self, width=40)
        self.query.pack()
        tk.Button(self, text="Tìm theo tên hoặc quê", command=self.search_member).pack(pady=5)
        self.result = tk.Text(self, height=20, width=100)
        self.result.pack()
        tk.Button(self, text="Quay lại", command=lambda: master.show_frame(StartPage)).pack()

    def search_member(self):
        if not os.path.exists(DATA_FILE): return
        query = self.query.get().lower()
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.result.delete("1.0", tk.END)
        found = 0
        data.sort(key=lambda x: x['mssv'])

        for idx, member in enumerate(data, start=1):
            if query in member['name'].lower() or query in member['hometown'].lower():
                found += 1
                self.result.insert(tk.END, f"STT {idx} - {member['name']}\n")
                self.result.insert(tk.END, json.dumps(member, indent=4, ensure_ascii=False) + "\n\n")

        if found == 0:
            self.result.insert(tk.END, "Không tìm thấy kết quả phù hợp.\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
