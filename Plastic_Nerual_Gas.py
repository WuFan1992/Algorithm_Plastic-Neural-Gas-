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
	Vector = np.mat(np.zeros((N,data_dim)))
	Vector[0,:] = dataSet[0,:]
	#Vector = []
	#Vector.append(dataSet[0,:])
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
				Vector[m,:]+=dec_learn_factor[i]*hk*(Vector_before[m,:]-x)
				#Vector[m]+=dec_learn_factor[i]*hk*(Vector_before[m]-x)

	return Vector
				
def SetVn(dataSet,Vector):
	Pn= []
	Vector_save = Vector
	Vector_new = []
	Vector_temp = []
	
	for v in Vector:
		Vector_temp = [vec for vec in Vector if vec!=v ]
		print (Vector_temp)
		for x in dataSet:
			smallest = True		
			for v_other in Vector_temp:
				if Distance(x,v) > Distance(x,v_other):	
					smallest = False		
			if smallest:			
				Pn.append(x)
		#Pn = np.mat(Pn)
		if len(Pn)!=0:
			v_new = sum(Pn)/len(Pn)
		else:
			v_new = 0
		Vector_new.append(v_new)
		#Vector = Vector_save
	
	return Vector_new
			
def Del_Vn_Decre_N:(Activation,Vector_new,N):
	'''
	for examplee there are 5 reference vector and 10 x
	so the Activation is in the form like [1,0,0,1,0], 1 represent the activation and 0 is nonactivation
	and then the Vector_new is in the form like [v1,0,v3,v4,0], if it is 0 , it means that no v in the Vector_new	

	'''		
	for i in range(len(Activation)):
		if Activation[i]== 1:
			vector = Vector_new[i]
			Vector_temp = [vec for vec in Vector if vec!=v ]
			for x in dataSet:
			smallest = True		
				for v_other in Vector_temp:
					if Distance(x,v) > Distance(x,v_other):	
					smallest = False		
				if smallest:			
					Pn.append(x)
			if len(Pn) == 0:
				Activation[i] =0
				Vector_new[i] =0
				N = N-1
	return Activation, Vector_new , N


			
		
def Set_An(Activation,Vector_new,Pn_list,Z,tolerate_cost,N):
	'''

	Pn_list is a list with 20 element(for example Vn has 20 vectors)
	Pn_list = [[x1,x14,x25,x78],[x2,x4],[],[x149,x235]````]
	D here is the dimension of x ,
	'''
	CN = 0
	CnN_list = []
	for i in range(len(Activation)):
		if Activation[i]==1:
			vec = Vector_new[i]
			Sum = 0
			for x in Pn_list[i] :
				D = len(x)
				Sum+= (x-vec)**2
			CnN = Sum/D
			if CnN >0:
				CnN_list.append(CnN)
			else:
				CnN_list.append(0)
			CN+=CnN
			if CnN < tolerate_cost:
				Activation[i]=1
		
	# verify if there is 0 in the list
	for cnn in CnN_list :
		if (cnn >=tolerate_cost) |(cnn ==0) |(CN not in Z):
			Z.append(CN)
			cv_star = max(CnN_list)
			Vector_new.append(cv_star)
			N = N+1	
			Vector= loop_neural_gas(Vector_new,Activation,Z,dataSet,N)   # iteration
		else:
			return Vector_new
			
			
		
	
			

def main(dataSet,N):
	#Vector, Activation,Z = Initialization(dataSet,N)
	#Vector = loop_neural_gas(Vector,Activation,Z,dataSet,N)e
	Vector = [[1.3,0.8],[1.5,-0.2],[-0.4,2.2]]
	Vector_new = SetVn(dataSet,Vector)
	print (Vector_new)


if __name__ == '__main__':
	dataSet = LoadData('testSet.txt')	
	main(dataSet,10)

	
	
	
