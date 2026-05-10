import tkinter as tk

root = tk.Tk()
root.title("Quản lý Sinh viên - UHL")
root.geometry("400x250")

# Cấu hình cho cột 1 (cột chứa ô nhập liệu) co giãn
root.columnconfigure(1, weight=1)

# 1. Tạo các thành phần
nhan_ma_sv = tk.Label(root, text="Mã sinh viên:")
o_nhap_ma_sv = tk.Entry(root)

nhan_ho_ten = tk.Label(root, text="Họ và tên:")
o_nhap_ho_ten = tk.Entry(root)

# 2. Sắp xếp các thành phần bằng grid

# Hàng 0: Mã sinh viên
nhan_ma_sv.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# Thêm sticky="ew" để ô nhập mã kéo giãn
o_nhap_ma_sv.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Hàng 1: Họ và tên
nhan_ho_ten.grid(row=1, column=0, padx=10, pady=10, sticky="w")
# Thêm sticky="ew" để ô nhập họ tên cũng kéo giãn theo
o_nhap_ho_ten.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

root.mainloop()