from typing import Dict

from layaberr.version import __version__
from layaberr._validation import ValidationFailed, ModelCouldNotBeFound, add_bad_request_exception_handler, add_failed_validation_handler, add_model_could_not_be_found_handler
from layaberr._authorization import add_unauthorized_exception_handler, add_forbidden_exception_handler
from layaberr._default import add_exception_handler


def add_error_handlers(api) -> Dict[str, dict]:
    bad_request = add_bad_request_exception_handler(api)
    failed_validation = add_failed_validation_handler(api)
    model_could_not_be_found = add_model_could_not_be_found_handler(api)
    unauthorized = add_unauthorized_exception_handler(api)
    forbidden = add_forbidden_exception_handler(api)
    exception = add_exception_handler(api)

    return {
        "responses": {
            bad_request[0].value: (bad_request[1], bad_request[2]),
            failed_validation[0]: (failed_validation[1], failed_validation[2]),
            model_could_not_be_found[0]: (
                model_could_not_be_found[1],
                model_could_not_be_found[2],
            ),
            unauthorized[0].value: (unauthorized[1], unauthorized[2]),
            forbidden[0].value: (forbidden[1], forbidden[2]),
            exception[0].value: (exception[1], exception[2]),
        }
    }
