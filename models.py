from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    user_role: str = Field(default="employee", max_length=50)

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=2000)
