import tkinter as tk
from tkinter import *
import csv
import numpy as np
import pickle
import pandas as pd
# from tkintertable import TableCanvas, TableModel


dept = []
opt = []
view = []


def take(x):
    if len(x) >= 6:
        try:
            x[5] = int(x[5])
            print("5")
            return x[5]
        except ValueError:
            return 0
    else:
        return 0


sort_ls = ["依選課上限人數排序", "依領域排序"]

class Home(tk.Frame):


	def __init__(self):
		tk.Frame.__init__(self)
		self.grid()
		self.createWidgets()
		# self.title("通識小幫手")
		# self.geometry("500x500")

	def createWidgets(self):
		# global variable
		self.l = tk.Label(self, text="系級", bg="white", font=("Arial", 12), width=15, height=2)
		#self.l.pack()  # 固定窗口位置

		self.variable = StringVar(self)
    # variable.set('one')
    # opt.remove(opt[0])
		self.w = OptionMenu(self, self.variable, *opt)
		# self.w.pack()
		self.l2 = tk.Label(self, text="如何排序", bg="white", font=("Arial", 12), width=15, height=2)
		# self.l2.pack()
		self.variable2 = StringVar(self)
		self.w2 = OptionMenu(self, self.variable2, *sort_ls)
		# self.w2.pack()

		self.button = Button(self, text = "OK", command = self.search)	
		# self.button.pack()

		self.l.grid(row = 0, column = 0)
		self.w.grid(row = 1, column = 0)
		self.l2.grid(row = 2, column = 0)
		self.w2.grid(row = 3, column = 0)
		self.button.grid(row = 4, column = 0)


	def search(self):
		view.clear()
		tmp = self.variable.get()
		tmp3 = self.variable2.get()
		choose = []

		for x in range(len(opt)):
			if tmp == opt[x]:
				# print(opt)
				tmp2 = database[x]  # 找出該科系可抵通識的領域
				# print(tmp2)
		for x in range(len(tmp2)):
			if tmp2[x] == 1:
				choose.append(x)  # 新增到另一個list
                # print(choose)
			
		for x in range(len(choose)):
			tmp = choose[x]
			for y in lecture[tmp]:
				view.append(y)
                # print(view) # 所有可以修的通識課
			if tmp3 == "依選課上限人數排序":
				view.sort(key=take, reverse=True)
        #print(view[0], view[1])	

		Search()


class Search:

    def __init__(self):
        self.search = tk.Tk()
        self.search.title("結果")
        self.search.geometry("1400x500")

        self.ybar = Scrollbar(self.search, command = self.OnVsb)
        self.ybar.pack(side = RIGHT, fill = Y)

        self.xbar = Scrollbar(self.search, orient = tk.HORIZONTAL)
        self.xbar.pack(side = BOTTOM, fill = X)

        self.listbox1 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox2 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox3 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox4 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox5 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox6 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        self.listbox7 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
        # self.listbox8 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)

        for i in range(len(view)):
            self.listbox1.insert(END, view[i][0])
            self.listbox2.insert(END, view[i][1])
            self.listbox3.insert(END, view[i][2])
            self.listbox4.insert(END, view[i][3])
            self.listbox5.insert(END, view[i][4])
            self.listbox6.insert(END, view[i][5])
            self.listbox7.insert(END, view[i][6])
            # self.listbox8.insert(END, view[i][7])

        # print(view[1])

        self.listbox1.pack(side = LEFT, fill = BOTH)
        self.listbox2.pack(side = LEFT, fill = BOTH)
        self.listbox3.pack(side = LEFT, fill = BOTH)
        self.listbox4.pack(side = LEFT, fill = BOTH)
        self.listbox5.pack(side = LEFT, fill = BOTH)
        self.listbox6.pack(side = LEFT, fill = BOTH)
        self.listbox7.pack(side = LEFT, fill = BOTH)
        # self.listbox8.pack(side = LEFT, fill = BOTH)

        self.listbox1.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox2.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox3.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox4.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox5.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox6.bind("<MouseWheel>", self.OnMouseWheel)
        self.listbox7.bind("<MouseWheel>", self.OnMouseWheel)
        # self.listbox8.bind("<MouseWheel>", self.OnMouseWheel)

        self.search.mainloop()

    def OnVsb(self, *args):
        self.listbox1.yview(*args)
        self.listbox2.yview(*args)
        self.listbox3.yview(*args)
        self.listbox4.yview(*args)
        self.listbox5.yview(*args)
        self.listbox6.yview(*args)
        self.listbox7.yview(*args)

        # self.listbox8.yview(*args)

    def OnMouseWheel(self, event):
        self.listbox1.yview("scroll", event.delta, "units")
        self.listbox2.yview("scroll", event.delta, "units")
        self.listbox3.yview("scroll", event.delta, "units")
        self.listbox4.yview("scroll", event.delta, "units")
        self.listbox5.yview("scroll", event.delta, "units")
        self.listbox6.yview("scroll", event.delta, "units")
        self.listbox7.yview("scroll", event.delta, "units")
        
        # self.listbox8.yview("scroll", event.delta, "units")
        return "break"


def read_dept():
    # 開啟 CSV 檔案

    with open("database.csv", newline="") as csvfile:

        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)

        # 以迴圈輸出每一列
        for row in rows:
            row = list(row)
            dept.append(row)
            opt.append(row[0])

    global database
    database = np.zeros((len(opt), 8))

    for x in range(len(dept)):
        # print(dept[x])
        for y in range(1, 9):
            # print(dept[x][y])
            if dept[x][y] == "T":
                database[x][y - 1] = 1
    global lecture
    with open("lecture.pickle", "rb") as file:
        lecture = pickle.load(file)
        #print(lecture)


if __name__ == "__main__":
    read_dept()
    app = Home()
    app.master.title("智慧通識小幫手")
    app.master.minsize(width = 100, height = 100)
    app.mainloop()

