from fastapi import APIRouter,Depends,Response,HTTPException

from app.exceptions import IncorrectEmailOrPasswordException, TokenAbsentException, UserAlreadyExistsException
from app.tasks.email_confirmation import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from app.users.dao import UserDAO
from app.users.schemas import SUserAuth

router = APIRouter (
    prefix="/auth",
    tags=["Auth и пользователи"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    send_booking_confirmation_email.delay(user_data.email)
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email,hashed_password=hashed_password)

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("cutly_access_token", access_token, httponly=True,)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout_user(response:Response):
    response.delete_cookie("cutly_access_token")
    
@router.post("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user