import tkinter as tk
from tkinter import *
import csv
import numpy as np
import pickle
import pandas as pd
from tkintertable import TableCanvas, TableModel


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
				print(opt)
				tmp2 = database[x]  # 找出該科系可抵通識的領域
				print(tmp2)
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
		self.search.geometry("500x500")

		self.ybar = Scrollbar(self.search)
		self.ybar.pack(side = RIGHT, fill = Y)

		self.xbar = Scrollbar(self.search, orient = tk.HORIZONTAL)
		self.xbar.pack(side = BOTTOM, fill = X)

		self.listbox1 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)
		self.listbox2 = Listbox(self.search, yscrollcommand = self.ybar.set, xscrollcommand = self.xbar.set)

		for i in range(len(view)):
			self.listbox1.insert(END, view[i][0])
			self.listbox2.insert(END, view[i][1])

		print(view[1])
	
		self.listbox1.pack(side = LEFT, fill = BOTH)
		self.listbox2.pack(side = LEFT, fill = BOTH)

		self.ybar.config(command = self.listbox1.yview)
		self.ybar.config(command = self.listbox2.yview)

		self.search.mainloop()




def construct_gui():
    window = tk.Tk()
    window.title("通識小幫手")
    window.geometry("500x500")

    # global variable
    l = tk.Label(
        window,
        text="系級",  # 标签的文字
        bg="white",  # 背景颜色
        font=("Arial", 12),  # 字体和字体大小
        width=15,
        height=2,  # 标签长宽
    )
    l.pack()  # 固定窗口位置

    variable = StringVar(window)
    # variable.set('one')
    # opt.remove(opt[0])
    w = OptionMenu(window, variable, *opt)
    w.pack()
    l2 = tk.Label(
        window,
        text="如何排序",  # 标签的文字
        bg="white",  # 背景颜色
        font=("Arial", 12),  # 字体和字体大小
        width=15,
        height=2,  # 标签长宽
    )
    l2.pack()
    variable2 = StringVar(window)
    w2 = OptionMenu(window, variable2, *sort_ls)
    w2.pack()

    def f():
        view.clear()
        tmp = variable.get()
        tmp3 = variable2.get()
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

        print(view[0], view[1])

        open_search()

    button = Button(window, text = "OK", command = f)
    button.pack()

    # tframe = Frame()
    # tframe.pack()
    # table = TableCanvas(tframe)
    # table.importCSV("database.csv", sep = ',')
    # table.show()

    window.mainloop()

def open_search():

	search = tk.Tk()
	search.title("結果")
	search.geometry("500x500")

	ybar = Scrollbar(search)
	ybar.pack(side = RIGHT, fill = Y)

	xbar = Scrollbar(search, orient = tk.HORIZONTAL)
	xbar.pack(side = BOTTOM, fill = X)

	listbox1 = Listbox(search, yscrollcommand = ybar.set, xscrollcommand = xbar.set)
	listbox2 = Listbox(search, yscrollcommand = ybar.set, xscrollcommand = xbar.set)

	for i in range(len(view)):
		listbox1.insert(END, view[i][0])
		listbox2.insert(END, view[i][1])

	print(view[1])
	
	listbox1.pack(side = LEFT, fill = BOTH)
	listbox2.pack(side = LEFT, fill = BOTH)

	ybar.config(command = listbox1.yview)
	ybar.config(command = listbox2.yview)

	search.mainloop()
	


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
	app.mainloop()

