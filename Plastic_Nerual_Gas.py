#!/usr/bin/env python


import numpy as np
import cv2
import operator


def LoadData(filename):
	dataMat = []
	infile = open(filename, 'r')
	for line in infile.readlines():
		curLine = line.strip().split('\t')
		fltLine = map(float,curLine)
		dataMat.append(fltLine)
	dataMat = np.mat(dataMat)
	return dataMat

def Initialization(dataSet,N):
	# dataSet must be a matrix not a list
	data_dim = dataSet.shape[1]	
	#Vector = np.mat(np.zeros((N,data_dim)))
	#Vector[0,:] = dataSet[0,:]
	Vector = []
	Vector.append(dataSet[0,:])
	#initialization of activation
	Activation = []
	for i in range(N):
		Activation.append(0)
	# A1 = 1
	Activation[0] = 1
	
	#initialization of Z
	Z = []
	Z.append(0)
	return Vector, Activation,Z

def Distance(VecA, VecB):
	return np.sqrt((np.power(VecA - VecB, 2)).sum())

def loop_neural_gas(Vector,Activation,Z,dataSet,N):
	
	Kn_List = []
	Vector_before = Vector
	#initialization of decreasing learning factor
	dec_learn_factor = []
	for j in range(len(dataSet)):
		dec_learn_factor.append(0)

	# initialization of lena
	Lena = []
	for k in range(len(dataSet)):
		Lena.append(0)

	dis_List = []
	
	#for i in range(1,dataSet.shape[0]): # we begin with 1 because we have i-1
	for i in range(1,5): # we begin with 1 because we have i-1
		x = dataSet[i,:]
		Kn_List = []
		dis_List = []
		index = 0
		Vector_before = Vector
		for v in Vector:
			dis = Distance(x,v)
			Kn_List.append((index,dis))
			dis_List.append(dis)
			index+=1
		Kn_List = sorted(Kn_List, key = operator.itemgetter(1),reverse=True)
		print(Kn_List)
		dis_List = sorted(dis_List, reverse= True)

		Best_index = Kn_List[0][0]
		if Activation[Best_index]==1:
			dec_learn_factor[i] = (0.5)**(i/dataSet.shape[0]) # we suppose dec_learn_factor[0] = 1, dec_learn_factor[dataSet.shape[0]] = 0.5
			Lena[i] =(0.5)**(i/dataSet.shape[0])  # we suppose Lena[0] = 1, Lena[dataSet.shape[0]] = 0.5
			for m in range(len(Vector)):
				hk = np.exp(m/Lena[i])
				#Vector[m,:]+=dec_learn_factor[i]*hk*(Vector_before[m,:]-x)
				Vector[m]+=dec_learn_factor[i]*hk*(Vector_before[m]-x)

	return Vector
				
			
			

def main(dataSet,N):
	Vector, Activation,Z = Initialization(dataSet,N)
	print (Vector)
	Vector = loop_neural_gas(Vector,Activation,Z,dataSet,N)
	print (Vector)


if __name__ == '__main__':
	dataSet = LoadData('testSet.txt')	
	main(dataSet,10)

	
	
	
