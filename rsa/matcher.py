"""Pure Python header/footer matcher."""
from dataclasses import dataclass
from .signature import FileSignature
from .reader import BinaryReader

@dataclass
class Match:
    signature: FileSignature
    offset: int
    end_offset: int
    truncated: bool = False

def find_all(data: bytes, signatures: list[FileSignature]) -> list[Match]:
    """Find bounded header-to-footer ranges in an in-memory byte sequence."""
    matches = []
    for sig in signatures:
        start = 0
        while True:
            offset = data.find(sig.header, start)
            if offset < 0: break
            limit = min(len(data), offset + sig.max_size)
            footer = data.find(sig.footer, offset + len(sig.header)) if sig.footer else -1
            if footer >= 0 and footer + len(sig.footer) <= limit:
                end = footer + len(sig.footer); truncated = False
            else:
                end = limit; truncated = True
            matches.append(Match(sig, offset, end, truncated))
            start = offset + max(1, len(sig.header))
    return sorted(matches, key=lambda m: (m.offset, m.end_offset))

def scan(reader: BinaryReader, signatures: list[FileSignature]) -> list[Match]:
    """Scan a file once and apply the deterministic matcher."""
    return find_all(reader.path.read_bytes(), signatures)
