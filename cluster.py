# encoding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import random

MAX = 1000000


def nearest_neighbor(index):
    distance = MAX
    neighbor = -1
    for i in range(length):
        if dist[index, i] < distance and rho[index] < rho[i]:
            distance = dist[index, i]
            neighbor = i
    if result[neighbor] == -1:
        result[neighbor] = nearest_neighbor(neighbor)
    return result[neighbor]


# ----------------------------------------读取数据-----------------------------------------
fileName = raw_input("Enter the file's name: ")
location = []
label = []
for line in open(fileName, "r"):
    items = line.strip("\n").split(",")
    label.append(int(items.pop()))
    tmp = []
    for item in items:
        tmp.append(float(item))
    location.append(tmp)
location = np.array(location)
label = np.array(label)
length = len(location)

# ----------------------------------------计算距离-----------------------------------------
dist = np.zeros((length, length))
ll = []
begin = 0
while begin < length-1:
    end = begin + 1
    while end < length:
        distance = np.linalg.norm(location[begin]-location[end])
        dist[begin][end] = distance
        dist[end][begin] = distance
        ll.append(distance)
        end = end + 1
    begin = begin + 1
ll = np.array(ll)

# Algorithm
# percent = float(raw_input("Enter the average percentage of neighbours: "))
percent = 2.0
position = int(len(ll) * percent / 100)
sortedll = np.sort(ll)
dc = sortedll[position]

# ---------------------------------------计算局部密度：ρ----------------------------------------
rho = np.zeros((length, 1))
begin = 0
while begin < length-1:
    end = begin + 1
    while end < length:
        # 采用高斯核函数
        rho[begin] = rho[begin] + np.exp(-(dist[begin][end] / dc) ** 2)
        rho[end] = rho[end] + np.exp(-(dist[begin][end]/dc) ** 2)
        # 采用截断核函数
        # if dist[begin][end] < dc:
        #    rho[begin] = rho[begin] + 1
        #    rho[end] = rho[end] + 1
        end = end + 1
    begin = begin + 1

# ------------------------------求比点的局部密度大的点到该点的最小距离：δ----------------------------

delta = np.ones((length, 1)) * MAX
maxDensity = np.max(rho)
begin = 0
while begin < length:
    if rho[begin] < maxDensity:
        end = 0
        while end < length:
            if rho[end] > rho[begin] and dist[begin][end] < delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    else:
        delta[begin] = 0.0
        end = 0
        while end < length:
            if dist[begin][end] > delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    begin = begin + 1

rate1 = 0.6
#Aggregation Spiral 0.6
#Jain Flame 0.8
#D31 0.75
#R15 0.6
#Compound 0.5
#Pathbased 0.2
thRho = rate1 * (np.max(rho) - np.min(rho)) + np.min(rho)

rate2 = 0.2
#Aggregation Spiral 0.2
#Jain Flame 0.2
#D31 0.05
#R15 0.1
#Compound 0.08
#Pathbased 0.4
thDel = rate2 * (np.max(delta) - np.min(delta)) + np.min(delta)

#确定聚类中心
result = np.ones(length, dtype=np.int) * (-1)
center = 0
#items = range(length)
#random.shuffle(items)
for i in range(length): #items:
    if rho[i] > thRho and delta[i] > thDel:
        result[i] = center
        center = center + 1
#赋予每个点聚类类标
for i in range(length):
    dist[i][i] = MAX

for i in range(length):
    if result[i] == -1:
        result[i] = nearest_neighbor(i)
    else:
        continue

plt.plot(rho, delta, '.')
plt.xlabel('rho'), plt.ylabel('delta')
plt.show()

R = range(256)
random.shuffle(R)
R = np.array(R)/255.0
G = range(256)
random.shuffle(G)
G = np.array(G)/255.0
B = range(256)
random.shuffle(B)
B = np.array(B)/255.0
colors = []
for i in range(256):
    colors.append((R[i], G[i], B[i]))

plt.figure()
for i in range(length):
    index = result[i]
    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
plt.xlabel('x'), plt.ylabel('y')
plt.show()

plt.figure()
for i in range(length):
    index = label[i]
    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
plt.xlabel('x'), plt.ylabel('y')
plt.show()
