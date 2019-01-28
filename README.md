<h2 align="center">Python Common Exception Module</h2>

<p align="center">
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Thin wrapper for handling exceptions.

The module is used to handle exception raised in pycommon-database and pycommon-server.

### Usage ###

## pycommon-database ##

Use to wrap marshalling exceptions.

| HTTP code | Parameter           | Description                                    |
|:----------|:--------------------|:-----------------------------------------------|
| 400       | `validation_failed` | Raised in case of validation error |
| 404       | `model_not_found`   | Raised in case of missing data                 |


## pycommon-server ##

Use to wrap flask-restplus exceptions.

| HTTP code | Parameter                | Description                                            |
|:----------|:-------------------------|:-------------------------------------------------------|
| 400       | `bad_request_exception`  | Raised in case the server cannot interpret the request |
| 401       | `unauthorized_exception` | Raised in case of unauthorized access                  |
| 500       | `default_exception`      | Default handler (Internal Server Error)                |
