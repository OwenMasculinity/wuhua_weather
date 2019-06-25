import csv
import sys
import pymysql
import pandas as pd
import json
from  matplotlib import pyplot as plt

from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVR
# preprocessing function
from sklearn.preprocessing import StandardScaler
from numpy import *
import numpy as np

file = open(r'G:\2017年大学生科研\2015_Air_quality_in_northern_Taiwan.csv', 'r', newline='')
reader = csv.DictReader(file)
rainfall=[]  # 降雨量 m2
RH = []  # 相对湿度 %
WS_HR = []  # 平均风速 m/sec

for row in reader:
    if row["station"] == "Zhongshan":
        temp_rainfall = row["RAINFALL"].strip("#").strip("x")
        if temp_rainfall == "NR":
            temp_rainfall = 0.
        if temp_rainfall == "":
            temp_rainfall = 0.
        else:
            temp_rainfall = float(temp_rainfall)
        rainfall.append(temp_rainfall)

        temp_RH = row["RH"].strip("#").strip("x")
        if temp_RH == "NR":
            temp_RH = 0.
        if temp_RH == "":
            temp_RH = 0.
        else:
            temp_RH = float(temp_RH)
        RH.append(temp_RH)

        temp_WS_HR = row["WS_HR"].strip("#").strip("x")
        if temp_WS_HR == "NR":
            temp_WS_HR = 0.
        if temp_WS_HR == "":
            temp_WS_HR = 0.
        else:
            temp_WS_HR = float(temp_WS_HR)
        WS_HR.append(temp_WS_HR)

data=np.zeros([len(rainfall)-4,6])
label=np.zeros([len(rainfall)-4,1])

for i in range(len(rainfall)-4):
    data[i, 0] = rainfall[i]
    data[i, 1] = rainfall[i + 1]
    data[i, 2] = rainfall[i + 2]
    data[i, 3] = rainfall[i + 3]
    data[i, 4] = RH[i + 4]
    data[i, 5] = WS_HR[i + 4]
    label[i,0] = rainfall[i + 4]

# data1=[row for row in rainfall[:-4]]
# data1=np.array(data1)
# data2=[row for row in rainfall[1:-3]]
# data2=np.array(data2)
# data3=[row for row in rainfall[2:-2]]
# data3=np.array(data3)
# data4=[row for row in rainfall[3:-1]]
# data4=np.array(data4)
# data5=[row for row in RH[4:]]
# data5=np.array(data5)
# data6=[row for row in WS_HR[4:]]
# data6=np.array(data6)
#
# data = [data1,data2,data3,data4,data5, data6]
# label = [row for row in rainfall[4:]]

# data = np.array(data)
# label = np.array(label)

# house_dataset = datasets.load_boston()
# house_data = house_dataset.data
# house_price = house_dataset.target

x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.2)
# f(x) = (x - means) / standard deviation
scaler = StandardScaler()
scaler.fit(x_train)
# standardization
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)


# construct SVR model
svr = SVR(kernel = 'linear')
# svr = SVR(kernel = 'rbf')
# svr = SVR(kernel = 'poly')
# svr = SVR(kernel = 'sigmoid')
svr.fit(x_train, y_train)
y_predict = svr.predict(x_test)
y_predict = y_predict.reshape(1747,1)
# result = hstack((y_test.reshape(-1, 1), y_predict.reshape(-1, 1)))
# print(result)

error = mean(abs(y_test-y_predict)/(y_predict))
print(error)

fig = plt.figure(2)
plt.plot(y_test)
plt.plot(y_predict)
plt.xlabel("数据序号",fontproperties="SimHei",fontsize=15)
plt.ylabel("降雨量(单位：mm)",fontproperties="SimHei",fontsize=15)
plt.legend(["test", "predict"], loc="upper right")
plt.show()