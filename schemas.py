from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class CandidateCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class CandidateResponse(CandidateCreate):
    id: UUID  # Changed from int to UUID
    
    model_config = ConfigDict(from_attributes=True)