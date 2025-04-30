# ---------------------------------------------------------------------------------
#
#	CS 315 Hw 1
#
#
#	====== Part A ======
#
#	Assignment of the built-in list creates reference to the original one. (Changes on the new one effects the original one.)
#
#	Subset assignment of the built-in list creates copy of the original one. (Changes on the new one does not effect the original one.)
#
#	Both assignment and subset assignment of the NumPy array creates reference to the original one. (Changes on the new one effects the original one.)
#
#
#	====== Part B ======
#
#	'*' operation on NumPy 2D arrays multiplies elements element-wise.
#
#	'*' operation on NumPy matrices, does matrix multiplication.
#
#
#	'**' operation on NumPy 2D arrays takes n-th power of each element.
#
#	'**' operation on NumPy matrices, takes power of matrices by multiplying matrices n times.
#
#
#	====== Part C ======
#

def readMatrix(fi):
	mx = None
	i = 0
	with open(fi) as f:
		for line in f:
			if i == 1: mx = np.zeros(shape=(int(line), int(line)))
			elif i > 3:
				li = line.split(" -- ")
				mx[li[0], li[1]] = 1
				mx[li[1], li[0]] = 1
			i += 1
	return mx

def numPath(mat, m):
	mx = mat
	for i in range (1, m): mx = np.dot(mx, mat)
	for i in range (0, mx.shape[0]):
		for j in range (i, mx.shape[0]):
			print str(i + 1) + " <-> " + str(j + 1) + " : " + str(int(mx[i, j]))

#
#	====== Part D ======
#
#	To store graphs more efficiently, using dictionaries could help as:
#
#		- For each node there will be only one entry.
#
#		- Each item in the dictionary will contain all edge information of the node specified with the key.
#
#				graph = {	'A': ['B', 'C'],
#							'B': ['C', 'D'],
#							'C': ['D'],
#							'D': ['C']}
#
#		* https://www.python.org/doc/essays/graphs/
#
#
#	With using libraries/packages:
#
#		- NetworkX (lots of great features)
#		- graph-tool (implemented in c++ for speed, based on BoostGraph lib)
#		- PyTables (large amounts of data)
#		- igraph
#
#
#	====== Part E ======
#

def createNameMap(acc):
	dic = {}
	i = 0
	for a in acc:
		n = a.getName()
		if n in dic: dic[n].append(i)
		else: dic[n] = [i]
		i += 1
	return dic

#
#	====== Notes ======
#
#	Please run this script as:
#
#		python hw1.py <input_file> <path_length>
#
#		python hw1.py in.txt 7
#
# ---------------------------------------------------------------------------------

import sys
import random
import time
import numpy as np

# ---------------------------------------------------------------------------------

if len(sys.argv) < 3:
	sys.exit(1)

# ---------------------------------------------------------------------------------

def pri(t, l=0):
	if l == 1: print "\n\n===== " + t + " =====\n"
	else: print "\n--- " + t + " ---\n"

# ---------------------------------------------------------------------------------

pri("Part A & B", 1)

pri("built in lists")
data = [1, 2, 3, 4]
print data
otherData = data
otherData[1] = -2
print otherData
print data
otherData = data[1:3]
print otherData
otherData[0] = 0
print otherData
print data

pri("numpy arrays")
data = np.array([1, 2, 3, 4])
print data
otherData = data
otherData[1] = -2
print otherData
print data
otherData = data[1:3]
print otherData
otherData[0] = 0
print otherData
print data

pri("numpy 2d arrays")
A = np.array([[1,2], [3,4]])
B = np.array([[2,1], [-1,2]])
print A * B
print A ** 3

pri("numpy matrices")
A = np.matrix([[1,2], [3,4]])
B = np.matrix([[2,1], [-1,2]])
print A * B
print A ** 3

# ---------------------------------------------------------------------------------

pri("Part C", 1)

pri("adjacency matrix")
mx = readMatrix(sys.argv[1])
print mx

pri("paths with length " + sys.argv[2])
numPath(mx, int(sys.argv[2]))

# ---------------------------------------------------------------------------------

pri("Part E", 1)

class Account:

	def __init__(self, id, name, balance):
		self.id = id
		self.name = name
		self.balance = balance

	def __str__(self): return "[id: %d, name: %s, balance: %s]" % (self.id, self.name, self.balance)

	def getId(self): return self.id

	def getName(self): return self.name

	def getBalance(self): return self.balance

	def withdraw(self, amount):
		self.balance -= amount
		return self.balance

	def deposit(self, amount):
		self.balance += amount
		return self.balance

def generateRandomAccounts(n):
	accounts = []
	for id in xrange(1, (n + 1)):
		name = ""
		for i in xrange(0, 5): name += random.choice("abcdefghijklmnopqrstuvwxyz")
		if id == 1: print "First account name is '%s'" % name
		accounts.append(Account(id, name, random.choice(xrange(0, 1000))))
	return accounts

def findAccountIndices(name, accounts):
	indices = []
	for (index, account) in enumerate(accounts):
		if account.getName() == name: indices.append(index)
	return indices

start = time.time()
accounts = generateRandomAccounts(1000000)
end = time.time()
print "Accounts created in %f seconds" % (end - start)
start = time.time()
nameMap = createNameMap(accounts)
end = time.time()
print "Name map created in %f seconds" % (end - start)

while True:
	name = raw_input("Account name: ")
	if name == "":
		print "Exiting..."
		break
	start1 = time.time()
	indices_x = findAccountIndices(name, accounts)
	end1 = time.time()
	start2 = time.time()
	indices = nameMap.get(name, [])
	end2 = time.time()
	if len(indices) > 0:
		for index in indices: print "> Account found: %s" % accounts[index]
	else: print "> No accounts found"
	print "Slow search took %f seconds" % (end1 - start1)
	print "Fast Search took %f seconds" % (end2 - start2)
