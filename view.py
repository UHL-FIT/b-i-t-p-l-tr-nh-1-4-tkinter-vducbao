import tkinter as tk
from tkinter import ttk

class StudentView:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Học bổng 2026 (MVC)")
        self.root.geometry("950x600")
        self.root.configure(bg="#f0f3f5")

        # Tiêu đề chính
        tk.Label(root, text="QUẢN LÝ XÉT DUYỆT HỌC BỔNG", font=("Arial", 16, "bold"), bg="#f0f3f5", fg="#2c3e50").pack(pady=10)

        # Thanh nút chức năng
        self.btn_frame = tk.Frame(root, bg="#f0f3f5")
        self.btn_frame.pack(pady=5)

        self.btn_add = tk.Button(self.btn_frame, text="THÊM SINH VIÊN", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_add.pack(side="left", padx=10)

        self.btn_edit = tk.Button(self.btn_frame, text="SỬA THÔNG TIN", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_edit.pack(side="left", padx=10)
        
        self.btn_delete = tk.Button(self.btn_frame, text="XÓA", bg="#c0392b", fg="white", font=("Arial", 10, "bold"), width=10)
        self.btn_delete.pack(side="left", padx=10)

        self.btn_export = tk.Button(self.btn_frame, text="XUẤT EXCEL", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), width=15)
        self.btn_export.pack(side="left", padx=10)

        # THANH TÌM KIẾM (Mới bổ sung)
        self.search_frame = tk.Frame(root, bg="#f0f3f5")
        self.search_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(self.search_frame, text="Tìm kiếm (MSV / Họ tên):", font=("Arial", 10), bg="#f0f3f5").pack(side="left", padx=5)
        self.entry_search = tk.Entry(self.search_frame, font=("Arial", 10), width=30)
        self.entry_search.pack(side="left", padx=5)
        
        self.btn_search = tk.Button(self.search_frame, text="TÌM KIẾM", bg="#34495e", fg="white", font=("Arial", 9, "bold"), width=10)
        self.btn_search.pack(side="left", padx=5)
        
        self.btn_reset_search = tk.Button(self.search_frame, text="HỦY LỌC", bg="#7f8c8d", fg="white", font=("Arial", 9, "bold"), width=10)
        self.btn_reset_search.pack(side="left", padx=5)

        # Bảng dữ liệu Treeview
        self.columns = ("MSV", "HoTen", "GioiTinh", "Lop", "SDT", "GPA", "DRL", "KetQua")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings", height=12)
        
        headers = ["MSV", "Họ Tên", "Giới tính", "Lớp", "SĐT", "GPA", "Điểm RL", "Kết Quả"]
        widths = [100, 160, 70, 80, 100, 60, 70, 120]
        
        for col, header, w in zip(self.columns, headers, widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=w)

        self.tree.tag_configure('dat', foreground='#1b5e20', background='#e8f5e9')
        self.tree.tag_configure('truot', foreground='#b71c1c', background='#ffebee')
        self.tree.pack(pady=5, padx=20, fill="both", expand=True)

        # DÒNG THỐNG KÊ SỐ LƯỢNG (Mới bổ sung)
        self.lbl_stats = tk.Label(root, text="Số SV đạt học bổng: 0   |   Số SV không đạt: 0", font=("Arial", 11, "bold"), bg="#f0f3f5", fg="#2c3e50")
        self.lbl_stats.pack(pady=15)

    def create_form_dialog(self, title):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        entries = {}
        fields = [
            ("MSV (*):", "MSV"), ("Họ tên (*):", "HoTen"), 
            ("Giới tính:", "GioiTinh"), ("Lớp:", "Lop"), 
            ("SĐT:", "SDT"), ("GPA (*):", "GPA"), ("Điểm RL (*):", "DRL")
        ]

        for i, (label_text, key) in enumerate(fields):
            tk.Label(dialog, text=label_text).grid(row=i, column=0, padx=15, pady=10, sticky="e")
            if key == "GioiTinh":
                entry = ttk.Combobox(dialog, values=["Nam", "Nữ", "Khác"], state="readonly", width=25)
                entry.set("Nam")
            else:
                entry = tk.Entry(dialog, width=28)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry

        frame_btn = tk.Frame(dialog)
        frame_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        btn_save = tk.Button(frame_btn, text="Lưu", width=10)
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = tk.Button(frame_btn, text="Hủy", width=10, command=dialog.destroy)
        btn_cancel.pack(side="left", padx=10)

        return dialog, entries, btn_save