"""Forensic metadata and anomaly analysis."""
from pathlib import Path
import hashlib
from rsa.entropy import shannon_entropy

def source_metadata(path: Path) -> dict:
    data = path.read_bytes()
    return {'path': str(path), 'size': len(data), 'md5': hashlib.md5(data).hexdigest(), 'sha256': hashlib.sha256(data).hexdigest(), 'entropy': round(shannon_entropy(data), 4)}

def anomalies(artifacts, source_size: int) -> list[dict]:
    warnings=[]
    for a in artifacts:
        if a.truncated: warnings.append({'offset': a.offset, 'type': 'truncated-artifact', 'message': f'{a.file_type} has no bounded footer'})
        if a.entropy >= 7.5: warnings.append({'offset': a.offset, 'type': 'high-entropy', 'message': 'High entropy range may indicate compression, encryption, or packed data'})
    return warnings
