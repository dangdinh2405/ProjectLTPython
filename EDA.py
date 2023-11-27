from tkinter import filedialog, simpledialog

import numpy as np
import pandas as pd
from scipy import stats
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, f_regression
import os
import tkinter as tk


class DataPreprocessing:
    def __init__(self, master, directory_path="./"):
        self.master = master
        
        self.top_level_window = tk.Toplevel(self.master)
        
        self.top_level_window.title("Data Loader")

        self.directory_path = directory_path
        self.selected_csv_file = None
        self.file_path = None
        self.df = None

        self.create_widgets()

    def on_close_callback(self):
        # Close the top-level window
        self.top_level_window.destroy()

    def create_widgets(self):
        # Label and Entry for directory path
        tk.Label(self.top_level_window, text="Đường dẫn thư mục:").grid(row=0, column=0, padx=10, pady=10)
        self.directory_entry = tk.Entry(self.top_level_window, width=50)
        self.directory_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.top_level_window, text="Chọn thư mục", command=self.browse_directory).grid(row=0, column=2, padx=10, pady=10)

        # Button to load data
        tk.Button(self.top_level_window, text="Load Data", command=self.load_data).grid(row=1, column=0, pady=10)

        tk.Button(self.top_level_window, text="Processing", command=self.preprocessing).grid(row=1, column=1, pady=10)

        tk.Button(self.top_level_window, text="Close", command=self.on_close_callback).grid(row=1, column=2, pady=10)

        # Textbox to display DataFrame
        self.textbox = tk.Text(self.top_level_window, width=80, height=20)
        self.textbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


    def browse_directory(self):
        self.directory_path = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(tk.END, self.directory_path)

    def update_textbox(self, message):
        self.textbox.insert(tk.END, message + '\n')
        self.textbox.update_idletasks()

    def get_user_input(self, prompt):
        return simpledialog.askinteger("Input", prompt, parent=self.top_level_window)

    def load_data(self):
        if self.directory_path and os.path.exists(self.directory_path):
            all_files = os.listdir(self.directory_path)
            csv_files = [f for f in all_files if f.endswith(".csv")]

            if csv_files:
                self.update_textbox("Danh sách tệp CSV có sẵn:")
                for i, csv_file in enumerate(csv_files):
                    self.update_textbox(f"{i + 1}. {csv_file}")

                try:
                    selected_index = self.get_user_input("Nhập số tương ứng với tệp bạn muốn chọn:") - 1

                    if 0 <= selected_index < len(csv_files):
                        self.selected_csv_file = csv_files[selected_index]
                        self.file_path = os.path.join(self.directory_path, self.selected_csv_file)
                        self.update_textbox(f"Bạn đã chọn tệp: {self.selected_csv_file}")
                        self.update_textbox(f"Đường dẫn tệp: {self.file_path}")

                        # Đọc dữ liệu từ tệp CSV đã chọn
                        self.df = pd.read_csv(self.file_path)
                        self.update_textbox(f'Độ lớn của bảng [frame] dữ liệu: {self.df.shape}')

                        # Hiển thị số lượng dòng từ DataFrame
                        while True:
                            try:
                                num_rows_to_display = self.get_user_input(
                                    "Nhập số lượng dòng bạn muốn in ra từ DataFrame:")
                                self.update_textbox(str(self.df.head(num_rows_to_display)))
                                break
                            except ValueError:
                                self.update_textbox("Lựa chọn không hợp lệ. Vui lòng nhập một số nguyên.")
                    else:
                        self.update_textbox("Lựa chọn không hợp lệ. Vui lòng chọn số thứ tự hợp lệ.")
                except TypeError:
                    self.update_textbox("Lựa chọn không hợp lệ. Vui lòng nhập một số nguyên.")
            else:
                self.update_textbox("Không có tệp CSV nào trong thư mục.")
        else:
            self.update_textbox(f"Thư mục '{self.directory_path}' không tồn tại.")

    def preprocessing(self):
        # Bước 3: Xử lý CỘT dữ liệu NULL quá nhiều OR không có giá trị phân tích
        count_values = self.df.count().sort_values()
        self.update_textbox("Số lượng giá trị không NULL cho mỗi cột:")
        self.update_textbox(count_values.to_string())  # Chuyển đổi thành chuỗi và hiển thị
        self.update_textbox("Danh sách các cột:")
        for i, column in enumerate(self.df.columns):
            self.update_textbox(f"{i}. {column}")

        # Chọn cột cần xóa
        columns_to_delete = [0, 1, 3]

        # Xóa cột đã chọn
        self.df = self.df.drop(self.df.columns[columns_to_delete], axis=1)

        # Bước 4: Xử lý DÒNG dữ liệu NULL
        self.df = self.df.dropna(how='any')
        self.update_textbox(f"Kích thước DataFrame sau khi xóa các dòng có giá trị null: {self.df.shape}")

        # Bước 5: Xử lý loại bỏ các giá trị ngoại lệ
        # Tính toán Z-Score
        z = np.abs(stats.zscore(self.df[['Postal Code', 'Electric Range', 'Base MSRP', 'DOL Vehicle ID', 'Census Tract']]))

        while True:
            try:
                threshold = self.get_user_input("Nhập ngưỡng giá trị Z-Score: ")
                break
            except ValueError:
                self.update_textbox("Vui lòng nhập một số thực hợp lệ.")

        self.update_textbox(f"Bạn đã chọn ngưỡng Z-Score là {threshold}")

        # Lọc dữ liệu dựa trên Z-Score
        self.df = self.df[(z < threshold).all(axis=1)]
        self.update_textbox(f"Kích thước DataFrame sau khi lọc dựa trên Z-Score: {self.df.shape}")

        # Bước 7: Chuẩn hóa tập dữ liệu Input dùng MinMaxScaler
        scaler = preprocessing.MinMaxScaler()
        selected_columns = ['Electric Range', 'Base MSRP', 'DOL Vehicle ID', 'Census Tract']
        scaler.fit(self.df[selected_columns])
        self.df[selected_columns] = scaler.transform(self.df[selected_columns])

        # In ra một số dòng của DataFrame đã xử lý
        self.update_textbox(self.df.head().to_string())

        # Bước 8: Xác định mô hình trích lọc các thuộc tính đặc trưng: EDA
        numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        if 'Census Tract' in numeric_columns:
            numeric_columns = numeric_columns.drop('Census Tract')

        X = self.df.loc[:, numeric_columns]
        y = self.df['Census Tract']
        selector = SelectKBest(f_regression, k=3)
        selector.fit(X, y)
        X_new = selector.transform(X)
        self.update_textbox(f"{X_new}\n")
        self.update_textbox(pd.DataFrame(y).to_string(index=False) + '\n')
        selected_columns = X.columns[selector.get_support(indices=True)]
        self.update_textbox("\n".join(selected_columns))

        # Bước 9: Xác định mô hình trích lọc các thuộc tính đặc trưng
        # XĐ data frame = Chiếu lấy các thuộc tính đặc trưng đã xđ trong B8
        self.df = self.df[['Electric Range', 'Legislative District', 'DOL Vehicle ID', 'Census Tract']]

        # Bước 10: EDA theo nhu cầu thực tế => input vào các mô hình AI, ML,...
        # Đơn giản nhất là lấy 1 thuộc tính đầu vào (Electric Range) để XD Mô hình
        X = self.df[['Electric Range']]
        y = self.df[['Census Tract']]
        X_str = X.to_string(index=False)
        y_str = y.to_string(index=False)

        self.update_textbox("Dữ liệu của Electric Range:\n" + X_str)
        self.update_textbox("Dữ liệu của Census Tract:\n" + y_str)


if __name__ == "__main__":
    # Khởi tạo đối tượng DataPreprocessing
    root = tk.Tk()
    data_processor = DataPreprocessing(root)
    # data_processor.preprocessing()
    root.mainloop()