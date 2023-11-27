import pandas as pd
import tkinter as tk
from tkinter import ttk


class StudentPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance App")
        
        # Thêm dòng text
        title_label = tk.Label(self.root, text="Student Performance Data", font=("Helvetica", 16), pady=10, bg="#0074ce")
        title_label.pack()

        # Tạo Frame chứa Canvas để bao gồm Treeview và thanh cuộn
        self.canvas_frame = tk.Frame(self.root, bg='blue')
        self.canvas_frame.pack(side=tk.LEFT, padx=15, pady=15)

        # Tăng kích thước của Canvas (chiều rộng và chiều cao)
        self.canvas_width = 1000
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

        # Tạo thanh cuộn ngang cho Canvas
        xsb = ttk.Scrollbar(self.canvas_frame, orient='horizontal', command=self.canvas.xview)
        xsb.pack(side=tk.BOTTOM, fill='x')
        self.canvas.configure(xscrollcommand=xsb.set)

        # Tạo Frame chứa Treeview
        self.tree_frame = tk.Frame(self.canvas, bg='blue')
        self.canvas.create_window((10, 10), window=self.tree_frame, anchor=tk.NW)

        # Tạo Treeview để hiển thị dữ liệu
        columns = list(df_BD_09.columns)
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        # Thêm tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Hiển thị dữ liệu từ DataFrame lên Treeview
        for i, row in df_BD_09.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Pack Treeview vào Frame
        self.tree.pack(side=tk.LEFT)

        # Thêm sự kiện để cập nhật kích thước Canvas khi Treeview thay đổi
        self.tree.bind("<Configure>", self.on_treeview_configure)

        #relx: ngang, càng lớn càng qua phải
        #rely: dọc càng lớn càng xuống dưới
        # Tạo Frame chứa nút Refresh
        refresh_frame = ttk.Frame(self.root)
        refresh_frame.place(relx=0.1, rely=0.75, anchor="s")
        refresh_frame.configure(borderwidth=15)
        
        # Tạo nút Refresh để làm mới dữ liệu
        refresh_button = ttk.Button(refresh_frame, text="Refresh", command=self.refresh_data)
        refresh_button.pack(side=tk.TOP, padx=5)
        
        # Tạo Frame chứa nút Exit
        exit_frame = ttk.Frame(self.root)
        exit_frame.place(relx=0.9, rely=0.75, anchor="s")
        exit_frame.configure(borderwidth=15)
        
        
        gray_button = tk.Button(exit_frame, text="Trắng Đen",command=self.root.destroy, fg="blue", bg="white")
        gray_button.pack(side='left', padx=3, pady=3)


        # Thiết lập kích thước cửa sổ mặc định
        self.root.geometry("1000x500")  # Thay đổi kích thước tùy ý

    def on_treeview_configure(self, event):
        # Cập nhật kích thước Canvas khi Treeview thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def refresh_data(self):
        # Làm mới dữ liệu từ DataFrame và cập nhật lại Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, row in df_BD_09.iterrows():
            self.tree.insert("", "end", values=list(row))
            


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background='#0074ce')
    app = StudentPerformanceApp(root)
    root.mainloop()