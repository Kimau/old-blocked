using UnityEngine;
using System.Collections;

public class QubeToMesh : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}
	
	public void setQube(QubedBlock qBlock)
	{
		MeshFilter mf = GetComponent<MeshFilter>();
		
		int numSolidBits = 0;
		for(uint i=0; i < 512; ++i)
			if(qBlock.IsVisible(i))
				++numSolidBits;
		
		// 
		
		Vector3[] newVert = new Vector3[numSolidBits * 8];
		int[] newTri      = new int[numSolidBits * 12 * 3];
		Vector2[] newUV   = new Vector2[numSolidBits * 8];
		Color[] newColours= new Color[numSolidBits * 8];
		
		//
		int v = 0;
		int t = 0;
		for(uint i=0; i < 512; ++i)
		{		
			if(qBlock.IsVisible(i) == false)
				continue;
			
			uint x = i % 8;
			uint y = (i % 64) / 8;
			uint z = (i / 64);
			
			// Make Triangles
			// Z-
			newTri[t++] = v+1;
			newTri[t++] = v+2;
			newTri[t++] = v+3;
			newTri[t++] = v+2;
			newTri[t++] = v+1;
			newTri[t++] = v+0;
			
			// Z+
			newTri[t++] = v+4;
			newTri[t++] = v+5;
			newTri[t++] = v+6;
			newTri[t++] = v+7;
			newTri[t++] = v+6;
			newTri[t++] = v+5;
			
			//  Y-
			newTri[t++] = v+0;
			newTri[t++] = v+1;
			newTri[t++] = v+4;
			newTri[t++] = v+5;
			newTri[t++] = v+4;
			newTri[t++] = v+1;
			
			//  Y+
			newTri[t++] = v+3;
			newTri[t++] = v+6;
			newTri[t++] = v+7;
			newTri[t++] = v+6;
			newTri[t++] = v+3;
			newTri[t++] = v+2;
			
			//  X-
			newTri[t++] = v+2;
			newTri[t++] = v+4;		
			newTri[t++] = v+6;
			newTri[t++] = v+4;
			newTri[t++] = v+2;
			newTri[t++] = v+0;
			
			//  X+
			newTri[t++] = v+1;
			newTri[t++] = v+3;
			newTri[t++] = v+5;
			newTri[t++] = v+7;
			newTri[t++] = v+5;
			newTri[t++] = v+3;
						
			// Make Verts			
			newUV[v+0] = new Vector2(0.0f, 0.0f);
			newUV[v+1] = new Vector2(0.3f, 0.0f);
			newUV[v+2] = new Vector2(0.6f, 0.0f);
			newUV[v+3] = new Vector2(0.0f, 0.0f);
			newUV[v+4] = new Vector2(0.0f, 1.0f);
			newUV[v+5] = new Vector2(0.3f, 1.0f);
			newUV[v+6] = new Vector2(0.6f, 1.0f);
			newUV[v+7] = new Vector2(1.0f, 1.0f);
			
			float[] colVals = qBlock.GetColour(i);
			float alpha = qBlock.GetAlpha(i);
			Color newCol = new Color(colVals[0], colVals[1], colVals[2], alpha);
			
			newColours[v+0] = newCol;
			newColours[v+1] = newCol;
			newColours[v+2] = newCol;
			newColours[v+3] = newCol;
			newColours[v+4] = newCol;
			newColours[v+5] = newCol;
			newColours[v+6] = newCol;
			newColours[v+7] = newCol;
			
			newVert[v++] = new Vector3(x - 0.5f, y - 0.5f, z - 0.5f); // 0
			newVert[v++] = new Vector3(x + 0.5f, y - 0.5f, z - 0.5f); // 1
			newVert[v++] = new Vector3(x - 0.5f, y + 0.5f, z - 0.5f); // 2
			newVert[v++] = new Vector3(x + 0.5f, y + 0.5f, z - 0.5f); // 3
			newVert[v++] = new Vector3(x - 0.5f, y - 0.5f, z + 0.5f); // 4
			newVert[v++] = new Vector3(x + 0.5f, y - 0.5f, z + 0.5f); // 5
			newVert[v++] = new Vector3(x - 0.5f, y + 0.5f, z + 0.5f); // 6
			newVert[v++] = new Vector3(x + 0.5f, y + 0.5f, z + 0.5f); // 7
		}
		
		Mesh newMesh = new Mesh();
		newMesh.vertices = newVert;
		newMesh.uv = newUV;
		newMesh.colors = newColours;
		newMesh.triangles = newTri;
		newMesh.MarkDynamic();
		newMesh.RecalculateNormals();
		newMesh.RecalculateBounds();
		
		mf.mesh = newMesh;
	}
}
