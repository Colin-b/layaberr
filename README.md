<h2 align="center">Exceptions handling for layab</h2>

<p align="center">
<a href="https://pypi.org/project/layaberr/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layaberr"></a>
<a href="https://travis-ci.org/Colin-b/layaberr"><img alt="Build status" src="https://api.travis-ci.org/Colin-b/layaberr.svg?branch=develop"></a>
<a href="https://travis-ci.org/Colin-b/layaberr"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.org/Colin-b/layaberr"><img alt="Number of tests" src="https://img.shields.io/badge/tests-14 passed-blue"></a>
<a href="https://pypi.org/project/layaberr/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layaberr"></a>
</p>

To be able to throw exceptions in your code and send a proper HTTP response automatically to your client your need to add error handler(s) to your API and endpoints.

## Add all handlers at once

```python
from flask_restplus import Resource
import layaberr

api = None # Your flask-restplus API instance
error_responses = layaberr.add_error_handlers(api)

@api.route("/your_endpoint")
@api.doc(**error_responses)
class YourFlaskRestPlusResource(Resource):
    def get(self):
        return "test"
```

## Add some handlers

```python
from flask_restplus import Resource
import layaberr

api = None # Your flask-restplus API instance
error_response = layaberr.add_failed_validation_handler(api)

@api.route("/your_endpoint")
class YourFlaskRestPlusResource(Resource):
    @api.response(error_response)
    def get(self):
        return "test"
```

## Supported Exceptions

The following exceptions are handled:

### ValidationFailed

In case your endpoint raises ValidationFailed, an HTTP error 400 (Bad Request) will be sent to the client.

#### Error not specific to a field in received data

This code:

```python
from layaberr import ValidationFailed

received_data = None
raise ValidationFailed(received_data, message="This is the error message")
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  1, "field_name":  "", "messages": ["This is the error message"]}]}
```

#### Error specific to a field in a received dictionary

This code:

```python
from layaberr import ValidationFailed

received_data = {"field 1": "value 1"}
raise ValidationFailed(received_data, errors={"field 1": ["Invalid value"]})
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  1, "field_name":  "field 1", "messages": ["Invalid value"]}]}
```

#### Error specific to a field in a received list of dictionaries

This code:

```python
from layaberr import ValidationFailed

received_data = [{"field 1": "value 1"}, {"field 1": "value 2"}]
raise ValidationFailed(received_data, errors={1: {"field 1": ["Invalid value"]}})
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  2, "field_name":  "field 1", "messages": ["Invalid value"]}]}
```

### ModelCouldNotBeFound

In case your endpoint raises ModelCouldNotBeFound, an HTTP error 404 (Not Found) will be sent to the client.

This code:

```python
from layaberr import ModelCouldNotBeFound

requested_data = None
raise ModelCouldNotBeFound(requested_data)
```

Will result in the following JSON response sent to the client:
```json
{"message":  "Corresponding model could not be found."}
```

### BadRequest

In case your endpoint raises BadRequest, an HTTP error 400 (Bad Request) will be sent to the client.

This code:

```python
from werkzeug.exceptions import BadRequest

raise BadRequest("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

### Unauthorized

In case your endpoint raises Unauthorized, an HTTP error 401 (Unauthorized) will be sent to the client.

This code:

```python
from werkzeug.exceptions import Unauthorized

raise Unauthorized("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

### Forbidden

In case your endpoint raises Forbidden, an HTTP error 403 (Forbidden) will be sent to the client.

This code:

```python
from werkzeug.exceptions import Forbidden

raise Forbidden("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

### Exception (this is the default handler)

In case your endpoint raises an Exception, an HTTP error 500 (Internal Server Error) will be sent to the client.

This code:

```python
raise Exception("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install layaberr
```