public class QPalColour : QubedPal
{
	public const uint MINID = 10;
	public const uint MAXID = 18;
	
	uint numBits;
	uint[][] colourDat;
	float[][] colours;
	
	public override uint NumBits { get { return numBits; } }
	public override uint PalID   { get { return MINID + numBits; } }
	
	public QPalColour()
	{
		numBits = 0;
	}
		
	public QPalColour(byte[] palDat, ref uint offset, int bitOffset)
	{
		numBits = palDat[offset++] - MINID;
		SetMask(bitOffset);
		
		colourDat = new uint[(int)System.Math.Pow(2, numBits)][];
		for(int i=0; i < colourDat.Length; ++i)
		{
			colourDat[i] = new uint[3];
			colourDat[i][0] = palDat[offset++];
			colourDat[i][1] = palDat[offset++];
			colourDat[i][2] = palDat[offset++];
		}
		
		colours = new float[colourDat.Length][];
		for(int i=0; i < colours.Length; ++i)
		{
			colours[i] = new float[3];
			colours[i][0] = (float)colourDat[i][0] / 255.0f;
			colours[i][1] = (float)colourDat[i][1] / 255.0f;
			colours[i][2] = (float)colourDat[i][2] / 255.0f;
		}
	}
	
	public float[] GetColour(uint blk)
	{
		return colours[BlkVal(blk)];
	}
}