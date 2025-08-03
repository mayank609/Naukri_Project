from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import openai
from datetime import datetime

from app.database import get_db, ContentIdea
from app.services.content_service import ContentService
from app.config import settings

router = APIRouter()

# Pydantic models for request/response
class ContentRequest(BaseModel):
    content_type: str  # image, caption, video
    brand_description: str
    target_audience: str
    platform: str = "instagram"
    tone: str = "professional"
    hashtags: Optional[List[str]] = []
    specific_requirements: Optional[str] = ""

class ContentResponse(BaseModel):
    content_type: str
    content: str
    strategy: str
    brand_alignment: str
    engagement_tips: List[str]
    hashtag_suggestions: List[str]

@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered content ideas"""
    try:
        content_service = ContentService()
        
        # Generate content based on type
        if request.content_type == "image":
            content_result = await content_service.generate_image_ideas(
                brand_description=request.brand_description,
                target_audience=request.target_audience,
                platform=request.platform,
                tone=request.tone,
                hashtags=request.hashtags,
                requirements=request.specific_requirements
            )
        elif request.content_type == "caption":
            content_result = await content_service.generate_caption_ideas(
                brand_description=request.brand_description,
                target_audience=request.target_audience,
                platform=request.platform,
                tone=request.tone,
                hashtags=request.hashtags,
                requirements=request.specific_requirements
            )
        elif request.content_type == "video":
            content_result = await content_service.generate_video_ideas(
                brand_description=request.brand_description,
                target_audience=request.target_audience,
                platform=request.platform,
                tone=request.tone,
                hashtags=request.hashtags,
                requirements=request.specific_requirements
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid content type")
        
        # Save to database
        content_idea = ContentIdea(
            user_id=1,  # TODO: Get from authentication
            idea_type=request.content_type,
            content=content_result["content"],
            strategy=content_result["strategy"],
            brand_guidelines=content_result["brand_alignment"]
        )
        db.add(content_idea)
        db.commit()
        
        return ContentResponse(
            content_type=request.content_type,
            content=content_result["content"],
            strategy=content_result["strategy"],
            brand_alignment=content_result["brand_alignment"],
            engagement_tips=content_result["engagement_tips"],
            hashtag_suggestions=content_result["hashtag_suggestions"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@router.post("/optimize")
async def optimize_content(
    content: str = Body(..., description="Content to optimize"),
    content_type: str = Body("caption", description="Type of content"),
    platform: str = Body("instagram", description="Platform"),
    brand_guidelines: str = Body(..., description="Brand guidelines"),
    db: Session = Depends(get_db)
):
    """Optimize existing content for better engagement"""
    try:
        content_service = ContentService()
        
        optimized_content = await content_service.optimize_content(
            content=content,
            content_type=content_type,
            platform=platform,
            brand_guidelines=brand_guidelines
        )
        
        return {
            "original_content": content,
            "optimized_content": optimized_content["content"],
            "improvements": optimized_content["improvements"],
            "engagement_score": optimized_content["engagement_score"],
            "suggestions": optimized_content["suggestions"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing content: {str(e)}")

@router.get("/ideas")
async def get_content_ideas(
    content_type: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get previously generated content ideas"""
    try:
        query = db.query(ContentIdea)
        
        if content_type:
            query = query.filter(ContentIdea.idea_type == content_type)
        
        ideas = query.order_by(ContentIdea.created_at.desc()).limit(limit).all()
        
        return {
            "ideas": [
                {
                    "id": idea.id,
                    "type": idea.idea_type,
                    "content": idea.content,
                    "strategy": idea.strategy,
                    "brand_guidelines": idea.brand_guidelines,
                    "created_at": idea.created_at.isoformat()
                }
                for idea in ideas
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching content ideas: {str(e)}")

@router.post("/strategy")
async def generate_content_strategy(
    brand_description: str = Body(..., description="Brand description"),
    target_audience: str = Body(..., description="Target audience"),
    goals: List[str] = Body(..., description="Content goals"),
    platform: str = Body("instagram", description="Platform")
):
    """Generate comprehensive content strategy"""
    try:
        content_service = ContentService()
        
        strategy = await content_service.generate_content_strategy(
            brand_description=brand_description,
            target_audience=target_audience,
            goals=goals,
            platform=platform
        )
        
        return {
            "strategy": strategy["overview"],
            "content_calendar": strategy["content_calendar"],
            "themes": strategy["themes"],
            "best_practices": strategy["best_practices"],
            "engagement_tactics": strategy["engagement_tactics"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating strategy: {str(e)}")

@router.post("/trending-topics")
async def get_trending_topics(
    industry: str = Body(..., description="Industry/niche"),
    platform: str = Body("instagram", description="Platform")
):
    """Get trending topics for content ideation"""
    try:
        content_service = ContentService()
        
        trending_topics = await content_service.get_trending_topics(
            industry=industry,
            platform=platform
        )
        
        return {
            "industry": industry,
            "platform": platform,
            "trending_topics": trending_topics["topics"],
            "hashtag_trends": trending_topics["hashtags"],
            "content_opportunities": trending_topics["opportunities"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending topics: {str(e)}") 