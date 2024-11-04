from enum import Enum
from typing import Any
from utils import Converter, RedisCache
from fastapi import APIRouter


class BaseRouter(Converter, RedisCache):
    """Class registering routes"""

    prefix: str
    description: dict[str, str] | None = None
    tags: list[str | Enum] | None = None
    paths: dict[str, str] | None = None
    response_models: dict[str, Any] | None = None
    response_models_exclude_unset: dict[str, bool] | None = None
    names: dict[str, str] | None = None
    __methods = ["get", "post", "put", "delete", "patch"]

    @classmethod
    def __getting_description(cls, element) -> None | str:
        # if description is given or None
        if cls.description is not None:
            return cls.description.get(element)

    @classmethod
    def __get_endpoint_name(cls, method, element):
        # if name is given or name gets from function name
        if cls.names is not None:
            if name := cls.names.get(element):
                return name

        name = " ".join(element.replace(f"{method}_", "", 1).split("_")).title()
        return name

    @classmethod
    def __get_response_model(cls, element):
        # if response model is given or return None
        if cls.response_models is None:
            return None

        response_model = cls.response_models.get(element)
        return response_model

    @classmethod
    def __get_response_model_exclude_unset(cls, element) -> bool:
        if cls.response_models_exclude_unset is None:
            return False
        return cls.response_models_exclude_unset.get(element, False)

    @classmethod
    def __get_path(cls, element):
        # If path is given
        if cls.paths is not None and cls.paths.get(element) is not None:
            path = cls.paths[element]
            return path

        # Get path from function name
        path = "/" + "_".join(element.split("_")[1:])
        # If path equal tag then path is "" like get_bots and tags = ["bots"] -> path = "/bots"
        if cls.tags is not None and cls.tags[0] == path[1:]:
            path = ""
        return path

    @classmethod
    def create_router(cls) -> APIRouter:
        """Create router with endpoints of class attributes"""
        router = APIRouter(prefix=cls.prefix)
        for element in cls.__dict__:
            method = element.split("_")[0]
            if method in cls.__methods:
                name = cls.__get_endpoint_name(method=method, element=element)
                router.add_api_route(
                    path=cls.__get_path(element),
                    tags=cls.tags,
                    endpoint=getattr(cls, element),
                    methods=[method],
                    description=cls.__getting_description(element),
                    response_model=cls.__get_response_model(element),
                    response_model_exclude_unset=cls.__get_response_model_exclude_unset(
                        element
                    ),
                    name=name,
                )
        return router
