"""Core carving pipeline independent from CLI and reporting."""
from pathlib import Path
from .reader import BinaryReader
from .signature import get_signatures
from .matcher import scan
from .validator import validate
from .fragment import make_artifact, resolve_overlaps

class PythonRsaEngine:
    """Pure Python backend for signature-based file carving."""
    name = 'python'
    def carve(self, path: Path, types=None):
        reader = BinaryReader(path)
        data = path.read_bytes()
        artifacts=[]
        for match in scan(reader, get_signatures(types)):
            chunk = data[match.offset:match.end_offset]
            ok, status = validate(chunk, match.signature)
            artifacts.append(make_artifact(path, match.offset, chunk, match.signature, status, match.truncated))
        return resolve_overlaps(artifacts)
