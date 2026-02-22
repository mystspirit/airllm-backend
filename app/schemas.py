from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Input prompt for the model")
    max_new_tokens: int = Field(
        128, ge=1, le=2048, description="Maximum number of new tokens"
    )


class GenerateResponse(BaseModel):
    output: str


class StatusResponse(BaseModel):
    installed: bool
    model_loaded: bool
    model_name: str | None = None
    message: str
