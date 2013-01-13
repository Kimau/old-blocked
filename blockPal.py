def BitsToBig(s, num):
	tempBucket = 0
	bigNums = []

	for i in range(len(s)):
		if s[i] >= num:
			bigNums.append(tempBucket)
			tempBucket = 0
		else:
			tempBucket = (tempBucket * num) + s[i]

	if tempBucket > 0:
		bigNums.append(tempBucket)
	elif len(bigNums) == 0:
		bigNums = [0]

	return bigNums

def MakeBit(bigNumber, num, padSize):
	if bigNumber < 1:
		return [0] * padSize

	smallBits = []
	while(bigNumber > 0):
		r = bigNumber % num
		smallBits.append(r)
		bigNumber = int(bigNumber / num)

	while len(smallBits) < padSize:
		smallBits.append(0)

	smallBits.reverse()
	return smallBits

def BigToBits(bigNums, num, padSize=0):
	if len(bigNums) == 0:
		return []
	
	smallBits = []

	for i in range(len(bigNums)):
		smallBits.append(MakeBit(bigNums[i], num, padSize))

	smallBits = reduce(lambda x,y: x + [255] + y, smallBits)
	return smallBits

def BytesToLinkList(rawData):
	blkLinks = []
	return blkLinks

class ColourPal:
	minID = 10
	maxID = 19

	def __init__(self):
		self.bits = 0
		self.colours = []

	def __repr__(self):
		return "Colour %d bits \t" % self.bits + str(self.colours)

	def EncodeJSON(self):
		tempDict = { 'palType' : 'Colour', 'bits': self.bits, 'palID' : ColourPal.minID + self.bits }
		tempDict['colours'] = self.colours
		return tempDict

	def ByteStr(self):
		tempDict = { 'ID' : ColourPal.minID + self.bits }
		tempDict['c'] = self.colours
		return tempDict		

	def ConvertFromBytes(self, byteData):
		#
		self.bits = byteData[0] % 10
		byteData = byteData[1:]
		
		self.colours = []
		reqLen = pow(2,self.bits)
		while reqLen > 0:
			self.colours.append(byteData[:3])
			byteData = byteData[3:]
			reqLen -= 1

		return byteData

	def ConvertToBytes(self):
		byteData = [self.bits + ColourPal.minID]
		byteData += reduce(lambda a,b: a + b, self.colours, [])
		return byteData

class AlphaPal:
	minID = 20
	maxID = 29

	def __init__(self):
		self.bits = 0
		self.scale = []

	def __repr__(self):
		return "Alpha %d bits \t" % self.bits + str(self.scale)

	def EncodeJSON(self):
		tempDict = { 'palType' : 'Alpha', 'bits': self.bits, 'palID' : AlphaPal.minID + self.bits }
		tempDict['scale'] = self.scale
		return tempDict

	def ByteStr(self):
		tempDict = { 'ID' : AlphaPal.minID + self.bits }
		tempDict['s'] = self.scale
		return tempDict		

	def ConvertFromBytes(self, byteData):
		#
		self.bits = byteData[0] % 10
		byteData = byteData[1:]
		
		self.scale = []
		reqLen = pow(2,self.bits)
		while reqLen > 0:
			self.scale.append(byteData[0])
			byteData = byteData[1:]
			reqLen -= 1

		return byteData

	def ConvertToBytes(self):
		byteData = [self.bits + AlphaPal.minID]
		byteData += self.scale
		return byteData

class ShadePal:
	minID = 30
	maxID = 39
	shadingMethods = {0: 'multiply',1: 'blend'};

	def __init__(self):
		self.bits = 0
		self.colour = [0,0,0]
		self.scale = []
		self.method = 0

	def __repr__(self):
		return "Shade %d bits \t%s %s - %s" % (self.bits, ShadePal.shadingMethods[self.method], str(self.colour), str(self.scale))

	def EncodeJSON(self):
		tempDict = { 'palType' : 'Shade', 'bits': self.bits, 'palID' : ShadePal.minID + self.bits }
		tempDict['method'] = self.method
		tempDict['colour'] = self.colour
		tempDict['scale'] = self.scale
		return tempDict

	def ByteStr(self):
		tempDict = { 'ID' : ShadePal.minID + self.bits }
		tempDict['m'] = self.method
		tempDict['c'] = self.colour
		tempDict['s'] = self.scale
		return tempDict		

	def ConvertFromBytes(self, byteData):
		#
		self.bits = byteData[0] % 10
		self.method = byteData[1]
		byteData = byteData[2:]

		self.colour = byteData[:3]
		byteData = byteData[3:]

		self.scale = []
		reqLen = pow(2,self.bits)
		while reqLen > 0:
			self.scale.append(byteData[0])
			byteData = byteData[1:]
			reqLen -= 1

		return byteData

	def ConvertToBytes(self):
		byteData = [self.bits + ShadePal.minID, self.method]
		byteData += self.colour
		byteData += self.scale
		return byteData

class SmoothPal:
	minID = 40
	maxID = 49
	
	def __init__(self):
		self.bits = 0

	def __repr__(self):
		return "Smooth %d bits \t" % self.bits

	def EncodeJSON(self):
		tempDict = { 'palType' : 'Smooth', 'bits': self.bits, 'palID' : SmoothPal.minID + self.bits }
		return tempDict

	def ByteStr(self):
		tempDict = { 'ID' : SmoothPal.minID + self.bits }
		return tempDict		

	def ConvertFromBytes(self, byteData):
		#
		self.bits = byteData[0] % 10
		byteData = byteData[1:]
		return byteData

	def ConvertToBytes(self):
		return [self.bits + SmoothPal.minID]

class QubedBlock:
	def __init__(self):
		self.artistID = 0
		self.blockID = 0
		self.bitsPerBlock = 8
		self.pallettes = []
		self.links = []
		self.blockData = []
		self.rawPal = []

	def __repr__(self):
		s = "Block %d:%d  %dbits" % (self.artistID, self.blockID, self.bitsPerBlock)
		s += " \n--Pallettes--\n"
		for p in self.pallettes:
			s += str(p) + " \n"
		s += "--------------\n"
		return s

	def EncodeJSON(self):
		tempDict = { 'artistID' : self.artistID, 'blockID' : self.blockID, 'bits' : self.bitsPerBlock, 'pals' : [], 'links' : self.links }
		for p in self.pallettes:
			tempDict['pals'].append(p.EncodeJSON())

		return tempDict

	def ByteStr(self):
		tempDict = { 'b' : self.bitsPerBlock, 'p' : [] }
		for p in self.pallettes:
			tempDict['p'].append(p.ByteStr())

		return tempDict

	def BytesToLinks(self, byteData):
		flatLink = BitsToBig(byteData, 255)
		self.links = []
		while(len(flatLink) >= 2):
			self.links.append(flatLink[:2])
			flatLink = flatLink[2:]


	def ConvertFromByteString(self, aid, bid, byteStrObj):
		self.rawPal       = None
		self.artistID     = int(aid)
		self.blockID      = int(bid)
		self.bitsPerBlock = int(byteStrObj["b"])
		self.pallettes    = []
		for p in byteStrObj["p"]:
			if p["ID"] >= ColourPal.minID  and p["ID"] <= ColourPal.maxID:
				newPal         = ColourPal()
				newPal.bits    = p["ID"] % 10
				newPal.colours = p["c"] 
			elif p["ID"] >= AlphaPal.minID  and p["ID"] <= AlphaPal.maxID:
				newPal       = AlphaPal()
				newPal.bits  = p["ID"] % 10
				newPal.scale = p["s"] 
			elif p["ID"] >= ShadePal.minID  and p["ID"] <= ShadePal.maxID:
				newPal = ShadePal()
				newPal.bits   = p["ID"] % 10
				newPal.colour = p["c"] 
				newPal.method = p["m"] 
				newPal.scale  = p["s"] 
			elif p["ID"] >= SmoothPal.minID  and p["ID"] <= SmoothPal.maxID:
				newPal       = SmoothPal()
				newPal.bits  = p["ID"] % 10
			else:
				raise Exception("Unknown ID")

			self.pallettes.append(newPal)
			#
		#
	def ConvertToBytes(self):
		byteData = []
		byteData += MakeBit(self.artistID, 255, 4)
		byteData += MakeBit(self.blockID, 255, 4)
		byteData += [self.bitsPerBlock]
		for p in self.pallettes:
			byteData += p.ConvertToBytes()

		self.rawPal = byteData
		return byteData

	def ConvertFromBytes(self, byteData):
		#
		self.rawPal       = byteData
		self.artistID     = BitsToBig(byteData[0:4], 255)[0]
		self.blockID      = BitsToBig(byteData[4:8], 255)[0]
		self.bitsPerBlock = byteData[8]
		
		self.pallettes = []

		byteData = byteData[9:]
		i = len(byteData)
		while len(byteData) > 0 and i > 0:
			if byteData[0] >= ColourPal.minID and byteData[0] < ColourPal.maxID:
				pal = ColourPal()	# Colour
			elif byteData[0] >= AlphaPal.minID and byteData[0] < AlphaPal.maxID:
				pal = AlphaPal()	# Alpha
			elif byteData[0] >= ShadePal.minID and byteData[0] < ShadePal.maxID:
				pal = ShadePal()	# Shade
			elif byteData[0] >= SmoothPal.minID and byteData[0] < SmoothPal.maxID:
				pal = SmoothPal()	# Smoothing
			else:
				return False #raise new Exception("Unknown Pal or Something gone wrong in processing")

			byteData = pal.ConvertFromBytes(byteData)
			self.pallettes.append(pal)
			i -= 1
			#
		#


if __name__=="__main__":
	sampleLinks = [4444, 1235, 4444, 1235, 4444, 1235, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 4444, 1235, 8, 45, 8, 45, 8, 45, 4444, 1235, 8, 45, 8, 45]
	sampleLinkBits = [17, 109, 255, 4, 215, 255, 17, 109, 255, 4, 215, 255, 17, 109, 255, 4, 215, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 1, 255, 3, 255, 17, 109, 255, 4, 215, 255, 8, 255, 45, 255, 8, 255, 45, 255, 8, 255, 45, 255, 17, 109, 255, 4, 215, 255, 8, 255, 45, 255, 8, 255, 45]

	x = QubedBlock()
	y = [0, 0, 0, 0, 0, 0, 0, 0, 8, 13, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 21, 100, 50, 32, 0, 0, 0, 0, 0, 33, 66, 100, 40]
	x.ConvertFromBytes(y)
	x.BytesToLinks(sampleLinkBits)
	print(x)

	z = x.ConvertToBytes()
	# print(y)
	# print(z)
	print("Byte encoding input/output match: " + str(all(map(lambda a,b: a == b, y,z))))

	import json
	# Compact JSON
	jsonPretty = json.dumps(x.EncodeJSON(), sort_keys=True, indent=4, separators=(',', ': '))
	jsonLong   = json.dumps(x.EncodeJSON(), separators=(',',':')) 
	jsonPacked = json.dumps(x.ByteStr(), separators=(',',':')) 

	print( jsonLong )
	print( jsonPacked )

	x.ConvertFromByteString(x.artistID, x.blockID, json.loads(jsonPacked))
	# Preety Print
	# print( json.dumps(x.EncodeJSON(), sort_keys=True, indent=4, separators=(',', ': ')) )

	testData = BigToBits(sampleLinks,255);
	print(sampleLinkBits == sampleLinks)
	#
#
