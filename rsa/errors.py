"""Domain errors used by the forensic pipeline."""
class RSAError(Exception):
    """Base exception for recoverable RSAcademy errors."""
class InputError(RSAError):
    """Input path is missing, unreadable, or empty."""
class BackendError(RSAError):
    """A selected matching backend could not run."""
class ValidationError(RSAError):
    """An artifact failed structural validation."""
