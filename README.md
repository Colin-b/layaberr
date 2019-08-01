<h2 align="center">Exceptions handling for layab</h2>

<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layaberr/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layaberr/master'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layaberr/job/master/cobertura/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layaberr/master&config=testCoverage'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/layaberr/job/master/lastSuccessfulBuild/testReport/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/layaberr/master&config=testCount'></a>
</p>

Thin wrapper for handling exceptions.

The module is used to handle exception raised in layabase and layab.

### Usage ###

## layabase ##

Use to wrap marshalling exceptions.

| HTTP code | Parameter           | Description                                    |
|:----------|:--------------------|:-----------------------------------------------|
| 400       | `validation_failed` | Raised in case of validation error             |
| 404       | `model_not_found`   | Raised in case of missing data                 |


## layab ##

Use to wrap flask-restplus exceptions.

| HTTP code | Parameter                | Description                                            |
|:----------|:-------------------------|:-------------------------------------------------------|
| 400       | `bad_request_exception`  | Raised in case the server cannot interpret the request |
| 401       | `unauthorized_exception` | Raised in case of unauthorized access                  |
| 500       | `default_exception`      | Default handler (Internal Server Error)                |
