"""Format-aware validators using standard-library checks."""
from .signature import FileSignature

def validate(data: bytes, signature: FileSignature) -> tuple[bool, str]:
    """Validate header/footer and basic format structure."""
    if not data.startswith(signature.header): return False, 'header-mismatch'
    if signature.footer and not data.endswith(signature.footer): return False, 'footer-missing-or-truncated'
    if signature.extension == '.png' and len(data) < 33: return False, 'png-too-short'
    if signature.extension == '.pdf' and b'%%EOF' not in data[-1024:]: return False, 'pdf-eof-not-near-end'
    if signature.extension == '.jpg' and len(data) < 4: return False, 'jpeg-too-short'
    return True, 'valid'
