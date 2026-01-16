from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.config import settings


# Показывает кнопку Authorize в Swagger
_api_key_header = APIKeyHeader(name="X-Admin-Token", auto_error=False)


def require_admin(api_key: str | None = Depends(_api_key_header)) -> None:
    """Проверка админ-токена.

    Для учебного проекта: без регистрации/пользователей.
    Доступ к /api/admin/* только при наличии заголовка X-Admin-Token.
    """

    expected = (settings.admin_token or "").strip()
    if not expected or expected == "change-me":
        # чтобы в проде/на защите случайно не оставить "пустую" админку
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ADMIN_TOKEN is not configured",
        )

    if not api_key or api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
        )
