<h2 align="center">Exceptions handling for layab</h2>

<p align="center">
<a href="https://pypi.org/project/layaberr/"><img alt="pypi version" src="https://img.shields.io/pypi/v/layaberr"></a>
<a href="https://travis-ci.com/Colin-b/layaberr"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/layaberr.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/layaberr"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/layaberr"><img alt="Number of tests" src="https://img.shields.io/badge/tests-22 passed-blue"></a>
<a href="https://pypi.org/project/layaberr/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/layaberr"></a>
</p>

This module allows to throw exceptions in your code and send a proper HTTP response automatically to your client.

Depending on the REST Framework you use, your need to add exception handler(s) to your API.

## Starlette

### Register exceptions handlers

If you want to document your API about those specific return types and the expected body, you can use [layab](https://pypi.org/project/layab/) to create your Starlette application.

You can also register all provided exceptions at once yourself using `layaberr.starlette.exception_handlers`

```python
from starlette.applications import Starlette
import layaberr.starlette

app = Starlette(exception_handlers=layaberr.starlette.exception_handlers)
```

### Supported Exceptions

The following exceptions are available

#### ValidationFailed

In case your endpoint raises ValidationFailed, an HTTP error 400 (Bad Request) will be sent to the client.

##### Error not specific to a field in received data

This code:

```python
from layaberr.starlette import ValidationFailed

received_data = None
raise ValidationFailed(received_data, message="This is the error message")
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  1, "field_name":  "", "messages": ["This is the error message"]}]}
```

##### Error specific to a field in a received dictionary

This code:

```python
from layaberr.starlette import ValidationFailed

received_data = {"field 1": "value 1"}
raise ValidationFailed(received_data, errors={"field 1": ["Invalid value"]})
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  1, "field_name":  "field 1", "messages": ["Invalid value"]}]}
```

##### Error specific to a field in a received list of dictionaries

This code:

```python
from layaberr.starlette import ValidationFailed

received_data = [{"field 1": "value 1"}, {"field 1": "value 2"}]
raise ValidationFailed(received_data, errors={1: {"field 1": ["Invalid value"]}})
```

Will result in the following JSON response sent to the client:
```json
{"fields":  [{"item":  2, "field_name":  "field 1", "messages": ["Invalid value"]}]}
```

#### Unauthorized

In case your endpoint raises Unauthorized, an HTTP error 401 (Unauthorized) will be sent to the client.

This code:

```python
from layaberr.starlette import Unauthorized

raise Unauthorized("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

#### Forbidden

In case your endpoint raises Forbidden, an HTTP error 403 (Forbidden) will be sent to the client.

This code:

```python
from layaberr.starlette import Forbidden

raise Forbidden("The exception message")
```

Will result in the following JSON response sent to the client:
```json
{"message":  "The exception message"}
```

#### Exception (this is the default handler)

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