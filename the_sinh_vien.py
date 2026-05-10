import tkinter as tk

root = tk.Tk()
root.title("Thẻ Sinh Viên Số")
root.geometry("400x350") # Tăng nhẹ chiều cao để chứa thêm dòng mới

# 1. Đổi màu nền của toàn bộ cửa sổ sang màu xám nhạt
root.configure(bg="#f8f9fa")

# Nhãn tiêu đề
nhan_truong = tk.Label(
    root, 
    text="TRƯỜNG ĐẠI HỌC HẠ LONG", 
    font=("Arial", 14, "bold"), 
    fg="white", 
    bg="#0056b3"
)
nhan_truong.pack(fill="x", pady=10)

# Nhãn hiển thị họ tên
nhan_ten = tk.Label(root, text="Họ tên: Nguyễn Văn A", font=("Arial", 12), bg="#f8f9fa")
nhan_ten.pack(pady=5)

# 2. Thêm dòng chữ "Khoa: Công nghệ thông tin" với màu xanh lá cây
nhan_khoa = tk.Label(
    root, 
    text="Khoa: Công nghệ thông tin", 
    font=("Arial", 12), 
    fg="green", 
    bg="#f8f9fa" # Đảm bảo màu nền nhãn khớp với màu nền cửa sổ
)
nhan_khoa.pack(pady=5)

# Nhãn hiển thị MSSV
nhan_msv = tk.Label(root, text="MSSV: 22010001", font=("Arial", 12), fg="red", bg="#f8f9fa")
nhan_msv.pack(pady=5)

# 3. Thay đổi kích thước nút bấm to hơn (dùng width và height)
nut_thoat = tk.Button(
    root, 
    text="Đóng ứng dụng", 
    command=root.destroy, 
    bg="#dc3545", 
    fg="white",
    font=("Arial", 10, "bold"),
    width=20,  # Độ rộng (tính theo số ký tự trung bình)
    height=2   # Độ cao (tính theo số dòng)
)
nut_thoat.pack(pady=20)

root.mainloop()
