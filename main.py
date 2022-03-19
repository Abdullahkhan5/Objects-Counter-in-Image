import numpy as np
import cv2

#Image Part
imageMatrix = cv2.imread('Pattern2.jpeg',0)

newMatrix = np.full((imageMatrix.shape[0]+2,imageMatrix.shape[1]+2),0,np.uint8)

for i in range(newMatrix.shape[0]-2):
    for j in range(newMatrix.shape[1]-2):
        newMatrix[i+1,j+1] = imageMatrix[i,j]

#Defining threshold
for i in range(1,newMatrix.shape[0]-1):
    for j in range(1,newMatrix.shape[1]-1):
        if newMatrix[i,j] > 127:
            newMatrix[i,j] = 255
        else:
            newMatrix[i,j] = 0

label = 0
obj = 0
pos = 0
eq_list = []
newlist = []

label_matrix = np.zeros((newMatrix.shape[0],newMatrix.shape[1]),dtype=int)

#Making Label Matrix
for i in range(1, newMatrix.shape[0]-1):
    for j in range(1, newMatrix.shape[1]-1):
        if newMatrix[i, j] == 255:
            count = 0
            list = []
            if newMatrix[i, j - 1] != 255 and newMatrix[i - 1, j - 1] != 255 and newMatrix[i - 1, j] != 255 and newMatrix[i - 1, j + 1] != 255:
                label += 1
                label_matrix[i, j] = label
                eq_list.append([label,label])
            if newMatrix[i, j - 1] == 255:
                pos = 1
                count += 1
                list.append(label_matrix[i, j - 1])
            if newMatrix[i - 1, j - 1] == 255:
                pos = 2
                count += 1
                list.append(label_matrix[i - 1, j - 1])
            if newMatrix[i - 1, j] == 255:
                pos = 3
                count += 1
                list.append(label_matrix[i - 1, j])
            if newMatrix[i - 1, j + 1] == 255:
                pos = 4
                count += 1
                list.append(label_matrix[i - 1, j + 1])
            if pos == 1 and count == 1:
                label_matrix[i, j] = label_matrix[i, j - 1]
            if pos == 2 and count == 1:
                label_matrix[i, j] = label_matrix[i - 1, j - 1]
            if pos == 3 and count == 1:
                label_matrix[i, j] = label_matrix[i - 1, j]
            if pos == 4 and count == 1:
                label_matrix[i, j] = label_matrix[i - 1, j + 1]
            if count > 1:
                minimum = min(list)
                for k in range(len(list)):
                    if minimum == list[k]:
                        label_matrix[i,j] = minimum
                    else:
                        label_matrix[i,j] = min(list)
                        #Updating Equivalency list
                        for l in range(len(eq_list)):
                            if eq_list[l][1] > min(list) and eq_list[l][1] in list:
                                eq_list[l][1] = min(list)

#Updating Label Matrix
for i in range(1,label_matrix.shape[0]-1):
    for j in range(1,label_matrix.shape[1]-1):
        for k in range(len(eq_list)):
            if label_matrix[i,j] == eq_list[k][0]:
                label_matrix[i,j] = eq_list[k][1]

#Updating no of Objects
for i in range(1,label_matrix.shape[0]-1):
    for j in range(1,label_matrix.shape[1]-1):
        if label_matrix[i,j] != 0 and label_matrix[i,j] not in newlist:
            minimum = label_matrix[i,j]
            newlist.append(minimum)
            obj += 1


print(obj)
np.set_printoptions(threshold=np.inf)
print(label_matrix)
