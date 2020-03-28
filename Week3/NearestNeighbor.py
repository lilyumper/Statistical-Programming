import numpy as np

print("Thomas Garcia")
print("DATA-51100, Statistical Programming")
print("Programming Assignment #3\n")

# Setting the csv's

training_data = "iris-training-data.csv"
test_data = "iris-testing-data.csv"

'''
we have to go through the data now
so we have to load data by adding numpy loadtxt
also included in the parameters is delimitier which mean it points out what seperates the data
in this case it is the ,
then we use cols which shows what columns to use, in this case we are using the first 4
so we start at teh 0 index to the 3 index
'''
training_attributes = np.loadtxt(training_data, delimiter=",", usecols=(0, 1, 2, 3))

'''
here we are grabbing the fifth column which contains the label
we follow the same process as above and only added the data type string as a unicode
if we dont' add unicode we will get an error as <U15 represents string
'''
training_label_name = np.loadtxt(training_data, dtype='<U15', delimiter=",", usecols=(4))

# we now do the same with testing data

test_attributes = np.loadtxt(test_data, delimiter=",", usecols=(0, 1, 2, 3))
test_label_name = np.loadtxt(test_data, delimiter=",", dtype='<U15', usecols=(4))

''' 
we have to find the distance and also the minimal distance index of the two sets of data
axis is used as it represents where in teh array we are pulling data
in this case it is dimensions so 1 is the 2nd index dimensions and 2 is the third 
the sum equation at the end collapes the dimension n and deletes it which each value
in the new matrix equal to the sum of the collapsed values
we use newaxis because it actually helps us insert a axis without having to reconstruct a tuple 
argmin returns the minimum values of the axis
'''
distance = np.sqrt((np.square(test_attributes[:, np.newaxis] - training_attributes))).sum(axis=2)
min_dist = distance.argmin(axis=1)

'''
now we have to find the predicted labels
i could not figure a way to do so without a for loop
however we are turning our data into a new nd array
we are then interating through the index of TLN using the value that is found in min_dist
we then reshape the data to example of the TLN
'''
labels = np.array([[training_label_name[i]] for i in min_dist]).reshape(training_label_name.shape)

# next we find the accuracy of the labels sum of al labels that are the same as TLN divided by the len of labels
sumOfLabels =((labels == test_label_name).sum())
lengthLabels = len(labels)
acc = sumOfLabels/lengthLabels

# next we print out the predicted
for i in range(len(labels)):
    print(i+1 ,test_label_name[i], labels [i])

# next we add the acc
print("The accuracy is: ", (acc * 100),"%")
