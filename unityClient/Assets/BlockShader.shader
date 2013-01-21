Shader "Custom/BlockShader" {
	SubShader {
	Tags { "Queue"="Transparent" "RenderType"="Transparent" }
		Pass {
		Blend One Zero
		CGPROGRAM
		#pragma vertex vert
		#pragma fragment frag
		#include "UnityCG.cginc"
		
		struct appdata {
		    float4 vertex : POSITION;
		    float4 color : COLOR0;
		};
		
		struct v2f {
		    float4 pos : SV_POSITION;
		    float4 color : COLOR0;
		    float3 tex : TEXCOORD;
		};
		
		v2f vert (appdata v) 
		{
		    v2f o;
		    o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
		    o.color = v.color;
		    o.tex.rgb = v.vertex.xyz;
		    return o;
		}
		
		half4 frag (v2f i) : COLOR
		{
			clip(i.color.a - 0.99);
			i.color.rgb = i.color.rgb * 0.9 + frac(i.tex - 0.5) * 0.1;
		    return i.color;
		}
		ENDCG		
	    }
	    
	    
	    Pass {
		Blend One OneMinusSrcAlpha
		ZWrite Off
		CGPROGRAM
		#pragma vertex vert
		#pragma fragment frag
		#include "UnityCG.cginc"
		
		struct appdata {
		    float4 vertex : POSITION;
		    float4 color : COLOR0;
		    float4 tex : TEXCOORD0; 
		};
		
		struct v2f {
		    float4 pos : SV_POSITION;
		    float4 color : COLOR0;
		    float4 tex : TEXCOORD;
		};
		
		v2f vert (appdata v)
		{
		    v2f o;
		    o.pos = mul(UNITY_MATRIX_MVP, v.vertex);
		    o.color = v.color;
		    o.color.rga = o.color.rga * o.color.a;
		    o.tex = v.tex; 
		    return o;
		}
		
		half4 frag (v2f i) : COLOR
		{
			clip(0.99 - i.color.a);
			i.color.rgb = i.color.rgb - (i.color.rgb * (step(0.001,i.tex.y) - step(0.1,i.tex.y))) * 0.1;
		    return i.color;
		}
		ENDCG		
	    }
	}
	Fallback "VertexLit"
} 