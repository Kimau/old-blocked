using System;

abstract public class QubedPal
{
	uint mask;
	public uint BitMask { get { return mask; } }
	
	public uint NumBits { get { return 0; } }
	public uint PalID   { get { return -1; } }
	
	public void SetMask(uint offset)
	{
		mask = (System.Math.Pow(2, NumBits) - 1) << offset;
	}
}