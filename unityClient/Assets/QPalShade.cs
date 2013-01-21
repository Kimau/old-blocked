public class QPalShade : QubedPal
{
	public const uint MINID = 30;
	public const uint MAXID = 38;
	
	uint numBits;
	uint shadeMethod;
	uint[] shadeColour;
	uint[] shadeDat;	
	
	float[] shadeTint;
	float[] shadeLevels;
	
	public override uint NumBits { get { return numBits; } }
	public override uint PalID   { get { return MINID + numBits; } }
	
	public QPalShade()
	{
		numBits = 0;
	}
	
	public QPalShade(byte[] palDat, ref uint offset, int bitOffset)
	{
		numBits = palDat[offset++] - MINID;
		shadeMethod = palDat[offset++];
		SetMask(bitOffset);
		
		shadeColour = new uint[3];
		shadeColour[0] = palDat[offset++];
		shadeColour[1] = palDat[offset++];
		shadeColour[2] = palDat[offset++];
		
		shadeTint = new float[3];
		shadeTint[0] = (float)shadeColour[0] / 255.0f;
		shadeTint[1] = (float)shadeColour[1] / 255.0f;
		shadeTint[2] = (float)shadeColour[2] / 255.0f;
		
		shadeDat = new uint[(uint)System.Math.Pow(2, numBits)];
		for(uint i=0; i < shadeDat.Length; ++i)
			shadeDat[i] = palDat[offset++];
		
		shadeLevels = new float[shadeDat.Length];		
		for(uint i=0; i < shadeLevels.Length; ++i)
			shadeLevels[i] = (float)shadeDat[i] / 100.0f;
	}
	
	public void GetShade(uint blk, ref float[] colour)
	{
		float lvl = shadeLevels[BlkVal(blk)];
		switch (shadeMethod) 
		{
      case 0: // Multiply
        colour[0] = colour[0] + (shadeTint[0] - 1) * lvl * colour[0];
        colour[1] = colour[1] + (shadeTint[1] - 1) * lvl * colour[1];
        colour[2] = colour[2] + (shadeTint[2] - 1) * lvl * colour[2];
        break;
      case 1: // Blend
        colour[0] = colour[0] + (shadeTint[0] - colour[0]) * lvl;
        colour[1] = colour[1] + (shadeTint[1] - colour[1]) * lvl;
        colour[2] = colour[2] + (shadeTint[2] - colour[2]) * lvl;
        break;
		default:
			break;
		}
	}
	
}