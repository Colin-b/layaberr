from layaberr.version import __version__
from layaberr._validation import (
    ValidationFailed,
    validation_failed_exception,
    ModelCouldNotBeFound,
    model_could_not_be_found_exception,
)
from layaberr._authorization import Unauthorized, Forbidden
from layaberr._default import http_exception, exception


exception_handlers = {
    ValidationFailed: validation_failed_exception,
    ModelCouldNotBeFound: model_could_not_be_found_exception,
    Unauthorized: http_exception,
    Forbidden: http_exception,
    Exception: exception,
}
