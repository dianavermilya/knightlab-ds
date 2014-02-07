import codecs

def dataToDict(f):
	d = {}
	f = open(f, 'r')
	
	# strip line ending characters
	keyString = f.readline().rstrip()
	
	# check for and strip utf-8 BOM (python bug wont auto-remove it :( )
	if keyString[0:3] == codecs.BOM_UTF8:
	    keyString = keyString[3:]
	  
	keys = keyString.split(",")
	
	for key in keys:
		d[key] = []
	for line in f:
		ans=line.split(",")
		for i in range(len(keys)):
			d[keys[i]].append(ans[i])
	
	return d

def meanAge(d):
	ages = d['age']
	s = 0
	for age in ages:
		s += int(age)
	return float(s)/len(ages) 

beths = dataToDict('beths.csv')
taxo = dataToDict('taxo.csv')
print 
print meanAge(beths)
print meanAge(taxo)
