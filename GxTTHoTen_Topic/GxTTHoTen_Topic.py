# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 19:59:48 2022

@author: VOXUAN
"""

# B1: NẠP THƯ VIỆN
    # Speech
import speech_recognition as sr02vtth
from gtts import gTTS
import playsound

    # tkinter
import tkinter as tk02vtth
from tkinter import messagebox

    # thư viện OS (lập thư mục, files)
import os  # THƯ VIỆN OS MS. WINDOWS = Lập thư mục & lưu file

   # Nạp các thư viện cần thiết EDA
import numpy as np #Numeric Python: Thư viện về Đại số tuyến tính tính
import pandas as pd #Python Analytic on Data System: For data processing (Thư viện xử lý dữ liệu)
from scipy import stats # thư viện cung cấp các công cụ thống kê [statistics] sub-lib của science python [các công cụ khoa học] 
from sklearn import preprocessing # Thư viện tiền xử lý DL (XL ngoại lệ: Isolated)
from sklearn.feature_selection import SelectKBest, chi2 # Nạp hàm Thư viện phân tích dữ liệu thăm dò

# B2: KHAI BÁO TÊN THƯ MỤC & FILE LƯU CÁC THÔNG TIN BÀI LÀM
vtth02_FILE = "vtth020.mp3"  # lưu tên  file Input
vtth02_DIR = 'vtth02'     # Thư mục lưu các file [trên]

os.makedirs(vtth02_DIR, exist_ok=True) # TẠO THƯ MỤC LƯU (từ thư viện os - của OS MS. Windows))

"""
CÁC HÀM THỰC HIỆN CÁC CHỨC NĂNG: HỆ THỐNG 
"""
def Thoat():
  traloi = messagebox.askquestion("Xác nhận","Thiệt thoát không (Y/N)?")
  if traloi == "yes": wn.destroy()

"""
CÁC HÀM THỰC HIỆN CÁC CHỨC NĂNG = SPEECH
"""

def Lenh(): # NHẬP ÂM THANH TỪ MICROPHONE
 r = sr02vtth.Recognizer()
 with sr02vtth.Microphone() as Source:
  #hiệu chỉnh mic để chuẩn bị nói
  messagebox.showinfo("Nhắc nhở", "Hieu chinh nhieu trươc khi noi!")
  r.adjust_for_ambient_noise(Source, duration=1)
  #nhận lời nói ra lệnh từ người dùng thông qua MIc [mặc định] lưu dữ liệu âm thanh vào audio_data
  messagebox.showinfo("Cảnh báo", "Bấm OK để bắt đầu Chọn lệnh bằng tiếng Việt, trong 3s" )
  audio_data = r.record(Source, duration = 3)
  try:
   vlenh = r.recognize_google(audio_data,language="vi")
  except: 
   vlenh = "Quý vị nói gì nghe không rõ...!"
  # xuất kết quả ra  
  messagebox.showinfo("Quý vị đã nói là", format(vlenh)) 
  vText = gTTS(text=vlenh, lang = 'vi')
  #vFile = '06VXT.mp3'
  vText.save(vtth02_FILE)
  playsound.playsound(vtth02_FILE)    

"""
CÁC HÀM THỰC HIỆN CÁC CHỨC NĂNG = EDA
"""

def EDA():
 df = pd.read_csv('./GxttHoTen_Topic.csv')
 # Display the shape of the data set (xem lượng dòng & cột dữ liệu của tập DL gốc)
 messagebox.showinfo("Độ lớn của bảng [frame] dữ liệu thời tiết", df.shape) 

""""""""""""""""""""""""""""""""""""""""""""
""" CÁC NỘI DUNG SAU CHƯA THỰC HIỆN 
""""""""""""""""""""""""""""""""""""""""""
# Bước 3: Xử lý CỘT dữ liệu NULL quá nhiều OR không có giá trị phân tích
# Checking for null values (Kiểm tra giá trị null = đếm số dòng có dữ liệu ứng từng thuộc# tính)
 messagebox.showinfo("CÁC CỘT DỬ LIỆU SẮP XẾP THEO THỨ TỰ CÓ DỮ LIỆU TỪ ÍT => NHIỀU",df.count().sort_values()) #df.count(): đếm số lượng dòng có dữ liệu của df, .sort_values() sx tăng dân
 df = df.drop(columns=['Sunshine','Evaporation','Cloud3pm','Cloud9am','Location','Date','RISK_MM'],axis=1)
 #df = df.drop(columns=['Sunshine','Evaporation','Cloud3pm','Cloud9am','Pressure9am',# 'Pressure3pm','WindDir3pm', 'WindDir9am', 'WindGustDir',# 'WindGustSpeed','Location','Date','RISK_MM'],axis=1)
 messagebox.showinfo("Độ lớn của bảng [frame] dữ liệu SAU KHI XỬ LÝ CỘT NULL", df.shape) # kiểm tra lại số lượng cột & dòng của df sau khi XL NULL cột
# Bước 4: Xử lý DÒNG dữ liệu NULL 
# Removing null values (Xóa tất cả các dòng có giá trị null trong tập FRAME dữ liệu.)
 df = df.dropna(how='any')
 messagebox.showinfo("Độ lớn của bảng [frame] dữ liệu SAU KHI XỬ LÝ DÒNG NULL", df.shape) # kiểm tra lại số lượng cột & dòng của df sau khi XL NULL các dòng DL

# Bước 5: Xử lý loại bỏ các giá trị ngoại lệ (cá biệt): isolated
#kiểm tra tập dữ liệu có bất kỳ ngoại lệ nào không
 z = np.abs(stats.zscore(df._get_numeric_data())) # Dò tìm và lấy các giá trị cá biệt trong tập dữ liệu gốc thông qua điểm z (z_score)
 messagebox.showinfo("MA TRAN Z-SCORE", z) # in ra tập (ma trận) các giá trị z-score từ tập dữ liệu gốc
 df= df[(z < 3).all(axis=1)] # kiểm tra và chỉ giữ lại trong df các giá trị số liệu tưng ứng với z-score < 3  # {loại các giá trị >= 3} vì các giá trị z-score >=3 tướng ứng với số liệu quá khác biệt so với các số liệu còn lại (“cá biệt” = “ngoại lệ” = isolated}
 messagebox.showinfo("Độ lớn của bảng [frame] dữ liệu SAU KHI XỬ LÝ NGOẠI LỆ", df.shape)# xác định số dòng & cột dữ liệu sau khu xử lý các giá trị cá biệt

 # Bước 6: Thay thế các vị trí giá trị  0 và 1 bởi CÓ (Yes) và KHÔNG (No).
 #Thay thế yes (CÓ) and no (KO) vào vị trí giá trị 1 (Y) và 0 (N) tương ứng cột|biến RainToday và# RainTomorrow
 df['RainToday'].replace({'KHONG': 'No', 'CO': 'Yes'},inplace = True)
 df['RainTomorrow'].replace({'KHONG': 'No', 'CO': 'Yes'},inplace = True)
 #Bước 7: Chuẩn hóa (Rời rạc hóa) tập dữ liệu Input dùng ..MaxMin
#  # CHUẨN HÓA DL
#  scaler = preprocessing.MinMaxScaler() #preprocessing là Sub-Library của thư viện sklearn=> hàm .MinMaxScaler() Rời rạc hóa tập dữ liệu Input
#  scaler.fit(df)
#  df = pd.DataFrame(scaler.transform(df), index=df.index, columns=df.columns)                    # Rời rạc hóa số liệu theo thang đo scaler
#  df.iloc[4:10]
#  messagebox.showinfo("Độ lớn của bảng [frame] dữ liệu SAU KHI CHUẨN HÓA DL", df.shape)# xác định số dòng & cột dữ liệu sau khu xử lý các giá trị cá biệt

#  # GIAI ĐOẠN 3: PHÂN TÍCH DỮ LIỆU THĂM DÒ : EDA

# # Bước 8: Nạp các thuộc tính quan trọng vào Dataset
# #The important features are put in a data frame
#  df = df[['Humidity3pm','Rainfall','RainToday','RainTomorrow']]

# # Bước 9: thực hiện các tính toán trên mô hình phân tích
# #To simplify computations we will use only one feature (Humidity3pm) to build the model
#  X = df
#  X = df[['Humidity3pm']]
#  y = df[['RainTomorrow']]
#  X = df.loc[:,df.columns!='RainTomorrow']
#  y = df[['RainTomorrow']]
#  selector = SelectKBest(chi2, k=3)
#  selector.fit(X, y)
#  X_new = selector.transform(X)
#  df(['Rainfall', 'Humidity3pm', 'RainToday'], dtype='object')
#  messagebox.showinfo(" KÊT QUẢ", X.columns[selector.get_support(indices=True)])# xác định số dòng & cột dữ liệu sau khu xử lý các giá trị cá biệt
"""

"""
THỦ TỤC CHÍNH = GUI
"""
# B3: LẬP GUI (EX4)
  # Tạo một cửa sổ mới
wn = tk02vtth.Tk()

  #Thêm tiêu đề cho cửa sổ
wn.title("stt HỌ VÀ TÊN, LỚP_HCMUTE, ĐỒ ÁN HỌC PHẦN: LẬP TRÌNH PYTHON, T8.2022")
  #Đặt kích thước của cửa sổ
wn.geometry('800x600')
  #Không cho thay đổi size 
wn.resizable(tk02vtth.FALSE, tk02vtth.FALSE)

  #Tiêu đề Form = tên đề tài 
t = "stt HỌ VÀ TÊN, LỚP_HCMUTE, ĐỒ ÁN HỌC PHẦN: LẬP TRÌNH PYTHON: EDA Supermarket"
lblDT = tk02vtth.Label(wn, text=t, background = "yellow", fg = "blue", relief = tk02vtth.SUNKEN, font=("Arial Bold", 13), borderwidth = 3, width = 65, height = 3)
lblDT.place(x = 10, y = 10)

# B4: CÁC NÚT LỆNH: EX1 = Speech 
  #Thoát
btnThoat = tk02vtth.Button(wn, text = "Thoát", width = 10, command = Thoat)
btnThoat.place(x =100, y = 200)# căn cứ vào kích thước form [wn.geometry("800x600")] => canh vị trí Button "thoát"
  
  #Xử lý lời nói = speech = VOICE ASSISTANT
btnNoi = tk02vtth.Button(wn, text = "TRỢ LÝ ẢO ", width = 15, command = Lenh)
btnNoi.place(x = 200, y = 200)  


# B5: CÁC NÚT LỆNH: EX3 = EDA = DỰ PHÂN TÍCH DỮ LIỆU KHÁM PHÁ
btnEDA = tk02vtth.Button(wn, text = "EDA", width = 15, command = EDA)
btnEDA.place(x = 400, y = 200)  
 
#Lặp vô tận để hiển thị cửa sổ
wn.mainloop()