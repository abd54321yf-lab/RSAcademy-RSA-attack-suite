"""File signature models and the built-in signature catalogue."""
from dataclasses import dataclass, field
from typing import Callable, Optional

@dataclass(frozen=True)
class FileSignature:
    """Describes a file header/footer and safe carving limits."""
    name: str
    extension: str
    header: bytes
    footer: bytes = b""
    max_size: int = 64 * 1024 * 1024
    validator: Optional[Callable[[bytes], bool]] = field(default=None, compare=False, repr=False)

    def matches_header(self, data: bytes, offset: int = 0) -> bool:
        return data.startswith(self.header, offset)

SIGNATURES = [
    FileSignature("JPEG image", ".jpg", b"\xff\xd8\xff", b"\xff\xd9", 32 * 1024 * 1024),
    FileSignature("PNG image", ".png", b"\x89PNG\r\n\x1a\n", b"IEND\xaeB`\x82", 64 * 1024 * 1024),
    FileSignature("PDF document", ".pdf", b"%PDF-", b"%%EOF", 128 * 1024 * 1024),
    FileSignature("ZIP archive", ".zip", b"PK\x03\x04", b"PK\x05\x06", 256 * 1024 * 1024),
    FileSignature("GIF image", ".gif", b"GIF8", b";", 32 * 1024 * 1024),
]

def get_signatures(names: Optional[list[str]] = None) -> list[FileSignature]:
    """Return all signatures or only extensions/names selected by the caller."""
    if not names:
        return list(SIGNATURES)
    wanted = {n.lower().lstrip('.') for n in names}
    return [s for s in SIGNATURES if s.extension.lstrip('.') in wanted or s.name.lower() in wanted]
