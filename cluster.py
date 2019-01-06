import os

import numpy as np
import matplotlib.pyplot as plt

MAX = 1000000


def nearest_neighbor(index):
    min_dist = MAX
    neighbor = -1
    for i in range(length):
        if dist[index, i] < min_dist and rho[index] < rho[i]:
            min_dist = dist[index, i]
            neighbor = i
    if result[neighbor] == -1:
        result[neighbor] = result[nearest_neighbor(neighbor)]
    return neighbor


# ----------------------------------------读取数据-----------------------------------------
fileName = input("Enter the file's name: ")
if not os.path.exists("Figure"):
    os.mkdir("Figure")
fileLoc = "Figure/" + fileName.split('.')[0]
if not os.path.exists(fileLoc):
    os.mkdir(fileLoc)

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
dist_list = []
first = 0
while first < length - 1:
    second = first + 1
    while second < length:
        distance = np.linalg.norm(location[first] - location[second])
        dist[first][second] = dist[second][first] = distance
        dist_list.append(distance)
        second = second + 1
    first = first + 1

dc = sorted(dist_list)[int(len(dist_list) * 0.02)]

# ---------------------------------------计算局部密度：ρ----------------------------------------
rho = np.zeros((length, 1))
first = 0
while first < length - 1:
    second = first + 1
    while second < length:
        # 采用高斯核函数
        rho[first] += np.exp(-(dist[first][second] / dc) ** 2)
        rho[second] += np.exp(-(dist[first][second] / dc) ** 2)
        # 采用截断核函数
        # if dist[first][second] < dc:
        #    rho[first] = rho[first] + 1
        #    rho[second] = rho[second] + 1
        second = second + 1
    first = first + 1

rmin, rmax = min(rho), max(rho)
rho = (rho - rmin) / (rmax - rmin)

# ------------------------------求与高密度点的最小距离：δ-----------------------------
delta = np.ones((length, 1)) * MAX
maxRho = np.max(rho)
first = 0
while first < length:
    if rho[first] < maxRho:
        second = 0
        while second < length:
            if rho[second] > rho[first] and dist[first][second] < delta[first]:
                delta[first] = dist[first][second]
            second = second + 1
    else:
        delta[first] = 0.0
        second = 0
        while second < length:
            if dist[first][second] > delta[first]:
                delta[first] = dist[first][second]
            second = second + 1
    first = first + 1

dmin, dmax = min(delta), max(delta)
delta = (delta - dmin) / (dmax - dmin)

# ------------------------------用ρ和δ的乘积γ作为阈值----------------------------
gama = np.zeros((length, 1))
for i in range(length):
    gama[i] = rho[i] * delta[i]

sortedGama = sorted(gama)
halfGama = sortedGama[:int(length * 0.95)]
avgGama = np.average(halfGama)
stdGama = np.std(halfGama)
thGama = min(avgGama + 25 * stdGama, max(gama))

# ------------------------------------用ρ和δ分别作为阈值------------------------------------
thRho = 0.2 * (np.max(rho) - np.min(rho)) + np.min(rho)
thDel = 0.2 * (np.max(delta) - np.min(delta)) + np.min(delta)

# -------------------------------------确定聚类中心------------------------------------
result = np.ones(length, dtype=np.int) * (-1)
centers = []
no = 0
for i in range(length):
    # if rho[i] > thRho and delta[i] > thDel:
    if rho[i] * delta[i] >= thGama:
        result[i] = no
        centers.append(i)
        no = no + 1

# -------------------------------------为每个点聚类------------------------------------
for i in range(length):
    dist[i][i] = MAX

for i in range(length):
    if result[i] == -1:
        result[i] = result[nearest_neighbor(i)]
    else:
        continue

colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
          '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

# -------------------------------------绘制决策图------------------------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title("决策图")
#plt.plot(rho, delta, '.')
for i in range(length):
    plt.plot(rho[i], delta[i], 'g', marker='.')

for i in centers:
    plt.plot(rho[i], delta[i], 'k', marker='o', markersize=5)
plt.xlabel('ρ'), plt.ylabel('δ')
plt.savefig(fileLoc + "/决策图.png")
plt.show()

# -------------------------------------γ------------------------------------
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title("γ分步图")

for i in range(length):
    plt.plot(i, gama[i], 'g', marker='.')

for i in centers:
    plt.plot(i, gama[i], 'k', marker='o', markersize=5)
plt.xlabel('n'), plt.ylabel('γ')
plt.savefig(fileLoc + "/γ.png")
plt.show()

# -------------------------------------绘制聚类的聚类结果------------------------------------
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title("聚类结果图")

for i in range(length):
    index = result[i]
    plt.plot(location[i][0], location[i][1], color=colors[(3 * index) % 10], marker='.')

for i in centers:
    plt.plot(location[i][0], location[i][1], 'k', marker='o', markersize=5)
plt.xlabel('x'), plt.ylabel('y')
plt.savefig(fileLoc + "/聚类结果图.png")
plt.show()

# -------------------------------------绘制原聚类结果------------------------------------
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title("实际类别图")

for i in range(length):
    index = label[i]
    plt.plot(location[i][0], location[i][1], color=colors[(3 * index) % 10], marker='.')
plt.xlabel('x'), plt.ylabel('y')
plt.savefig(fileLoc + "/实际类别图.png")
plt.show()
