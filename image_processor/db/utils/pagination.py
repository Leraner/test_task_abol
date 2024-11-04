import math

from pydantic import BaseModel


class Pagination:
    @staticmethod
    def get_paginated_data(
        page: int,
        size: int,
        total_count: int,
        objects: list[BaseModel],
        model: type[BaseModel],
    ) -> BaseModel:
        total_pages: int = math.ceil(round(total_count / size, 1)) or 1
        has_next_page: bool = page < total_pages
        has_previous_page: bool = page != 1 and page <= total_pages + 1

        return model(
            total_count=total_count,
            total_pages=total_pages,
            has_next_page=has_next_page,
            has_previous_page=has_previous_page,
            page=page,
            items=objects,
        )