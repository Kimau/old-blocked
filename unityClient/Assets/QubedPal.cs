using System;
using System.Collections.Generic;

abstract public class QubedPal
{
	int bitOffset;
	uint mask;
	public uint BitMask { get { return mask; } }
	public uint BlkVal(uint blk) { return (blk & mask) >> bitOffset; }
	
	public virtual uint NumBits { get { return 0; } }
	public virtual uint PalID   { get { return 0; } }
	
	public void SetMask(int offset)
	{
		bitOffset = offset;
		mask = (uint)(System.Math.Pow(2, NumBits) - 1) << offset;
	}
		
	/// <summary>
	/// Convert little number bits into a list of Big Numbers
	/// </summary>
	public static List<uint> BitsToBig(byte[] bArr, uint len, uint offset = 0, uint bitLimit = 255) 
	{
		uint tempBucket = 0;
		List<uint> numberList = new List<uint>();
		
		for(uint i = 0; i < len; ++i)
		{
			if(bArr[i+offset] >= bitLimit)
			{
				numberList.Add(tempBucket);
				tempBucket = 0;
			}
			else
				tempBucket = (tempBucket * bitLimit) + bArr[i+offset];
		}
		
		if(tempBucket > 0)
			numberList.Add(tempBucket);
		else if(numberList.Count == 0)
			numberList.Add(0);
		
		return numberList;
	}
	
	/// <summary>
	/// Makes a list of small bits from a big number
	/// </summary>
	public static List<uint> MakeBit(uint bigNumber, uint bitLimit = 255, uint padding = 0)
	{
		List<uint> bitList = new List<uint>();
		
		if(bigNumber == 0)
		{
			bitList.Add(0);
			return bitList;
		}
		
		while(bigNumber > 0)
		{
			bitList.Add(bigNumber % bitLimit);
			bigNumber /= bitLimit;
		}
		
		while(bitList.Count < padding)
			bitList.Add(0);
		
		bitList.Reverse();
		return bitList;
	}
	
	/// <summary>
	/// Makes a list of small bits split by limit token from a list of big numbers
	/// </summary>
	public static List<uint> BigToBits(uint[] bigNumbers, uint bitLimit = 255)
	{
		List<uint> bitList = new List<uint>();
		foreach(uint num in bigNumbers)
		{
			bitList.AddRange(MakeBit(num, bitLimit));
			bitList.Add(bitLimit);
		}
		
		bitList.RemoveAt(bitList.Count - 1);		
		return bitList;
	}
}