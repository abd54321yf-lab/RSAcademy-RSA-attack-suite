"""Single-file and batch orchestration."""
from pathlib import Path
from time import perf_counter
from backends import get_backend
from output.reports import report_payload, write_json, write_html, write_ascii

def rsa_one(path, output_dir, backend='python', types=None):
    path=Path(path); out=Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    started=perf_counter(); artifacts=get_backend(backend).carve(path, types); payload=report_payload(path, artifacts, backend, perf_counter()-started)
    ext=out/'extracted_files'; ext.mkdir(exist_ok=True)
    for i,a in enumerate(artifacts,1):
        data=path.read_bytes()[a.offset:a.offset+a.size]; target=ext/f'file_{i:03d}_0x{a.offset:08X}{a.extension}'; target.write_bytes(data); a.extracted_path=str(target)
    payload=report_payload(path, artifacts, backend, perf_counter()-started)
    write_json(payload,out/'report.json'); write_html(payload,out/'report.html'); write_ascii(payload,out/'disk_map.txt')
    return payload

def discover(directory, patterns=None, recursive=False):
    root=Path(directory); patterns=patterns or ['*']; files=[]
    for pattern in patterns: files.extend(root.rglob(pattern) if recursive else root.glob(pattern))
    return sorted({p.resolve() for p in files if p.is_file() and p.stat().st_size > 0})

def rsa_many(paths, output_root, backend='python', types=None):
    root=Path(output_root); results=[]; errors=[]
    for path in paths:
        try: results.append(rsa_one(path, root/path.stem, backend, types))
        except Exception as exc: errors.append({'path':str(path),'status':'error','error_type':type(exc).__name__,'message':str(exc)})
    summary={'project':'RSAcademy - RSA attack suite','total_images_processed':len(results)+len(errors),'successful':len(results),'errors':errors,'total_artifacts':sum(len(r['artifacts']) for r in results),'results':results}
    import json
    root.mkdir(parents=True,exist_ok=True); (root/'batch_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return summary
