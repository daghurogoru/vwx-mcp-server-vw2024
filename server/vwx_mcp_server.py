import json,os,sys,time,uuid
from pathlib import Path
root=Path(os.environ.get("VWX_MCP_BRIDGE_DIR",str(Path.home()/"Documents"/"Vectorworks"/"VWX-MCP-Bridge"))); q=root/"commands"; r=root/"responses"
tools=["document_info","list_layers","list_selection","create_rectangle","set_active_layer","delete_selection","save_document"]
def call(op,args):
 q.mkdir(parents=True,exist_ok=True);r.mkdir(parents=True,exist_ok=True);i=str(uuid.uuid4());t=q/(i+".tmp");t.write_text(json.dumps({"operation":op,"arguments":args}));t.replace(q/(i+".json"));out=r/(i+".json");end=time.time()+45
 while time.time()<end:
  if out.exists(): d=json.loads(out.read_text());out.unlink();return d
  time.sleep(.1)
 return {"ok":False,"error":"Run VWX MCP Bridge Process Queue in Vectorworks 2024."}
for line in sys.stdin:
 try:
  x=json.loads(line);m=x.get("method");i=x.get("id")
  if m=="notifications/initialized":continue
  if m=="initialize":z={"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"vwx-mcp-server-vw2024","version":"0.1.0"}}
  elif m=="tools/list":z={"tools":[{"name":"vwx_"+n,"description":n.replace("_"," "),"inputSchema":{"type":"object","properties":{}}} for n in tools]}
  elif m=="tools/call":
   p=x["params"];d=call(p["name"].replace("vwx_",""),p.get("arguments",{}));z={"content":[{"type":"text","text":json.dumps(d)}],"isError":not d.get("ok",False)}
  else:continue
  print(json.dumps({"jsonrpc":"2.0","id":i,"result":z}),flush=True)
 except Exception as e: print(json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32603,"message":str(e)}}),flush=True)
