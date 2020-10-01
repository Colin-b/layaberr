from typing import List, Callable

import yaml
from apispec import APISpec, BasePlugin
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.schemas import BaseSchemaGenerator, EndpointInfo


class StarlettePlugin(BasePlugin):
    def __init__(self, app: Starlette):
        self.generator = BaseSchemaGenerator()
        self.app = app

    def init_spec(self, spec: APISpec):
        if hasattr(
            spec, "components"
        ):  # Temporary fix while waiting for PR to be merged in apispec
            for exception, handler in self.app.exception_handlers.items():
                spec.components.schema(
                    name=exception.__name__,
                    component=self.generator.parse_docstring(handler),
                )

    def endpoints(self) -> List[EndpointInfo]:
        return self.generator.get_endpoints(self.app.routes)

    def path_helper(
        self,
        path=None,
        operations=None,
        parameters=None,
        endpoint: EndpointInfo = None,
        **kwargs,
    ):
        if endpoint is None:
            return None

        default_operation = {
            "summary": self._summary(endpoint.func),
            "operationId": f"{endpoint.http_method.lower()}_{endpoint.func.__name__}",
            "responses": {
                exception.status_code: {
                    "description": exception.__doc__ or "",
                    "schema": {"$ref": f"#/definitions/{exception.__name__}"},
                }
                for exception in self.app.exception_handlers
                if isinstance(exception, HTTPException)
            },
        }
        # TODO Document error 500
        # Allow to override auto generated documentation
        default_operation.update(self.generator.parse_docstring(endpoint.func))
        operations[endpoint.http_method] = default_operation

    def _summary(self, func_or_method: Callable) -> str:
        """
        Given a function, parse the docstring and return it as a string if this is not YAML.
        """
        docstring = func_or_method.__doc__
        if not docstring:
            return ""

        # We support having regular docstrings before the schema
        # definition. Here we return just the schema part from
        # the docstring.
        docstring = docstring.split("---")[0]

        parsed = yaml.safe_load(docstring)

        if isinstance(parsed, dict):
            return ""

        return parsed


def client():
    app = Starlette(exception_handlers=layaberr.starlette.exception_handlers)

    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Example API",
        version="1.0",
        openapi_version="2.0",
        info={"description": "explanation of the api purpose"},
        plugins=[plugin],
    )
    plugin.init_spec(spec)

    @app.route("/swagger.json", include_in_schema=False)
    def schema(request):
        for endpoint in plugin.endpoints():
            spec.path(path=endpoint.path, endpoint=endpoint)
        return JSONResponse(spec.to_dict())
