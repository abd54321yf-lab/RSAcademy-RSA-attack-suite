"""Backend protocol for interchangeable matchers."""
from typing import Protocol
from pathlib import Path
from rsa.fragment import RsaArtifact
class RsaBackend(Protocol):
    name: str
    def carve(self, path: Path, types=None) -> list[RsaArtifact]: ...
