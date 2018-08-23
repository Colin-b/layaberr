import logging
import sys
import unittest

logging.basicConfig(
    format='%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG)
logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

from werkzeug.exceptions import Unauthorized

from pycommon_error import validation, authorization, default

logger = logging.getLogger(__name__)


class FlaskRestPlusExceptionsTest(unittest.TestCase):
    def setUp(self):
        logger.info(f'-------------------------------')
        logger.info(f'Start of {self._testMethodName}')

    def tearDown(self):
        logger.info(f'End of {self._testMethodName}')
        logger.info(f'-------------------------------')

    def test_handle_exception_failed_validation_on_list_of_items(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    # Mock of the input (List of items)
                    received_data = [{'optional_string_value': 'my_value1', 'mandatory_integer_value': 1,
                                      'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23',
                                      'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                      'optional_float_value': 100},
                                     {'optional_string_value': 'my_value2', 'optional_enum_value': 'First Enum Value',
                                      'optional_date_value': '2017-10-23',
                                      'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                      'optional_float_value': 200}]
                    failed_validation = validation.ValidationFailed(received_data)
                    errors = {1: {'mandatory_integer_value': ['Missing data for required field.']}}
                    setattr(failed_validation, 'errors', errors)
                    # Call handle_exception method
                    result = func(failed_validation)
                    # Assert output, if NOK will raise Assertion Error
                    assert (result[0] == {
                        'fields': [
                            {
                                'item': 2,
                                'field_name': 'mandatory_integer_value',
                                'messages': ['Missing data for required field.']
                            }
                        ]
                    })
                    assert (result[1] == 400)
                    return result

                return wrapper

        # Since TestApi is not completely mocked, add_failed_validation_handler will raise a "NoneType is not iterable
        # exception after the call to handle_exception. Exception is therefore ignored
        try:
            validation.add_failed_validation_handler(TestAPI)
        except TypeError:
            pass

    def test_handle_exception_failed_validation_a_single_item(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    # Mock of the input (Single item)
                    received_data = {'optional_string_value': 'my_value1', 'mandatory_integer_value': 1,
                                     'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23',
                                     'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                     'optional_float_value': 100}, {'optional_string_value': 'my_value2',
                                                                    'optional_enum_value': 'First Enum Value',
                                                                    'optional_date_value': '2017-10-23',
                                                                    'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                                                    'optional_float_value': 200}
                    failed_validation = validation.ValidationFailed(received_data)
                    errors = {'mandatory_integer_value': ['Missing data for required field.']}
                    setattr(failed_validation, 'errors', errors)
                    # Call handle_exception method
                    result = func(failed_validation)
                    # Assert output, if NOK will raise Assertion Error
                    assert (result[0] == {'fields': [
                        {'item': 1, 'field_name': 'mandatory_integer_value',
                         'messages': ['Missing data for required field.']}]})
                    assert (result[1] == 400)
                    return result

                return wrapper

        # Since TestApi is not completely mocked, add_failed_validation_handler will raise a "NoneType is not iterable
        # exception after the call to handle_exception. Exception is therefore ignored
        try:
            validation.add_failed_validation_handler(TestAPI)
        except TypeError:
            pass

    def test_handle_exception_model_not_found(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    # Mock of the input (Single item)
                    row = {'value': 'my_value1'}
                    no_model = validation.ModelCouldNotBeFound(row)
                    # Call handle_exception method
                    result = func(no_model)
                    # Assert output, if NOK will raise Assertion Error
                    assert (result[0] == {'message': 'Corresponding model could not be found.'})
                    assert (result[1] == 404)
                    return result

                return wrapper

        # Since TestApi is not completely mocked, add_failed_validation_handler will raise a "NoneType is not iterable
        # exception after the call to handle_exception. Exception is therefore ignored
        try:
            validation.add_model_could_not_be_found_handler(TestAPI)
        except TypeError:
            pass

    def test_handle_unauthorized_exception(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def raise_error():
                raise Unauthorized

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    result = func('Access Unauthorized')
                    assert (result[0] == {'message': 'Access Unauthorized'})
                    assert (result[1] == 401)
                    return result

                return wrapper

        try:
            authorization.add_unauthorized_exception_handler(TestAPI)
        except TypeError:
            pass

    def test_handle_bad_request_exception(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def raise_error():
                raise Unauthorized

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    result = func('Input payload validation failed')
                    assert (result[0] == {'message': 'Input payload validation failed'})
                    assert (result[1] == 400)
                    return result

                return wrapper

        try:
            validation.add_bad_request_exception_handler(TestAPI)
        except TypeError:
            pass

    def test_default_handler(self):
        class TestAPI:

            @staticmethod
            def model(cls, name):
                pass

            @staticmethod
            def errorhandler(cls):
                pass

            @staticmethod
            def raise_error():
                raise Unauthorized

            @staticmethod
            def marshal_with(cls, code):
                def wrapper(func):
                    result = func('Internal Server Error')
                    assert (result[0] == {'message': 'Internal Server Error'})
                    assert (result[1] == 500)
                    return result

                return wrapper

        try:
            default.add_exception_handler(TestAPI)
        except TypeError:
            pass
