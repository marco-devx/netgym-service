from datetime import date

from fastapi import Query


class ListStudentFiltersParams:
    def __init__(
        self,
        search: str | None = Query(None, description="Search term"),
        organization_id: int | None = Query(None, ge=1, description="Contractor id"),
        role_id: int | None = Query(None, ge=1, description="Role id"),
        date_from: date | None = Query(None, description="Registered from date"),
        date_to: date | None = Query(None, description="Registered to date"),
        sort_by: str | None = Query(
            None,
            description="Field to sort by (full_name, registered_date, document, average_score, organization)",
        ),
        sort_dir: str = Query(
            "desc", regex="^(asc|desc)$", description="Sort direction", alias="sort_dir"
        ),
        page: int = Query(1, ge=1, description="Current page number"),
        size: int = Query(10, ge=1, le=100, description="Page size"),
    ):
        self.search = search
        self.organization_id = organization_id
        self.role_id = role_id
        self.date_from = date_from
        self.date_to = date_to
        self.sort_by = sort_by
        self.sort_dir = sort_dir
        self.page = page
        self.size = size

    def to_dict(self) -> dict:
        return {
            "search": self.search,
            "organization_id": self.organization_id,
            "role_id": self.role_id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "sort_by": self.sort_by,
            "sort_dir": self.sort_dir,
            "page": self.page,
            "size": self.size,
        }
