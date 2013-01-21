using System;
using System.Collections.Generic;
using System.Diagnostics;

public class QubedBlock
{
	struct QBlkLink 
	{ 
		public uint artID; 
		public uint blkID; 
		public QBlkLink(uint a, uint b)
		{
			artID = a;
			blkID = b;
		}
	};
	
	uint artistID;
	uint blockID;
	uint blockSize;	
	uint[] qBits;	
	Dictionary<Type, QubedPal> qPals;	
	Dictionary<uint, QBlkLink> qLinks;
	
	float[] defaultColour = new float[]{1.0f, 1.0f, 1.0f};
	float defaultAlpha = 1.0f;
	
	
	//--------------------------------------------------------
	// Accessors
	public QPalColour Colour { get { return (QPalColour)qPals[typeof(QPalColour)]; } }
	public QPalAlpha  Alpha  { get { return (QPalAlpha)qPals[typeof(QPalAlpha)];  } }
	public QPalShade  Shade  { get { return (QPalShade)qPals[typeof(QPalShade)];  } }
	public QPalSmooth Smooth { get { return (QPalSmooth)qPals[typeof(QPalSmooth)]; } }
	
	public uint this[int key]
	{
    get { return qBits[key];  }
    set { qBits[key] = value; }
	}
		
	public int NumBits 
	{ 
		get 
		{ 
			int c = 2; 
			foreach(QubedPal p in qPals.Values)
				c += (int)p.NumBits; 
			
			return c;
		}
	}
	
	//---------------------------------------------------------
	// Constructors
	public QubedBlock() : this(0,0,8)
	{
	}
	
	public QubedBlock(byte[] rawBytes, int palLen, int blockLen, int lnkLen)
	{
		byte[] palDat   = new byte[palLen];
		byte[] blockDat = new byte[blockLen];
		byte[] lnkDat   = new byte[lnkLen];
		
		Buffer.BlockCopy(rawBytes, 0, palDat, 0, palLen);
		Buffer.BlockCopy(rawBytes, palLen, blockDat, 0, blockLen);
		Buffer.BlockCopy(rawBytes, palLen + blockLen, lnkDat, 0, lnkLen);
		
		// Process Pallette		
		artistID  = QubedPal.BitsToBig(palDat, 4, 0)[0];
		blockID   = QubedPal.BitsToBig(palDat, 4, 4)[0];
		blockSize = QubedPal.BitsToBig(palDat, 1, 8)[0];
		
		qPals = new Dictionary<Type, QubedPal>();
		
		uint palOffset = 9;
		while(palOffset < palLen)
		{
			if((palDat[palOffset] >= QPalColour.MINID) && (palDat[palOffset] < QPalColour.MAXID))
				qPals[typeof(QPalColour)] = new QPalColour(palDat, ref palOffset, NumBits);
			else if((palDat[palOffset] >= QPalAlpha.MINID) && (palDat[palOffset] < QPalAlpha.MAXID))
				qPals[typeof(QPalAlpha)] = new QPalAlpha(palDat, ref palOffset, NumBits);
			else if((palDat[palOffset] >= QPalShade.MINID) && (palDat[palOffset] < QPalShade.MAXID))
				qPals[typeof(QPalShade)] = new QPalShade(palDat, ref palOffset, NumBits);
			else if((palDat[palOffset] >= QPalSmooth.MINID) && (palDat[palOffset] < QPalSmooth.MAXID))
				qPals[typeof(QPalSmooth)] = new QPalSmooth(palDat, ref palOffset, NumBits);
			else
				Debug.Assert(false, "Unknown Pal ID");
		}
		
		// Process Block Data
		List<uint> linkIDList = new List<uint>();

		qBits = new uint[blockSize*blockSize*blockSize];
		for(uint i = 0; i < (blockSize*blockSize*blockSize); ++i)
		{
			qBits[i] = blockDat[i];
			if((qBits[i] & 0x2) == 1)
				linkIDList.Add(i);
		}
		
		// Process Link Data
		List<uint> lnkDatList = QubedPal.BitsToBig(lnkDat, (uint)lnkLen, 0);
		
		Debug.Assert(linkIDList.Count != (lnkDatList.Count*2), "Link Bits don't match amount of Links Sent");
		
		qLinks = new Dictionary<uint, QBlkLink>();
		for(int i = 0; i < linkIDList.Count; ++i)
		{
			qLinks[linkIDList[i]] = new QBlkLink(lnkDatList[i*2], lnkDatList[i*2+1]);
		}
		
	}
	
	public QubedBlock(uint artID, uint blkID, uint blkSize)
	{
		artistID = artID;
		blockID = blkID;
		blockSize = blkSize;
		
		qBits = new uint[blockSize*blockSize*blockSize];
		qPals = new Dictionary<Type, QubedPal>();
		qLinks = new Dictionary<uint, QBlkLink>();
	}
	
	//-------------------------------------------------------------------
	// Functions
	
	public uint fromXYZ(uint x, uint y, uint z) 
	{ 
		return x + (y*blockSize) + (z*blockSize*blockSize);
	}

	public float[] GetColour(uint i) 
	{
		uint blkVal = qBits[i];
		float[] blkColour = defaultColour;
		if(qPals.ContainsKey(typeof(QPalColour)))
			blkColour = Colour.GetColour(blkVal);
		
		if(qPals.ContainsKey(typeof(QPalShade)))
			Shade.GetShade(blkVal, ref blkColour);
		
		return blkColour;
	}
	
	
	public float GetAlpha(uint i) 
	{ 
		uint blkVal = qBits[i];
		if(qPals.ContainsKey(typeof(QPalAlpha)))
			return Alpha.GetAlpha(blkVal);
		else
			return defaultAlpha;
	}
	
	public bool IsVisible(uint i) 
	{ 
		if((qBits[i] & 1) == 0)
			return false;
		
		if(GetAlpha(qBits[i]) < 0.01f)
			return false;
		
		return true;
	}
	
	public bool IsVisible(uint x, uint y, uint z) { return IsVisible(fromXYZ(x,y,z)); }
	
}