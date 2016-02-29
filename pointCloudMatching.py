__author__ = 'Holliday'
import time, csv, copy
from pcr_minDist import minDist
from registration import registration, R as createR
from getDK import getDk
import numpy as np

def readData(filename):
    start = time.clock()
    csvfile = open(filename, 'rb')
    dat = csv.reader(csvfile, delimiter=' ')
    pointCloud = []
    for i, row in enumerate(dat):
        pointCloud.append([float(row[0]), float(row[1]), float(row[2])])

    print time.clock() - start
    return np.array(pointCloud)

if __name__ == '__main__':
    threshold = 100
    cloud1 = readData("pointcloud1.fuse")
    cloud2 = readData("pointcloud2.fuse")
    # yk = minDist(cloud1, cloud2)
    pk = copy.copy(cloud1)

    # get the error of the first two iterations to use in the while loop condition
    # yk = minDist(pk, cloud2)
    qr, qt = registration(cloud1, cloud2)
    dk1 = getDk(qr, qt, pk, cloud2)
    pk = np.add(np.mat(cloud1) * np.mat(createR(qr.transpose())), qt.transpose())

    yk = minDist(pk, cloud2)
    qr, qt = registration(cloud1, yk)
    dk2 = getDk(qr, qt, pk, yk)
    pk = np.add(np.multiply(cloud1, createR(qr)), qt)


    while dk1 - dk2 > threshold:
        dk1 = dk2
        yk = minDist(pk, cloud2)
        qr, qt = registration(cloud1, yk)
        dk2 = getDk(qr, qt, pk, yk)
        pk = np.add(np.multiply(cloud1, createR(qr)), qt)

    print np.concatenate(qr, qt)