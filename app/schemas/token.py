from pydantic import BaseModel

# สำหรับการตอบกลับเมื่อ Login สำเร็จ (Response Model)
class Token(BaseModel):
    """
    Schema สำหรับ Access Token Response
    """
    access_token: str
    token_type: str = "bearer" # ตามมาตรฐาน OAuth2 มักจะเป็น "bearer"

# สำหรับโครงสร้างข้อมูลของ Token ที่เก็บใน JWT Payload
class TokenData(BaseModel):
    """
    Schema สำหรับข้อมูลที่ถอดรหัสออกมาจาก JWT Token (Payload)
    """
    username: str | None = None