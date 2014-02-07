def dataToDict(f):
	d = {}
	f = open(f, 'r')
	keyString = f.readline()[:-2]
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
print meanAge(beths)
print meanAge(taxo)