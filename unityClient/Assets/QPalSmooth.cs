public class QPalSmooth : QubedPal
{
	public const uint MINID = 40;
	public const uint MAXID = 48;
	
	uint numBits;
	
	public override uint NumBits { get { return numBits; } }
	public override uint PalID   { get { return MINID + numBits; } }
	
	public QPalSmooth()
	{
		numBits = 0;
	}
	
	public QPalSmooth(byte[] palDat, ref uint offset, int bitOffset)
	{
		numBits = palDat[offset++] - MINID;
		SetMask(bitOffset);
	}
	
	public uint SmoothGroup(uint blk)
	{
		return BlkVal(blk);
	}
}