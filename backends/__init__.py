"""Backend factory."""
from rsa.engine import PythonRsaEngine
from rsa.errors import BackendError

def get_backend(name: str = 'python'):
    if name == 'python': return PythonRsaEngine()
    if name == 'yara':
        try:
            import yara  # type: ignore
        except ImportError as exc:
            raise BackendError('YARA backend requested but yara-python is not installed') from exc
        raise BackendError('YARA backend is optional and requires a configured ruleset')
    raise BackendError(f'Unknown backend: {name}')
