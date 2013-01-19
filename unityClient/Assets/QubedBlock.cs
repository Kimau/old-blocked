using System.Collections.Generic;

public class QubedBlock
{
	struct QBlkLink { uint artID; uint blkID; };
	struct QBit 
	{ 
		bool solid;
		uint linkID;
		uint[] palDat;
	};
	
	QBit[,,]    qBits;
	List<QubedPal> qPal;
	List<QBlkLink> qBlockLinks;
	uint        blockSize;	
		
	public uint NumBits 
	{ 
		get 
		{ 
			uint c = 0; 
			foreach(QubedPal p in qPal)
				c += p.NumBits; 
			
			return c;
		}
	}
	
	public QubedBlock()
	{
		QubedBlock(8);
	}
	
	public QubedBlock(uint blkSize)
	{
		blockSize = blkSize;
		
		qBits = new QBit[blockSize,blockSize,blockSize];
		qPal = new List<QubedPal>();
		qBlockLinks = new List<QBlkLink>();
	}
}