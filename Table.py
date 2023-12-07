import tkinter as tk
from tkinter import ttk

#class bảng
class Table:
    def __init__(self, root):
        self.tree = None
        self.create_treeview(root)
    # Tạo treeview mới sử dụng widget treeview
    def create_treeview(self, root):
        style = ttk.Style(root)
        style.configure("Treeview.Heading", font=('Time New Roman', 18))  # Đặt font cho tiêu đề cột
        style.configure("Treeview", font=('Time New Roman', 15), rowheight=30)  # Đặt font cho các hàng
        self.tree = ttk.Treeview(root, show='headings', height=6)
        self.tree['columns'] = []
    # Gán tiêu đề các cột
    def setHeader(self, header):
        self.tree['columns'] = header
        for head in header:
            self.tree.heading(head, text=head, anchor=tk.CENTER)
            self.tree.column(head, anchor=tk.CENTER, width=200)
    # Thêm hàng mới vào treeview
    def addRow(self, row):
        if not self.tree['columns']:
            self.setHeader(list(row.keys()))
        self.tree.insert('', 'end', values=list(row.values()))
    #Thêm nội dung vào
    def addData(self, data):
        for row in data:
            self.addRow(row)
    # Hiển thị bảng lên giao diện
    def display(self):
        self.tree.pack(padx=10, pady=10)
