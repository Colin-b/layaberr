# Python Common Error Module #

Thin wrapper to handle error raised through pycommon-database and pycommon-server.

The module can be used to handle exception raised by pycommon-database and pycommon-server.

### Usage ###

## pycommon-database ##

| parameter                    | description                                    |
|:-----------------------------|:-----------------------------------------------|
| `model_not_found`            | Raised in case of missing data                 |
| `validation_failed`          | Raised in case of Marshmallow validation error |

## pycommon-server ##

| parameter                    | description                     |
|:-----------------------------|:--------------------------------|
| `model_not_found`            | Raised in case of missing model |
| `validation_failed`          | Raised in case of invalid model |