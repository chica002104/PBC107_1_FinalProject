import numpy as np
import pickle
data = []  
for x in range(1,9):
	fname = 'a' + str(x)+'.txt'
	f = open(fname,'r')
	a = f.readlines()
	a = a[379:]
	data.append([])
	for y in a:
		if 'align="center' in y:
			y = y.split('>')
			y = y[11:]
			for z in range(7):
				y.remove(y[1])
			for z in range(len(y)):
				y[z] = y[z].split('<')[0]
			new = []
			for z in y:
				if (len(z) >= 2)& ('nbsp' not in z) & ('加入' not in z):
					new.append(z)
			data[x - 1].append(new)
for x in range(8):
	del data[x][0] # 把第一列刪除
	for y in range(len(data[x])):	
		data[x][y].insert(0, "A" + str(x + 1))
	print(len(data[x]))
	print(data[x])
file = open('lecture.pickle', 'wb')
pickle.dump(data, file)
file.close()