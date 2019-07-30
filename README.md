<h2 align="center">Python Common Exception Module</h2>

<p align="center">
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_error/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_error/master'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_error/job/master/cobertura/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_error/master&config=testCoverage'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_error/job/master/lastSuccessfulBuild/testReport/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_error/master&config=testCount'></a>
</p>

Thin wrapper for handling exceptions.

The module is used to handle exception raised in pycommon_database and pycommon_server.

### Usage ###

## pycommon_database ##

Use to wrap marshalling exceptions.

| HTTP code | Parameter           | Description                                    |
|:----------|:--------------------|:-----------------------------------------------|
| 400       | `validation_failed` | Raised in case of validation error             |
| 404       | `model_not_found`   | Raised in case of missing data                 |


## pycommon_server ##

Use to wrap flask-restplus exceptions.

| HTTP code | Parameter                | Description                                            |
|:----------|:-------------------------|:-------------------------------------------------------|
| 400       | `bad_request_exception`  | Raised in case the server cannot interpret the request |
| 401       | `unauthorized_exception` | Raised in case of unauthorized access                  |
| 500       | `default_exception`      | Default handler (Internal Server Error)                |
