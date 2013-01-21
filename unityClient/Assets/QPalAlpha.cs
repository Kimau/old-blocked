public class QPalAlpha : QubedPal
{
	public const uint MINID = 20;
	public const uint MAXID = 28;
	
	uint numBits;
	uint[] alphaDat;
	float[] alphaVal;
	
	public override uint NumBits { get { return numBits; } }
	public override uint PalID   { get { return MINID + numBits; } }
	
	public QPalAlpha()
	{
		numBits = 0;
	}
	
	public QPalAlpha(byte[] palDat, ref uint offset, int bitOffset)
	{
		numBits = palDat[offset++] - MINID;
		SetMask(bitOffset);
		
		uint reqLen = (uint)System.Math.Pow(2, numBits);
		alphaDat = new uint[reqLen];
		for(uint i=0; i < alphaDat.Length; ++i)
			alphaDat[i] = palDat[offset++];
		
		alphaVal = new float[alphaDat.Length];
		for(uint i=0; i < alphaVal.Length; ++i)
			alphaVal[i] = (float)(alphaDat[i]) / 100.0f;
	}
	
	public float GetAlpha(uint blk)
	{
		return alphaVal[BlkVal(blk)];
	}
}