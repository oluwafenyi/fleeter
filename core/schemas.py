
from drf_yasg import openapi


bad_request = openapi.Response(
    description="bad request response",
    schema=openapi.Schema(
        type="object",
        properties={"<field>": openapi.Schema(type="array", items=openapi.Schema(type="string", title="error detail"))}
    ),
    examples={
        "application/json": {
            "confirm_password": ["passwords do not match"]
        }
    }
)

not_found = openapi.Response(
    description="not found response",
    schema=openapi.Schema(
        type="object",
        properties={"detail": openapi.Schema(type="string")}
    ),
    examples={
        "application/json": {
            "detail": "resource not found"
        }
    }
)

following_response = openapi.Response(
    description="user following/unfollowing response",
    schema=openapi.Schema(
        type="object",
        properties={"following": openapi.Schema(type="boolean")}
    ),
    examples={
        "application/json": {
            "following": True
        }
    }
)

media_upload_response = openapi.Response(
    description="media upload response",
    schema=openapi.Schema(
        type="object",
        properties={"upload_status": openapi.Schema(type="string")}
    ),
    examples={
        "application/json": {
            "upload_status": "success"
        }
    }
)
