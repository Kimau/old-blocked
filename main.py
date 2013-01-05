#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime
import urllib
import webapp2
import random
import json
import os
import jinja2
import logging

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.api import users

jinja_enviroment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#---------------------------------------------------------------------
#   Data Model Notes
#
#   BlockArtist < Block < BlockVer
#---------------------------------------------------------------------
class BlockArtist(db.Model):
	user     = db.UserProperty(auto_current_user=True)
	joined   = db.DateTimeProperty(auto_now_add=True)
	nickname = db.StringProperty(required=True)
	artistID = db.IntegerProperty(required=True)						# Artist Number
	blockMax = db.IntegerProperty(default=256)
	#xyz - facing
	x = db.IntegerProperty()
	y = db.IntegerProperty()
	z = db.IntegerProperty()
	f = db.IntegerProperty()

class Block(db.Model):
	blockID  = db.IntegerProperty(required=True)						# Block Number

# Core      - 1bit - SOLID Flag 
#           - 1bit - LINK Flag

# Colour Palette
# [10] 0bit - 1x  24Bit Web RGB   24 [0*512+ 1*24 =    0 +  24 =   24]
# [11] 1bit - 8x  24Bit Web RGB   48 [1*512+ 2*24 =  512 +  48 =  560]
# [12] 2bit - 8x  24Bit Web RGB  180 [2*512+ 4*24 = 1024 + 180 = 1120]
# [13] 3bit - 8x  24Bit Web RGB  360 [3*512+ 8*24 = 2048 + 360 = 1728]
# [14] 4bit - 16x 24Bit Web RGB  720 [4*512+16*24 = 4096 + 720 = 2432]

# Alpha Palette
# [20] 0bit - 100
# [20] 1bit - 100, 50
# [21] 2bit - 100, 75, 50, 25
# [22] 3bit - 100, 87, 74, 61, 48, 35, 22, 9

# Blend Palette
# [30] Multiply - 0bit - Stop Inheritence
# [31] Multiply - 1bit - 0, 50  - 24Bit Web RGB - 
# [32] Multiply - 2bit - 0, 33, 66, 100  - 24Bit Web RGB - 
# [33] Multiply - 3bit - 0, 10, 25, 40, 55, 70, 85, 100 - 24Bit Web RGB - 

# Smoothing Palette
# [40] 0bit - Stop Smoothing
# [41] 1bit - Not Smooth, Smooth
# [42] 2bit - Not Smooth, 3 x Smoothing Groups

# 50 Shape  - 3bit - Shape Date *shrug unkown*

class BlockVer(db.Model):
	date      = db.DateTimeProperty(auto_now_add=True)
	blockData = db.BlobProperty(required=True)						# Save Data
	palData   = db.ByteStringProperty()                             # Pallette Data
	linkData  = db.ListProperty(db.Key)								# Links to BLOCK not Block Ver

#---------------------------------------------------------------------
#	Helpers
#---------------------------------------------------------------------
def getArtistByID(artID):
	if artID == None or len(artID) < 1:
		usr = users.get_current_user()
		artist = BlockArtist.gql('WHERE user = :u', u = usr).get()
		return artist

	artist = BlockArtist.get_by_key_name('aid' + artID)
	return artist

def getBlockByID(artID, blockID):
	if blockID == None or len(blockID) < 1:
		blockID = 0

	block = Block.get(db.Key.from_path('BlockArtist', 'aid' + str(artID), 'Block', 'bid' + str(blockID)))
	return block


#---------------------------------------------------------------------
#   Handler Notes
#---------------------------------------------------------------------
class ArtistHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['content-type'] = 'application/json; charset=utf-8'

		artist = getArtistByID(self.request.get('aid'))

		if artist == None:			
			self.response.out.write(json.dumps({"aid": -1, "nickname" : '' }));
			return

		self.response.out.write(json.dumps({"aid": artist.artistID, "nickname" : artist.nickname }));


	def post(self):
		self.response.headers['content-type'] = 'application/json; charset=utf-8'
		usr = users.get_current_user()

		artist = getArtistByID(None)

		if artist == None:
			newNick = self.request.get('newNickname')
			if newNick == None or len(newNick) < 3:
				self.response.out.write('No Nickname')
				self.error(400)
				return

			myArtID = self.bumpCounter()

			if myArtID > 0:
				artist = BlockArtist(key_name='aid' + str(myArtID), nickname = newNick, artistID = myArtID)
				artist.put()
			else:
				self.response.out.write('OUT OF RANGE ')

			if artist == None:			
				self.error(500)
				return
			#

		self.response.out.write(json.dumps({"aid": artist.artistID, "nickname" : artist.nickname }));

	def bumpCounter(self):
		memCl = memcache.Client()
		counter = memCl.gets('aid')
		if counter == None:
			aid = BlockArtist.all(keys_only=True).count()
			memCl.set('aid', aid)
			counter = memCl.gets('aid')

		x = 0
		while x < 10:
			counter = memCl.get('aid')
			if memCl.cas('aid', counter+1):
				return counter+1
			x += 1

		return -1

class BlockHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['content-type'] = 'application/json; charset=utf-8'

		# Check if Art ID
		artist = getArtistByID(self.request.get('aid'))

		if artist == None:
			self.response.out.write(json.dumps({ "aid": -1 }));
			return

		# Check Block ID
		block = getBlockByID(artist.artistID, self.request.get('blockID'))

		if block == None:
			self.response.out.write(json.dumps({"aid": artist.artistID, "bid" : -1 }));
			return

		# Else Get Home Block
		self.response.out.write(json.dumps({"aid": artist.artistID, "bid" : block.blockID }));

	def post(self):
		# Block Data
		bData = self.request.get('blockData')
		pData = self.request.get('palData')
		lData = self.request.get('linkData')

		# Validate Data
		if bData == None or pData == None or lData == None or len(bData) < 1 or len(pData) < 1 == None or len(lData) < 1 == None:
			# You need to pass this data
			self.error(400)

		self.response.out.write(json.dumps({'blockData':bData, 'palData':pData, 'linkData':lData}));
		return

		# Check Block ID
		artist = getArtistByID(None)
		bid = self.request.get('blockID')
		block = getBlockByID(artist.artistID, bid)


		# Create New Block
		if block == None:
			blockList = Block.gql('WHERE ancestor IS :a', a = artist)
			bid = blockList.count()

			if bid >= artist.blockMax:
				self.error(500) # Exceeded Limit
				return

			block = Block(key_name='bid' + str(bid),parent=artist, blockID=bid)
			block.put()
			#

		# Make New Version
		newBVersion = BlockVer(parent=block, blockData=bData, palData=pData, linkData=lData)
		newBVersion.put()

		self.response.out.write(json.dumps({"aid": artist.artistID, "bid" : block.blockID }));
		pass

class MainHandler(webapp2.RequestHandler):
	def get(self):
		usr = users.get_current_user()

		artist = getArtistByID(None)

		if artist == None:
			self.response.out.write("""<div class="artist form"><h3>Create Artist Profile</h3>
				<form action="/artist" method="post">
				<input type="text" name="newNickname" />
				<input type="submit" value="Submit" />
				</form></div>
				""");
			return
		else:
			self.response.out.write("""
				Hello %s ! Your #%d
				""" % (artist.nickname, artist.artistID));
		#

		blockList = Block.gql('WHERE ancestor IS :a', a = artist)

		self.response.out.write(blockList.count())
		self.response.out.write('<div class="blockList"><ul>')
		for block in blockList:
			self.response.out.write('<li>#%d : ver[#%d]</li>' % (block.blockID, 0))

		self.response.out.write('</ul></div>')

		self.response.out.write("""<div class="block form"><h3>Create Block</h3>
				<form action="/block" method="post">
				<input name="colour1" type="color" />
				<input type="submit" value="New Block" />
				</form></div>
				""");

#================================================================================
#
#                Helper Functions
#
#================================================================================
def BitsToBig(s, num):
	tempBucket = 0
	bigNums = []
	i = 0
	while(len(s)):
		if s[i] >= num:
			bigNums.append(tempBucket)
			tempBucket = 0
		else:
			tempBucket = (tempBucket * num) + s[i]
		++i

	if tempBucket > 0:
		bigNums.append(c)
	elif bigNums.length == 0:
		bigNums = [0]

	return bigNums

def MakBit(bigNumber, num, padSize):
	if bigNumber:
		return [0]

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
	
	smallBits = [MakeBit(bigNums[0], num, 0)]

	i = 0
	while i < len(bigNums):
		smallBits.append(MakeBit(bigNums[0], num, 0))

	return smallBits

class BlockPal:
	palColourID = [10:19]
	palAlphaID  = [20:29]
	palShadeID  = [30:39]
	palSmoothID = [40:49]

	def ConvertFromBytes(self, byteData):
		#
		self.artistID     = BitsToBig(byteData[0:4], 255)
		self.blockID      = BitsToBig(byteData[4:8], 255)
		self.bitsPerBlock = byteData[8]
		
		self.palColour    = None
		self.palAlpha     = None
		self.palShade     = None
		self.palSmooth    = None

		byteData = byteData[9:]
		while(len(byteData)):
			#
			if   byteData[0] > palColourID[0] and byteData[0] < palColourID[1]:
				#
			elif byteData[0] > palAlphaID[0]  and byteData[0] < palAlphaID[1]:
				#
			elif byteData[0] > palShadeID[0]  and byteData[0] < palShadeID[1]:
				#
			elif byteData[0] > palSmoothID[0] and byteData[0] < palSmoothID[1]:
				#
			else:
				# "Unknown Pal or Something gone wrong in processing"
				raise new Exception("Unknown Pal or Something gone wrong in processing")
			#
		#

	def ConvertToBytes(self, bytes):
		#

# Block Handler
class BlockEditHandler(webapp2.RequestHandler):
	def processData(self, blockDataLength, palDataLength, linkDataLength, rawBody):
		# Check Lengths
		if(palDataLength < 2) or (palDataLength > 490):
			return [False, "Pallette Data Length Invalid"]
		if(linkDataLength < 0):
			return [False, "Link Data Length Invalid"] 
		if(blockDataLength != 512):
			return [False, "Block Data Length Invalid"]

		# Process Block
		palData = rawBody[0:palDataLength]
		blockData = rawBody[palDataLength:(palDataLength+blockDataLength)]
		linkData = rawBody[(palDataLength+blockDataLength):(palDataLength+blockDataLength+linkDataLength)]

		newPal = BlockPal()
		newPal.ConvertFromBytes(palData)

		# a
		BitsToBig(processedBlock["pal"][0:4], 255)

		logging.info(str(rawBody) + '\n-------------------\n' + str([palData, blockData, linkData]) + '\n-------------------\n')

	def post(self):
		rawBytes = []
		for line in self.request.body:
			rawBytes.append(ord(str(line)))

		try:
			blockLen = int(self.request.get('szBlock'))
		except ValueError:
			blockLen = 0

		try:
			palLen = int(self.request.get('szPal'))
		except ValueError:
			palLen = 0

		try:
			linkLen = int(self.request.get('szLink'))
		except ValueError:
			linkLen = 0

		self.processData(blockLen, palLen, linkLen, rawBytes)

		# Send Response
		self.response.headers['Content-Type'] = 'application/boobs; base64'
		self.response.headers['szBlock']      = str(self.request.get('szBlock'))
		self.response.headers['szPal']        = str(self.request.get('szPal'))
		self.response.headers['szLink']       = str(self.request.get('szLink'))
		self.response.body = self.request.body

	def get(self):
		# SETUP
		artist = getArtistByID(None)

		if artist == None:
			self.error(500)
			return

		aid = artist.artistID
		block = getBlockByID(aid, None)

		if block == None:
			bid = 0
		else:
			bid = block.blockID

		# Get Others
		blockList = Block.gql('WHERE ancestor IS :a', a = artist)

		# Get Request Data
		bData = self.request.get('blockData')
		pData = self.request.get('palData')
		lData = self.request.get('linkData')

		template_values = {
			'artistID' : aid,
			'blockID'  : bid,
			'blockList': blockList,
			'blockData': bData, 
			'palData'  : pData, 
			'linkData' : lData
		}

		template = jinja_enviroment.get_template('newBlockVer.html')
		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
								('/', MainHandler), 
								('/artist', ArtistHandler), 
								('/block', BlockHandler),
								('/blockEditor', BlockEditHandler)],
								debug=True)
