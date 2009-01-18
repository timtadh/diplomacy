#Pre: Pass in a list, each element is a line of the file
#Post: Return a dictionary object that was made like this
    # File:
    #    Key|Value
    #    Key|
    #    Key|Value
    #    ~
    #    ~
    #the spot that has no value, the key|value pair that follows it is its value
    #in other words it has a dictionary as its value
    # List passed in:
    #    {'Key|Value', 'Key|', 'Key|Value', '~', '~']

    # Dictionary Returned:
    #    {Key:Value, Key:{Key:Value}}
def accessAdvanceddb(list):
	dict = {}
	x = 0
	
	while x < list.__len__() and list[x] != '~':
	    
		if list[x][list[x].__len__()-1] == '|':
			list2 = []
			key = list[x]
			
		
	                for y in range(x+1, list.__len__()):
				list2.append(list[y]) #put all items after the key in a list
				
			for y in range(x+1, list.__len__()):
				del list[x] #delete all the items that where put in list2
				
			returnedVal = accessAdvanceddb(list2) #recursive call

			current = key.split('|')
			if len(current) >= 1 and len(returnedVal) >= 1:
                            cDict = {current[0]:returnedVal[0]} #update the dictionary obj
                            dict.update(cDict)
                        else:
                            return [None, []]

			list.__iadd__(returnedVal[1]) #put unused items back in list
		else:
			current = list[x].split('|')
			if len(current) == 2:
                            cDict = {current[0]:current[1]} #update the ditionary object for reg
                            dict.update(cDict)
                        else:
                            return [None, []]
		x += 1
		     
	list3 = []
	for z in range((x+1), list.__len__()):
		list3.append(list[z])
	returnVal = []
	returnVal.append(dict) #contains dictionary created
	returnVal.append(list3) #list3 contains unused items
	return returnVal 

#Pre: pass in a dictionary object, no other objects in dict except for diction and primative
#Post: returns the dictionary in advanceDDB format
    # File:
    #    Key|Value
    #    Key|
    #    Key|Value
    #    ~
    #    ~
def makeAdvanceDDB(d):
	s = ''
	list = d.keys()
	for x in list:
		if type(d[x]) == type({}): #if current item a dictionary object
			s += str(x) + '|^'
			s += makeAdvanceDDB(d[x]) #recursive call
		else: s += str(x) + '|' + str(d[x]) + '^' #put key val pair in string
	s += '~' + '^' #end the dictionary
	return s

#pass in valid file name for file in AdvanceDDB format return a Dictionary Obj
def openAdvanceDDB(filename):
    file = open(filename)
    fileList = file.readlines()
    file.close()
    str = ''
    for x in fileList:
        str += x
    rawList = str.split('^')
    if rawList[rawList.__len__()-1] == '': del rawList[rawList.__len__()-1]
    return accessAdvanceddb(rawList)[0]

def decodeDDB(string):
    rawList = string.split('^')
    if rawList[rawList.__len__()-1] == '': del rawList[rawList.__len__()-1]
    return accessAdvanceddb(rawList)[0]

#Pass in filename and dictionary object, returns true if successful write of
#an AdvanceDDB of the dictionary
def saveAdvanceDDB(filename, dict):
    str = makeAdvanceDDB(dict)
    file = open(filename, 'w')
    file.write(str)
    file.close()
    return True



