from pydantic import BaseModel, EmailStr, field_validator


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_length(cls, v):
        if len(v) > 50:
            raise ValueError("Email must be less than 50 characters")
        return v
