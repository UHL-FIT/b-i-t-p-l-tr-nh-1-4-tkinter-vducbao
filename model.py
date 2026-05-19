import pandas as pd
import re

class StudentModel:
    def __init__(self):
        self.df = pd.DataFrame(columns=['MSV', 'HoTen', 'GioiTinh', 'Lop', 'SDT', 'GPA', 'DRL', 'KetQua'])

    def validate_data(self, msv, hoten, gpa_str, drl_str):
        if not msv or not hoten or not gpa_str or not drl_str:
            return False, "Vui lòng nhập đầy đủ các trường bắt buộc (*) và điểm số!"

        pattern_msv = r"^(1[4-9]|2[0-6])(dh|DH)\d{6}$"
        if not re.match(pattern_msv, msv):
            return False, "Mã SV không hợp lệ!\nĐịnh dạng: 2 số đầu (14-26) + 'dh'/'DH' + 6 số cuối."

        try:
            gpa = float(gpa_str)
            drl = float(drl_str)
            if not (0 <= gpa <= 4):
                return False, "GPA phải nằm trong khoảng từ 0 đến 4.0!"
            if not (0 <= drl <= 100):
                return False, "Điểm rèn luyện phải từ 0 đến 100!"
        except ValueError:
            return False, "GPA và Điểm RL phải là số thực!"

        return True, "Hợp lệ"

    def calculate_scholarship(self, gpa, drl):
        is_eligible = (gpa >= 3.2 and drl >= 80) or (gpa >= 3.6)
        return "Đạt học bổng" if is_eligible else "Không đạt"

    def add_student(self, data):
        data['KetQua'] = self.calculate_scholarship(float(data['GPA']), float(data['DRL']))
        new_df = pd.DataFrame([data])
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    def update_student(self, msv_old, new_data):
        new_data['KetQua'] = self.calculate_scholarship(float(new_data['GPA']), float(new_data['DRL']))
        idx = self.df.index[self.df['MSV'] == msv_old].tolist()
        if idx:
            for key, value in new_data.items():
                self.df.at[idx[0], key] = value

    def delete_student(self, msv):
        self.df = self.df[self.df['MSV'] != msv].reset_index(drop=True)

    def search_students(self, query):
        if not query:
            return self.df
        query = query.lower()
        # Tìm kiếm không phân biệt chữ hoa thường theo Mã SV hoặc Họ Tên
        filtered_df = self.df[
            self.df['MSV'].astype(str).str.lower().str.contains(query) | 
            self.df['HoTen'].astype(str).str.lower().str.contains(query)
        ]
        return filtered_df

    def export_to_excel(self, file_path):
        self.df.to_excel(file_path, index=False)