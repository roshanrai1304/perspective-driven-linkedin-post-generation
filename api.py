from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from perspective_post_generator import PerspectivePostGenerator

app = FastAPI(title="Perspective-Driven LinkedIn Post Generator")

# Sample physician perspectives
DEFAULT_PERSPECTIVES = [
    "AI should augment healthcare professionals, not replace them",
    "Technology must enhance the human connection in medicine, not diminish it",
    "Data privacy and ethical considerations must be prioritized in healthcare AI",
    "AI tools should reduce administrative burden to allow more time with patients",
    "Healthcare AI should focus on improving patient outcomes and experience",
    "AI solutions must be accessible to all healthcare providers, not just large institutions",
    "Clinicians should be involved in the development of healthcare AI systems"
]

# Initialize the generator with default perspectives
generator = PerspectivePostGenerator(DEFAULT_PERSPECTIVES)

class ArticleInput(BaseModel):
    content: str = Field(..., description="Article URL or summary text")
    is_url: bool = Field(False, description="Whether the content is a URL")
    perspectives: Optional[List[str]] = Field(None, description="Custom perspective statements")
    word_count: int = Field(225, description="Target word count for the LinkedIn post")

class PostResponse(BaseModel):
    post: str
    confidence_score: float
    error: Optional[str] = None

@app.post("/generate-post", response_model=PostResponse)
async def generate_post(article_input: ArticleInput):
    """Generate a LinkedIn post based on article content and physician's perspective."""
    
    # Use custom perspectives if provided
    if article_input.perspectives:
        temp_generator = PerspectivePostGenerator(article_input.perspectives)
        result = temp_generator.generate_post(
            article_input.content, 
            article_input.is_url,
            article_input.word_count
        )
    else:
        result = generator.generate_post(
            article_input.content, 
            article_input.is_url,
            article_input.word_count
        )
    
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 