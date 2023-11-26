import numpy as np
import pandas as pd
from scipy import stats
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, f_regression
import os

class DataPreprocessing:
    def __init__(self, directory_path="./"):
        self.directory_path = directory_path
        self.file_path = None
        self.df = None

    def load_data(self):
        if os.path.exists(self.directory_path):
            all_files = os.listdir(self.directory_path)
            csv_files = [f for f in all_files if f.endswith(".csv")]

            if csv_files:
                print("Danh sách tệp CSV có sẵn:")
                for i, csv_file in enumerate(csv_files):
                    print(f"{i + 1}. {csv_file}")

                try:
                    selected_index = int(input("Nhập số tương ứng với tệp bạn muốn chọn: ")) - 1

                    if 0 <= selected_index < len(csv_files):
                        self.selected_csv_file = csv_files[selected_index]
                        self.file_path = os.path.join(self.directory_path, self.selected_csv_file)
                        print(f"Bạn đã chọn tệp: {self.selected_csv_file}")
                        print(f"Đường dẫn tệp: {self.file_path}")
                    else:
                        print("Lựa chọn không hợp lệ. Vui lòng chọn số thứ tự hợp lệ.")
                except ValueError:
                    print("Lựa chọn không hợp lệ. Vui lòng chọn số thứ tự hợp lệ.")
            else:
                print("Không có tệp CSV nào trong thư mục.")
        else:
            print(f"Thư mục '{self.directory_path}' không tồn tại.")

        # Đọc dữ liệu từ tệp CSV đã chọn
        self.df = pd.read_csv(self.file_path)
        print('Độ lớn của bảng [frame] dữ liệu thời tiết:', self.df.shape)

        # Hiển thị số lượng dòng từ DataFrame
        while True:
            try:
                num_rows_to_display = int(input("Nhập số lượng dòng bạn muốn in ra từ DataFrame: "))
                print(self.df.head(num_rows_to_display))
                break
            except ValueError:
                print("Lựa chọn không hợp lệ. Vui lòng nhập một số nguyên.")

    def preprocessing(self):
        # Bước 3: Xử lý CỘT dữ liệu NULL quá nhiều OR không có giá trị phân tích
        print(self.df.count().sort_values())
        print("Danh sách các cột:")
        for i, column in enumerate(self.df.columns):
            print(f"{i}. {column}")

        # Chọn cột cần xóa
        columns_to_delete = []
        while True:
            try:
                column_index = int(input("Nhập số thứ tự của cột bạn muốn xóa (nhấn Enter để kết thúc): "))
                if 0 <= column_index < len(self.df.columns):
                    columns_to_delete.append(column_index)
                else:
                    print("Số thứ tự không hợp lệ. Vui lòng nhập số thứ tự hợp lệ hoặc nhấn Enter để kết thúc.")
            except ValueError:
                break

        # Xóa cột đã chọn
        self.df = self.df.drop(self.df.columns[columns_to_delete], axis=1)
        print(self.df.shape)

        # Bước 4: Xử lý DÒNG dữ liệu NULL
        self.df = self.df.dropna(how='any')
        print(self.df.shape)

        # Bước 5: Xử lý loại bỏ các giá trị ngoại lệ
        # Tính toán Z-Score
        z = np.abs(stats.zscore(self.df[['Postal Code', 'Electric Range', 'Base MSRP', 'DOL Vehicle ID', 'Census Tract']]))

        while True:
            try:
                threshold = float(input("Nhập ngưỡng giá trị Z-Score: "))
                break
            except ValueError:
                print("Vui lòng nhập một số thực hợp lệ.")

        print(f"Bạn đã chọn ngưỡng Z-Score là {threshold}")

        # Lọc dữ liệu dựa trên Z-Score
        self.df = self.df[(z < threshold).all(axis=1)]
        print(self.df.shape)

        # Bước 7: Chuẩn hóa tập dữ liệu Input dùng MinMaxScaler
        scaler = preprocessing.MinMaxScaler()
        selected_columns = ['Electric Range', 'Base MSRP', 'DOL Vehicle ID', 'Census Tract']
        scaler.fit(self.df[selected_columns])
        self.df[selected_columns] = scaler.transform(self.df[selected_columns])

        # In ra một số dòng của DataFrame đã xử lý
        print(self.df.head())

        # Bước 8: Xác định mô hình trích lọc các thuộc tính đặc trưng: EDA
        numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
        if 'Census Tract' in numeric_columns:
            numeric_columns = numeric_columns.drop('Census Tract')

        X = self.df.loc[:, numeric_columns]
        y = self.df['Census Tract']
        selector = SelectKBest(f_regression, k=3)
        selector.fit(X, y)
        X_new = selector.transform(X)
        print(X_new)
        print(pd.DataFrame(y))
        print(X.columns[selector.get_support(indices=True)])

        # Bước 9: Xác định mô hình trích lọc các thuộc tính đặc trưng
        # XĐ data frame = Chiếu lấy các thuộc tính đặc trưng đã xđ trong B8
        self.df = self.df[['Electric Range', 'Legislative District', 'DOL Vehicle ID', 'Census Tract']]

        # Bước 10: EDA theo nhu cầu thực tế => input vào các mô hình AI, ML,...
        # Đơn giản nhất là lấy 1 thuộc tính đầu vào (Electric Range) để XD Mô hình
        X = self.df[['Electric Range']]
        y = self.df[['Census Tract']]
        print(X)
        print(y)

if __name__ == "__main__":
    # Khởi tạo đối tượng DataPreprocessing
    data_processor = DataPreprocessing()

    data_processor.load_data()
    data_processor.preprocessing()
