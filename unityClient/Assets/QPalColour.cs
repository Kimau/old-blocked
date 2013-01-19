public class QPalColour : QubedPal
{
	const uint COLOURID = 10;
	
	uint numBits;
	
	public override uint NumBits { get { return numBits; } }
	public override uint PalID   { get { return COLOURID + numBits; } }
	
	public QPalColour()
	{
		numBits = 0;
	}
}