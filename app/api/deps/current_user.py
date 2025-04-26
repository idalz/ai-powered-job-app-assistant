from fastapi import Depends, HTTPException
from app.api.deps.jwt_bearer import JWTBearer
from app.core.security import verify_access_token

# Get current user payload
def get_current_user_payload(token: str = Depends(JWTBearer())):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
    return payload
