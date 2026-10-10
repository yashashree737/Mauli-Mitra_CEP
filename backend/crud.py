from typing import Any, Callable, Type

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from schemas import Action, GeoPoint, METHOD_TO_ACTION


def point_to_geo(wkt_element: Any) -> GeoPoint | None:
    if wkt_element is None:
        return None
    shape = to_shape(wkt_element)
    return GeoPoint(latitude=shape.y, longitude=shape.x)


def geo_to_wkt(point: GeoPoint | dict | None) -> WKTElement | None:
    if point is None:
        return None
    if isinstance(point, dict):
        return WKTElement(f"POINT({point['longitude']} {point['latitude']})", srid=4326)
    return WKTElement(f"POINT({point.longitude} {point.latitude})", srid=4326)


def model_to_read_dict(instance: Any, location_fields: set[str] | None = None) -> dict[str, Any]:
    location_fields = location_fields or set()
    data: dict[str, Any] = {}
    for column in instance.__table__.columns:
        name = column.name
        value = getattr(instance, name)
        if name in location_fields:
            data[name] = point_to_geo(value)
        else:
            data[name] = value
    return data


def apply_create_data(model: Any, payload: BaseModel, location_fields: set[str] | None = None) -> Any:
    location_fields = location_fields or set()
    data = payload.model_dump(exclude_unset=True)
    for field in location_fields:
        if field in data:
            data[field] = geo_to_wkt(data.pop(field))
    return model(**data)


def apply_update_data(instance: Any, payload: BaseModel, location_fields: set[str] | None = None) -> Any:
    location_fields = location_fields or set()
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field in location_fields:
            setattr(instance, field, geo_to_wkt(value))
        else:
            setattr(instance, field, value)
    return instance


def create_crud_router(
    *,
    prefix: str,
    tag: str,
    model: Type,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    read_schema: Type[BaseModel],
    location_fields: set[str] | None = None,
    order_by: Callable | None = None,
) -> APIRouter:
    location_fields = location_fields or set()
    router = APIRouter(prefix=prefix, tags=[tag])

    def validate_action(method: str, action: Action) -> None:
        expected = METHOD_TO_ACTION.get(method)
        if expected is None:
            raise HTTPException(status_code=405, detail=f"Method {method} not allowed")
        if action != expected:
            raise HTTPException(
                status_code=400,
                detail=f"Action '{action.value}' does not match HTTP method '{method}' "
                f"(expected '{expected.value}')",
            )

    def serialize(instance: Any) -> BaseModel:
        return read_schema.model_validate(model_to_read_dict(instance, location_fields))

    @router.get("")
    def read_records(
        action: Action = Query(...),
        id: int | None = Query(None),
        db: Session = Depends(get_db),
    ):
        validate_action("GET", action)
        if id is not None:
            instance = db.get(model, id)
            if instance is None:
                raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
            return serialize(instance)
        query = db.query(model)
        if order_by is not None:
            query = query.order_by(order_by())
        instances = query.all()
        return [serialize(item) for item in instances]

    @router.post("")
    async def create_record(request: Request, db: Session = Depends(get_db)):
        body = await request.json()
        action = Action(body.get("action"))
        validate_action("POST", action)
        if body.get("data") is None:
            raise HTTPException(status_code=400, detail="'data' is required for CREATE")
        payload = create_schema.model_validate(body["data"])
        instance = apply_create_data(model, payload, location_fields)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return serialize(instance)

    @router.put("")
    async def replace_record(request: Request, db: Session = Depends(get_db)):
        body = await request.json()
        action = Action(body.get("action"))
        validate_action("PUT", action)
        record_id = body.get("id")
        if record_id is None:
            raise HTTPException(status_code=400, detail="'id' is required for UPDATE")
        if body.get("data") is None:
            raise HTTPException(status_code=400, detail="'data' is required for UPDATE")
        instance = db.get(model, record_id)
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        payload = update_schema.model_validate(body["data"])
        apply_update_data(instance, payload, location_fields)
        db.commit()
        db.refresh(instance)
        return serialize(instance)

    @router.patch("")
    async def update_record(request: Request, db: Session = Depends(get_db)):
        body = await request.json()
        action = Action(body.get("action"))
        validate_action("PATCH", action)
        record_id = body.get("id")
        if record_id is None:
            raise HTTPException(status_code=400, detail="'id' is required for UPDATE")
        if body.get("data") is None:
            raise HTTPException(status_code=400, detail="'data' is required for UPDATE")
        instance = db.get(model, record_id)
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        payload = update_schema.model_validate(body["data"])
        apply_update_data(instance, payload, location_fields)
        db.commit()
        db.refresh(instance)
        return serialize(instance)

    @router.delete("")
    def delete_record(
        action: Action = Query(...),
        id: int = Query(...),
        db: Session = Depends(get_db),
    ):
        validate_action("DELETE", action)
        instance = db.get(model, id)
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        db.delete(instance)
        db.commit()
        return {"deleted": True, "id": id}

    @router.get("/retrieve")
    def retrieve_record_by_field(
        field: str = Query(..., description="Field name to query by"),
        value: str = Query(..., description="Value of the field"),
        db: Session = Depends(get_db),
    ):
        if not hasattr(model, field):
            raise HTTPException(status_code=400, detail=f"Field '{field}' not found in {model.__name__}")
        
        column = getattr(model, field)
        instance = db.query(model).filter(column == value).first()
        if instance is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return serialize(instance)

    return router
