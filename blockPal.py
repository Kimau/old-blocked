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
		bigNums.append(c)
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

def BigToBits(bigNums, num):
	if len(bigNums) == 0:
		return []
	
	smallBits = []

	for i in range(len(bigNums)):
		smallBits.append(MakeBit(bigNums[i], num, 0))

	smallBits = reduce(lambda x,y: x + [255] + y, smallBits)
	return smallBits

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

	def ConvertFromBytes(self, byteData):
		#
		self.bits = byteData[0] % 10
		byteData = byteData[1:]
		return byteData

class BlockPal:
	def __init__(self):
		self.artistID = 0
		self.blockID = 0
		self.bitsPerBlock = 8
		self.pallettes = []

	def __repr__(self):
		s = "Block %d:%d  %dbits" % (self.artistID, self.blockID, self.bitsPerBlock)
		s += " \n--Pallettes--\n"
		for p in self.pallettes:
			s += str(p) + " \n"
		s += "--------------\n"
		return s

	def EncodeJSON(self):
		tempDict = { 'artistID' : self.artistID, 'blockID' : self.blockID, 'bits' : self.bitsPerBlock, 'pals' : []}
		for p in self.pallettes:
			tempDict['pals'].append(p.EncodeJSON())

		return tempDict

	def ConvertFromBytes(self, byteData):
		#
		self.artistID     = BitsToBig(byteData[0:4], 255)[0]
		self.blockID      = BitsToBig(byteData[4:8], 255)[0]
		self.bitsPerBlock = byteData[8]
		
		self.pallettes = []

		byteData = byteData[9:]
		i = len(byteData)
		while len(byteData) > 0 and i > 0:
			if byteData[0] > ColourPal.minID and byteData[0] < ColourPal.maxID:
				pal = ColourPal()	# Colour
			elif byteData[0] > AlphaPal.minID and byteData[0] < AlphaPal.maxID:
				pal = AlphaPal()	# Alpha
			elif byteData[0] > ShadePal.minID and byteData[0] < ShadePal.maxID:
				pal = ShadePal()	# Shade
			elif byteData[0] > SmoothPal.minID and byteData[0] < SmoothPal.maxID:
				pal = SmoothPal()	# Smoothing
			else:
				return False #raise new Exception("Unknown Pal or Something gone wrong in processing")

			byteData = pal.ConvertFromBytes(byteData)
			self.pallettes.append(pal)
			i -= 1
			#
		#

	def ConvertToBytes(self, bytes):
		#
		pass


if __name__=="__main__":
	x = BlockPal()
	y = [0, 0, 0, 0, 0, 0, 0, 0, 8, 13, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 21, 100, 50, 32, 0, 0, 0, 0, 0, 33, 66, 100, 40]
	x.ConvertFromBytes(y)
	print(x)
	import json
	# Compact JSON
	print( json.dumps(x.EncodeJSON(), separators=(',',':')) )
	# Preety Print
	# print( json.dumps(x.EncodeJSON(), sort_keys=True, indent=4, separators=(',', ': ')) )
