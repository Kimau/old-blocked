using UnityEngine;
using System.Collections.Generic;

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
		
		List<int> jobLot = new List<int>();
		int maxLimit = 512;
		for(int i=0; i < maxLimit; ++i)
		{
			if(qBlock.BlockVisible(i))
			{
				int x = i % 8;
				int y = (i % 64) / 8;
				int z = (i / 64);	
					
				if((x < 1) || (qBlock.BlockVisible(i-1) == false))
					jobLot.Add(i*6 + 0);
				if((x > 6) || (qBlock.BlockVisible(i+1) == false))
					jobLot.Add(i*6 + 1);
				if((y < 1) || (qBlock.BlockVisible(i-8) == false))
					jobLot.Add(i*6 + 2);
				if((y > 6) || (qBlock.BlockVisible(i+8) == false))
					jobLot.Add(i*6 + 3);
				if((z < 1) || (qBlock.BlockVisible(i-64) == false))
					jobLot.Add(i*6 + 4);
				if((z > 6) || (qBlock.BlockVisible(i+64) == false))
					jobLot.Add(i*6 + 5);
			}
		}
		
		// 		
		Vector3[] newVert  = new Vector3[jobLot.Count * 4];
		Vector3[] newNorm  = new Vector3[jobLot.Count * 4];
		Color[] newColours = new Color[jobLot.Count * 4];
		Vector2[] newUV    = new Vector2[jobLot.Count * 4];
		int[] newTri       = new int[jobLot.Count * 6];
		
		//
		for(int i=0; i < jobLot.Count; ++i)
		{			
			int b = (jobLot[i] / 6);
			if(qBlock.BlockVisible(b) == false)
				continue;
			
			int x = b % 8;
			int y = (b % 64) / 8;
			int z = (b / 64);			
			int v = i*4;
			int t = i*6;
			
			// Make Triangles
			newTri[t+0] = v+1;
			newTri[t+1] = v+2;
			newTri[t+2] = v+3;
			newTri[t+3] = v+2;
			newTri[t+4] = v+1;
			newTri[t+5] = v+0;
			
			// Make Verts			
			newUV[v+0] = new Vector2(0.0f, 0.0f);
			newUV[v+1] = new Vector2(1.0f, 0.0f);
			newUV[v+2] = new Vector2(0.0f, 1.0f);
			newUV[v+3] = new Vector2(1.0f, 1.0f);
			
			float[] colVals = qBlock.BlockColour(b);
			float alpha = qBlock.BlockAlpha(b);
			Color newCol = new Color(colVals[0], colVals[1], colVals[2], alpha);
			
			newColours[v+0] = newCol;
			newColours[v+1] = newCol;
			newColours[v+2] = newCol;
			newColours[v+3] = newCol;
			
			switch((jobLot[i] % 6))
			{
			case 0: // -X
				newVert[v+0] = new Vector3(x - 0.5f, y + 0.5f, z + 0.5f); // 0
				newVert[v+1] = new Vector3(x - 0.5f, y - 0.5f, z + 0.5f); // 1
				newVert[v+2] = new Vector3(x - 0.5f, y + 0.5f, z - 0.5f); // 2
				newVert[v+3] = new Vector3(x - 0.5f, y - 0.5f, z - 0.5f); // 3
				
				newNorm[v+0] = Vector3.left;
				newNorm[v+1] = Vector3.left;
				newNorm[v+2] = Vector3.left;
				newNorm[v+3] = Vector3.left;
				break;
				
			case 1: // +X
				newVert[v+0] = new Vector3(x + 0.5f, y + 0.5f, z - 0.5f); // 0
				newVert[v+1] = new Vector3(x + 0.5f, y - 0.5f, z - 0.5f); // 1
				newVert[v+2] = new Vector3(x + 0.5f, y + 0.5f, z + 0.5f); // 2
				newVert[v+3] = new Vector3(x + 0.5f, y - 0.5f, z + 0.5f); // 3
				
				newNorm[v+0] = Vector3.right;
				newNorm[v+1] = Vector3.right;
				newNorm[v+2] = Vector3.right;
				newNorm[v+3] = Vector3.right;
				break;
			case 2: // -Y
				newVert[v+0] = new Vector3(x - 0.5f, y - 0.5f, z + 0.5f); // 0
				newVert[v+1] = new Vector3(x + 0.5f, y - 0.5f, z + 0.5f); // 1
				newVert[v+2] = new Vector3(x - 0.5f, y - 0.5f, z - 0.5f); // 2
				newVert[v+3] = new Vector3(x + 0.5f, y - 0.5f, z - 0.5f); // 3
				
				newNorm[v+0] = Vector3.down;
				newNorm[v+1] = Vector3.down;
				newNorm[v+2] = Vector3.down;
				newNorm[v+3] = Vector3.down;
				break;
			case 3: // +Y
				newVert[v+0] = new Vector3(x - 0.5f, y + 0.5f, z - 0.5f); // 0
				newVert[v+1] = new Vector3(x + 0.5f, y + 0.5f, z - 0.5f); // 1
				newVert[v+2] = new Vector3(x - 0.5f, y + 0.5f, z + 0.5f); // 2
				newVert[v+3] = new Vector3(x + 0.5f, y + 0.5f, z + 0.5f); // 3
				
				newNorm[v+0] = Vector3.up;
				newNorm[v+1] = Vector3.up;
				newNorm[v+2] = Vector3.up;
				newNorm[v+3] = Vector3.up;
				break;
			case 4: // -Z
				newVert[v+0] = new Vector3(x - 0.5f, y - 0.5f, z - 0.5f); // 0
				newVert[v+1] = new Vector3(x + 0.5f, y - 0.5f, z - 0.5f); // 1
				newVert[v+2] = new Vector3(x - 0.5f, y + 0.5f, z - 0.5f); // 2
				newVert[v+3] = new Vector3(x + 0.5f, y + 0.5f, z - 0.5f); // 3
				
				newNorm[v+0] = Vector3.back;
				newNorm[v+1] = Vector3.back;
				newNorm[v+2] = Vector3.back;
				newNorm[v+3] = Vector3.back;
				break;
			case 5: // +Z
				newVert[v+0] = new Vector3(x - 0.5f, y + 0.5f, z + 0.5f); // 0
				newVert[v+1] = new Vector3(x + 0.5f, y + 0.5f, z + 0.5f); // 1
				newVert[v+2] = new Vector3(x - 0.5f, y - 0.5f, z + 0.5f); // 2
				newVert[v+3] = new Vector3(x + 0.5f, y - 0.5f, z + 0.5f); // 3
				
				newNorm[v+0] = Vector3.forward;
				newNorm[v+1] = Vector3.forward;
				newNorm[v+2] = Vector3.forward;
				newNorm[v+3] = Vector3.forward;
				break;
			}
		}
		
		Mesh newMesh = new Mesh();
		newMesh.vertices = newVert;
		newMesh.normals = newNorm;
		newMesh.uv = newUV;
		newMesh.colors = newColours;
		newMesh.triangles = newTri;
		
		newMesh.MarkDynamic();
		newMesh.RecalculateBounds();
		newMesh.Optimize();
		
		mf.mesh = newMesh;
	}
}
