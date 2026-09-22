"""Artifact model and overlap resolution."""
from dataclasses import dataclass, asdict
from pathlib import Path
from .signature import FileSignature
from .entropy import shannon_entropy, entropy_label
import hashlib

@dataclass
class RsaArtifact:
    """A carved byte range and its forensic metadata."""
    source: str; offset: int; size: int; file_type: str; extension: str
    validation_status: str; md5: str; sha256: str; entropy: float; entropy_class: str
    truncated: bool = False; extracted_path: str = ''
    def to_dict(self): return asdict(self)

def make_artifact(source: Path, offset: int, data: bytes, signature: FileSignature, status: str, truncated: bool) -> RsaArtifact:
    return RsaArtifact(str(source), offset, len(data), signature.name, signature.extension,
        status, hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest(),
        round(shannon_entropy(data), 4), entropy_label(shannon_entropy(data)), truncated)

def resolve_overlaps(artifacts: list[RsaArtifact]) -> list[RsaArtifact]:
    """Keep the first range when two matches overlap."""
    result=[]; end=-1
    for artifact in sorted(artifacts, key=lambda x: (x.offset, -x.size)):
        if artifact.offset >= end:
            result.append(artifact); end = artifact.offset + artifact.size
    return result
