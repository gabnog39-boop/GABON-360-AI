module.exports=async(req,res)=>{try{
 const m0=await (await fetch("https://www.geoboundaries.org/api/current/gbOpen/GAB/ADM0/")).json();
 const meta=Array.isArray(m0)?m0[0]:m0;const u=meta.simplifiedGeometryGeoJSON||meta.gjDownloadURL;
 const r=await fetch(u);if(!r.ok)throw new Error("HTTP "+r.status);const geo=await r.json();
 res.setHeader("Content-Type","application/json; charset=utf-8");res.setHeader("Cache-Control","s-maxage=86400");res.status(200).json({meta,geo})
}catch(e){res.status(502).json({error:{message:"geoBoundaries indisponible"}})}};
