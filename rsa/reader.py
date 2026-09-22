"""Bounded binary reading helpers."""
from pathlib import Path
from dataclasses import dataclass
from .errors import InputError

@dataclass
class BinaryReader:
    """Reads a file in bounded chunks without loading it all into memory."""
    path: Path
    block_size: int = 1024 * 1024
    def __post_init__(self):
        self.path = Path(self.path)
        if not self.path.is_file():
            raise InputError(f"File not found: {self.path}")
        if self.path.stat().st_size == 0:
            raise InputError(f"Zero-byte input: {self.path}")
    @property
    def size(self) -> int:
        return self.path.stat().st_size
    def read_at(self, offset: int, length: int) -> bytes:
        if offset < 0 or length < 0 or offset > self.size:
            raise InputError(f"Invalid offset or length: {offset}, {length}")
        with self.path.open('rb') as stream:
            stream.seek(offset)
            return stream.read(length)
    def chunks(self):
        with self.path.open('rb') as stream:
            offset = 0
            while True:
                data = stream.read(self.block_size)
                if not data:
                    break
                yield offset, data
                offset += len(data)
