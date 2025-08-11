from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import JSONResponse
import dns.resolver
import dns.rdatatype

app = FastAPI()

resolver = dns.resolver.Resolver()
resolver.timeout = 2
resolver.lifetime = 2

@app.get("/dns-query")
async def dns_query(
    name: str = Query(...),
    type: str = Query("A"),
    request: Request = None
):
    accept = request.headers.get("accept", "")
    if "application/dns-json" not in accept:
        raise HTTPException(status_code=406, detail="Not Acceptable")

    try:
        qtype = type.upper()
        result = resolver.resolve(name, qtype)
        return JSONResponse({
            "Status": 0,
            "TC": False,
            "RD": True,
            "RA": True,
            "AD": False,
            "CD": False,
            "Question": [{"name": name, "type": qtype}],
            "Answer": [
                {"name": name, "type": qtype, "TTL": r.ttl, "data": r.to_text()}
                for r in result
            ]
        })
    except Exception:
        return JSONResponse({"Status": 3, "Question": [{"name": name, "type": type}]})

@app.get("/")
async def root():
    return {"status": "DNS-over-HTTPS na Vercel"}
