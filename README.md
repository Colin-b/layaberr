# Python Common Exception Module #

Thin wrapper for handling exceptions.

The module is used to handle exception raised in pycommon-database and pycommon-server.

### Usage ###

## pycommon-database ##

Use to wrap marshalling exceptions.

| parameter                    | description                                    |
|:-----------------------------|:-----------------------------------------------|
| `model_not_found`            | Raised in case of missing data                 |
| `validation_failed`          | Raised in case of Marshmallow validation error |

## pycommon-server ##

Use to wrap flask-restplus exceptions.

| parameter                    | description                                  |
|:-----------------------------|:---------------------------------------------|
| `default_exception`          | Default handler (500: Internal Server Error) |
| `unauthorized_exception`     | Raised in case of unauthorized acces         |
| `bad_request_exception`      | Raised in case the server cannot interpret the request |