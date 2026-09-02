from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

# This ensures our tables are linked to the database engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VeriHire API")

# Dependency: Opens a database session for a request, then safely closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Our endpoint: Create a Candidate
@app.post("/candidates/", response_model=schemas.CandidateResponse)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    
    # 1. Check if the email is already in the database
    existing_user = db.query(models.Candidate).filter(models.Candidate.email == candidate.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Convert the Pydantic schema into a SQLAlchemy model instance
    new_candidate = models.Candidate(
        first_name=candidate.first_name, 
        last_name=candidate.last_name, 
        email=candidate.email
    )
    
    # 3. Save it to the database
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    
    return new_candidate
    # Our second endpoint: Fetch all Candidates
@app.get("/candidates/", response_model=list[schemas.CandidateResponse])
def read_candidates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    # Query the database for all candidates, with pagination (skip/limit)
    candidates = db.query(models.Candidate).offset(skip).limit(limit).all()
    
    return candidates
    # Our third endpoint: Fetch a specific Candidate by ID
@app.get("/candidates/{candidate_id}", response_model=schemas.CandidateResponse)
def read_candidate(candidate_id: UUID, db: Session = Depends(get_db)):
    
    # Search the database for the specific ID
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    
    # If no candidate is found, throw a 404 error
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    return candidate