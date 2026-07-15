import json,os
from pathlib import Path
import vs
root=Path(os.environ.get("VWX_MCP_BRIDGE_DIR",str(Path.home()/"Documents"/"Vectorworks"/"VWX-MCP-Bridge")));q=root/"commands";r=root/"responses"
def run(op,a):
 if op=="document_info":return {"ok":True,"document":vs.GetFName(),"activeLayer":vs.GetLName(vs.ActLayer())}
 if op=="list_layers":
  x=[];h=vs.FLayer()
  while h:x.append({"name":vs.GetLName(h)});h=vs.NextLayer(h)
  return {"ok":True,"layers":x}
 if op=="list_selection":return {"ok":True,"objects":[]}
 if op=="create_rectangle":x,y,w,h=map(float,(a["x"],a["y"],a["width"],a["height"]));vs.Rect(x,y,x+w,y+h);return {"ok":True}
 if op=="set_active_layer":vs.Layer(a["name"]);return {"ok":True}
 if op=="delete_selection":vs.DelSelectedObj();return {"ok":True}
 if op=="save_document":vs.SaveActiveDocument();return {"ok":True}
for f in sorted(q.glob("*.json")):
 try:x=json.loads(f.read_text());a=run(x["operation"],x.get("arguments",{}))
 except Exception as e:a={"ok":False,"error":str(e)}
 t=r/(f.stem+".tmp");r.mkdir(parents=True,exist_ok=True);t.write_text(json.dumps(a));t.replace(r/(f.stem+".json"));f.unlink()
