"""Self-contained report writers."""
from pathlib import Path
import json, html
from analysis.forensics import source_metadata, anomalies
from map.builder import build_map, ascii_map

def report_payload(path, artifacts, backend='python', elapsed=0.0):
    p=Path(path); meta=source_metadata(p)
    return {'project':'RSAcademy - RSA attack suite','source':meta,'backend':backend,'extracted_files_count':len(artifacts),'artifacts':[a.to_dict() for a in artifacts],'offset_map':build_map(artifacts,meta['size']),'warnings':anomalies(artifacts,meta['size']),'execution_seconds':round(elapsed,4)}

def write_json(payload, path):
    Path(path).write_text(json.dumps(payload, indent=2), encoding='utf-8')

def write_ascii(payload, path):
    arts=payload['artifacts']; lines=[f"RSAcademy | {payload['source']['path']}",f"Backend: {payload['backend']} | Artifacts: {len(arts)}",f"Map: {ascii_map(payload['offset_map'])}"]
    lines += [f"- 0x{a['offset']:08X} {a['extension']} {a['size']} bytes {a['validation_status']} entropy={a['entropy']}" for a in arts]
    Path(path).write_text('\n'.join(lines)+'\n', encoding='utf-8')

def write_html(payload, path):
    s=payload['source']; rows=''.join(f"<tr><td>0x{a['offset']:X}</td><td>{html.escape(a['file_type'])}</td><td>{a['size']}</td><td>{a['validation_status']}</td><td>{a['entropy']}</td><td><code>{a['md5']}</code></td></tr>" for a in payload['artifacts'])
    warnings=''.join(f"<li>{html.escape(w['message'])}</li>" for w in payload['warnings']) or '<li>None</li>'
    doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>RSAcademy Forensic Report</title><style>body{{font:15px system-ui;margin:0;background:#0b1220;color:#e5e7eb}}main{{max-width:1100px;margin:auto;padding:32px}}.card{{background:#111b2e;border:1px solid #24324d;border-radius:14px;padding:20px;margin:16px 0}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #293852;text-align:left}}code{{color:#93c5fd}}.map{{letter-spacing:3px;color:#34d399;font-size:20px}}</style></head><body><main><h1>RSAcademy Forensic Report</h1><p>Signature-based recovery and digital forensics analysis.</p><section class="card"><h2>Source</h2><p><b>Path:</b> {html.escape(s['path'])}<br><b>Size:</b> {s['size']} bytes<br><b>SHA-256:</b> <code>{s['sha256']}</code><br><b>Backend:</b> {payload['backend']}</p></section><section class="card"><h2>Offset Distribution</h2><div class="map">{ascii_map(payload['offset_map'])}</div></section><section class="card"><h2>Artifacts ({len(payload['artifacts'])})</h2><table><tr><th>Offset</th><th>Type</th><th>Size</th><th>Status</th><th>Entropy</th><th>MD5</th></tr>{rows}</table></section><section class="card"><h2>Warnings & anomalies</h2><ul>{warnings}</ul></section></main></body></html>'''
    Path(path).write_text(doc, encoding='utf-8')
