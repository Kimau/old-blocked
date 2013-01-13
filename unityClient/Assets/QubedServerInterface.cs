using UnityEngine;
using System.Collections;
using System.Net;
using System.IO;

public class QubedServerInterface : MonoBehaviour
{
	CookieContainer myCookies;

	// Use this for initialization
	void Start()
	{
		myCookies = new CookieContainer();
		
		if(myCookies.Count < 1)
			GetAuthorityCookiesNOW();
		
		if(myCookies.Count > 0)
			Poke();
		else
			Debug.LogWarning("No Cookies :(");
	}
	
	// Update is called once per frame
	void Update()
	{
		
	}
	
	void GetAuthorityCookiesNOW()
	{
		string reqString = "http://localhost:9634/_ah/login?action=Login&continue=http%3A%2F%2Flocalhost%3A9634%2F";
		reqString += "&email=" + "boom%40example.com";
		
		HttpWebRequest webReq = (HttpWebRequest)WebRequest.Create(reqString);
		webReq.Referer = "http://localhost:9634/_ah/login";
		webReq.UserAgent = "Mozilla/5.0";
		webReq.CookieContainer = myCookies;
		
		HttpWebResponse webRep = (HttpWebResponse)webReq.GetResponse();
		if(webRep.StatusCode != HttpStatusCode.OK)
			Debug.LogError(webRep.StatusCode + "\n" + webRep.StatusDescription);
	}
	
	void Poke()
	{
		HttpWebRequest webReq = (HttpWebRequest)WebRequest.Create("http://localhost:9634/blockEditor");
		webReq.Referer = "http://localhost:9634/blockEditor";
		webReq.UserAgent = "Mozilla/5.0";
		webReq.ContentType = "application/qubed; base64";
		webReq.Headers.Add("aid", "1");
		webReq.Headers.Add("bid", "0");
		
		webReq.CookieContainer = myCookies;
		webReq.Method = "GET";
		
		HttpWebResponse webRep = (HttpWebResponse)webReq.GetResponse();
		if(webRep.StatusCode != HttpStatusCode.OK)
			Debug.LogError(webRep.StatusCode + "\n" + webRep.StatusDescription);
	
		// All Good
		Stream stream = webRep.GetResponseStream();
		BinaryReader binReader = new BinaryReader(stream);
		byte[] byteStr = binReader.ReadBytes((int)webRep.ContentLength);
		Debug.Log(byteStr);
		stream.Close();
	}
	/*
	void PostToGAE()
	{
		var auth = GetAuth();  							// I can get the authtoken
		var cookies = GetCookies(auth);  		// I can get the ACSID cookie

		var url = string.Format("http://localhost:9634/blockEditor");
		var content = "testvalue=test";
		HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
		request.KeepAlive = false;
		request.CookieContainer = cookies;
		byte[] byteArray = Encoding.UTF8.GetBytes(content);
		request.ContentLength = byteArray.Length;
		request.ContentType = "application/x-www-form-urlencoded";
		request.Method = "POST";
		Stream dataStream = request.GetRequestStream();
		dataStream.Write(byteArray, 0, byteArray.Length);
		dataStream.Close();
		HttpWebResponse response = (HttpWebResponse)request.GetResponse(); // This gives me 403
		Stream stream = response.GetResponseStream();
		StreamReader reader = new StreamReader(stream);
		string result = reader.ReadToEnd();
		reader.Close();
	}

	CookieContainer GetCookies(string auth)
	{
		CookieContainer cookies = new CookieContainer();
		var url = string.Format("http://test.appspot.com/_ah/login?auth={0}",
                            System.Web.HttpUtility.UrlEncode(auth));
		HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
		request.AllowAutoRedirect = false;
		request.CookieContainer = cookies;
		request.ContentType = "application/x-www-form-urlencoded";
		request.Method = "GET";
		HttpWebResponse response = (HttpWebResponse)request.GetResponse();
		Stream stream = response.GetResponseStream();
		StreamReader reader = new StreamReader(stream);
		string result = reader.ReadToEnd(); 
		reader.Close();
		return cookies;
	}

	string GetAuth()
	{
		HttpWebRequest request = (HttpWebRequest)WebRequest.Create("http://www.google.com/accounts/ClientLogin");
		var content = "Email=test@gmail.com&Passwd=testpass&service=ah&accountType=HOSTED_OR_GOOGLE";
		byte[] byteArray = Encoding.UTF8.GetBytes(content);
		request.ContentLength = byteArray.Length;
		request.ContentType = "application/x-www-form-urlencoded";
		request.Method = "POST";
		Stream dataStream = request.GetRequestStream();
		dataStream.Write(byteArray, 0, byteArray.Length);
		dataStream.Close();
		HttpWebResponse response = (HttpWebResponse)request.GetResponse();
		Stream stream = response.GetResponseStream();
		StreamReader reader = new StreamReader(stream);
		string loginStuff = reader.ReadToEnd();
		reader.Close();

		var auth = loginStuff.Substring(loginStuff.IndexOf("Auth")).Replace("Auth=", "").TrimEnd('\n');
		return auth;
	}
	*/
}
