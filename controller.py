from tkinter import messagebox, filedialog
import tkinter as tk

class StudentController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Đăng ký sự kiện các nút chính
        self.view.btn_add.config(command=self.open_add_dialog)
        self.view.btn_edit.config(command=self.open_edit_dialog)
        self.view.btn_delete.config(command=self.delete_student)
        self.view.btn_export.config(command=self.export_excel)
        
        # Đăng ký sự kiện tìm kiếm
        self.view.btn_search.config(command=self.search_student)
        self.view.btn_reset_search.config(command=self.reset_search)

        # Hiển thị dữ liệu trống ban đầu để cập nhật dòng đếm
        self.refresh_treeview()

    def refresh_treeview(self, df_to_display=None):
        if df_to_display is None:
            df_to_display = self.model.df
                
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
            
        count_dat = 0
        count_truot = 0
        
        for _, row in df_to_display.iterrows():
            if row['KetQua'] == "Đạt học bổng":
                tag = 'dat'
                count_dat += 1
            else:
                tag = 'truot'
                count_truot += 1
                
            values = (row['MSV'], row['HoTen'], row['GioiTinh'], row['Lop'], 
                      row['SDT'], row['GPA'], row['DRL'], row['KetQua'])
            self.view.tree.insert("", "end", values=values, tags=(tag,))
            
        self.view.lbl_stats.config(
            text=f"Số SV đạt học bổng: {count_dat}   |   Số SV không đạt: {count_truot}"
        )

    def get_data_from_entries(self, entries):
        return {key: entry.get().strip() for key, entry in entries.items()}

    def open_add_dialog(self):
        dialog, entries, btn_save = self.view.create_form_dialog("Thêm Sinh viên")

        def save():
            data = self.get_data_from_entries(entries)
            is_valid, msg = self.model.validate_data(data['MSV'], data['HoTen'], data['GPA'], data['DRL'])
            if not is_valid:
                messagebox.showwarning("Lỗi", msg, parent=dialog)
                return
            if data['MSV'] in self.model.df['MSV'].values:
                messagebox.showwarning("Lỗi", "Mã sinh viên đã tồn tại!", parent=dialog)
                return

            self.model.add_student(data)
            self.refresh_treeview()
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã thêm sinh viên!")

        btn_save.config(command=save)

    def open_edit_dialog(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một sinh viên để sửa!")
            return

        item_values = self.view.tree.item(selected_item[0])['values']
        msv_old = str(item_values[0])

        dialog, entries, btn_save = self.view.create_form_dialog("Sửa Sinh viên")

        for i, key in enumerate(["MSV", "HoTen", "GioiTinh", "Lop", "SDT", "GPA", "DRL"]):
            if key == "GioiTinh":
                entries[key].set(item_values[i])
            else:
                entries[key].insert(0, item_values[i])

        def save():
            data = self.get_data_from_entries(entries)
            is_valid, msg = self.model.validate_data(data['MSV'], data['HoTen'], data['GPA'], data['DRL'])
            if not is_valid:
                messagebox.showwarning("Lỗi", msg, parent=dialog)
                return
            if data['MSV'] != msv_old and data['MSV'] in self.model.df['MSV'].values:
                messagebox.showwarning("Lỗi", "Mã sinh viên mới đã tồn tại!", parent=dialog)
                return

            self.model.update_student(msv_old, data)
            self.refresh_treeview()
            dialog.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")

        btn_save.config(command=save)

    def delete_student(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một sinh viên để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
            msv = str(self.view.tree.item(selected_item[0])['values'][0])
            self.model.delete_student(msv)
            self.refresh_treeview()

    # HÀM TÌM KIẾM ĐÃ ĐƯỢC CẢI TIẾN THÊM POPUP THÔNG BÁO
    def search_student(self):
        query = self.view.entry_search.get().strip()
        if not query:
            messagebox.showwarning("Thông báo", "Vui lòng nhập Mã SV hoặc Họ tên để tìm kiếm!")
            return

        filtered_df = self.model.search_students(query)
        
        # Cập nhật danh sách hiển thị và bộ đếm bên dưới trước
        self.refresh_treeview(filtered_df)

        if filtered_df.empty:
            messagebox.showinfo("Kết quả tìm kiếm", f"Không tìm thấy sinh viên nào khớp với từ khóa: '{query}'")
            return
        
        # Gom thông tin các sinh viên tìm thấy thành chuỗi văn bản để hiển thị lên hộp thoại thông báo
        thong_tin_popup = "🔍 KẾT QUẢ TÌM THẤY:\n"
        thong_tin_popup += "="*40 + "\n"
        
        for _, row in filtered_df.iterrows():
            thong_tin_popup += f"• MSV: {row['MSV']}\n"
            thong_tin_popup += f"• Họ và tên: {row['HoTen']}\n"
            thong_tin_popup += f"• Lớp: {row['Lop']} | Giới tính: {row['GioiTinh']}\n"
            thong_tin_popup += f"• GPA: {row['GPA']} | Điểm RL: {row['DRL']}\n"
            thong_tin_popup += f"➔ XÉT HỌC BỔNG: {row['KetQua'].upper()}\n"
            thong_tin_popup += "-"*40 + "\n"
            
        # Hiển thị bảng thông báo lên màn hình
        messagebox.showinfo("Thông tin tìm kiếm sinh viên", thong_tin_popup)
        
    def reset_search(self):
        self.view.entry_search.delete(0, tk.END)
        self.refresh_treeview()

    def export_excel(self):
        if self.model.df.empty:
            messagebox.showwarning("Trống", "Chưa có dữ liệu để xuất file!")
            return
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                title="Chọn nơi lưu file",
                initialfile="Ket_qua_hoc_bong.xlsx"
            )
            if file_path:
                self.model.export_to_excel(file_path)
                messagebox.showinfo("Thành công", f"Đã lưu file tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")