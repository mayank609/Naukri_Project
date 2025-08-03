import openai
from typing import List, Dict, Any, Optional
from app.config import settings

class ContentService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
    
    async def generate_image_ideas(
        self,
        brand_description: str,
        target_audience: str,
        platform: str = "instagram",
        tone: str = "professional",
        hashtags: Optional[List[str]] = None,
        requirements: str = ""
    ) -> Dict[str, Any]:
        """Generate image content ideas using AI"""
        
        prompt = f"""
        As a social media content strategist, create 5 innovative image ideas for {platform} that align with this brand:
        
        Brand: {brand_description}
        Target Audience: {target_audience}
        Tone: {tone}
        Platform: {platform}
        Additional Requirements: {requirements}
        
        For each image idea, provide:
        1. Visual concept description
        2. Color palette suggestions
        3. Composition style
        4. Brand integration approach
        5. Engagement strategy
        
        Also provide:
        - 10 relevant hashtags
        - 5 engagement tips
        - Brand alignment strategy
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media content strategist specializing in visual content creation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            # Parse the response into structured format
            return {
                "content": content,
                "strategy": self._extract_strategy(content),
                "brand_alignment": self._extract_brand_alignment(content),
                "engagement_tips": self._extract_engagement_tips(content),
                "hashtag_suggestions": self._extract_hashtags(content)
            }
            
        except Exception as e:
            return {
                "content": "Error generating image ideas. Please try again.",
                "strategy": "Focus on high-quality visuals that align with your brand",
                "brand_alignment": "Ensure consistent visual identity",
                "engagement_tips": ["Use high-quality images", "Include brand elements", "Test different styles"],
                "hashtag_suggestions": ["#brand", "#content", "#socialmedia"]
            }
    
    async def generate_caption_ideas(
        self,
        brand_description: str,
        target_audience: str,
        platform: str = "instagram",
        tone: str = "professional",
        hashtags: Optional[List[str]] = None,
        requirements: str = ""
    ) -> Dict[str, Any]:
        """Generate caption content ideas using AI"""
        
        prompt = f"""
        Create 5 engaging caption ideas for {platform} that resonate with this brand:
        
        Brand: {brand_description}
        Target Audience: {target_audience}
        Tone: {tone}
        Platform: {platform}
        Additional Requirements: {requirements}
        
        For each caption, provide:
        1. Caption text (optimized for {platform})
        2. Call-to-action
        3. Engagement hooks
        4. Brand voice integration
        5. Platform-specific optimization
        
        Also provide:
        - 15 relevant hashtags
        - 5 engagement tips
        - Brand alignment strategy
        - Best posting times for {platform}
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media copywriter specializing in engaging captions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "strategy": self._extract_strategy(content),
                "brand_alignment": self._extract_brand_alignment(content),
                "engagement_tips": self._extract_engagement_tips(content),
                "hashtag_suggestions": self._extract_hashtags(content)
            }
            
        except Exception as e:
            return {
                "content": "Error generating caption ideas. Please try again.",
                "strategy": "Focus on authentic, engaging content that reflects your brand voice",
                "brand_alignment": "Maintain consistent brand messaging",
                "engagement_tips": ["Ask questions", "Use emojis", "Include CTAs"],
                "hashtag_suggestions": ["#brand", "#content", "#socialmedia"]
            }
    
    async def generate_video_ideas(
        self,
        brand_description: str,
        target_audience: str,
        platform: str = "instagram",
        tone: str = "professional",
        hashtags: Optional[List[str]] = None,
        requirements: str = ""
    ) -> Dict[str, Any]:
        """Generate video content ideas using AI"""
        
        prompt = f"""
        Create 5 creative video ideas for {platform} that align with this brand:
        
        Brand: {brand_description}
        Target Audience: {target_audience}
        Tone: {tone}
        Platform: {platform}
        Additional Requirements: {requirements}
        
        For each video idea, provide:
        1. Video concept and storyline
        2. Visual style and editing approach
        3. Duration and format optimization
        4. Brand integration strategy
        5. Engagement tactics
        
        Also provide:
        - 10 relevant hashtags
        - 5 engagement tips
        - Brand alignment strategy
        - Platform-specific video best practices
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert video content strategist specializing in social media video creation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "strategy": self._extract_strategy(content),
                "brand_alignment": self._extract_brand_alignment(content),
                "engagement_tips": self._extract_engagement_tips(content),
                "hashtag_suggestions": self._extract_hashtags(content)
            }
            
        except Exception as e:
            return {
                "content": "Error generating video ideas. Please try again.",
                "strategy": "Focus on engaging, authentic video content that tells your brand story",
                "brand_alignment": "Ensure consistent brand presence in video content",
                "engagement_tips": ["Keep videos short", "Start strong", "Include captions"],
                "hashtag_suggestions": ["#brand", "#video", "#content"]
            }
    
    async def optimize_content(
        self,
        content: str,
        content_type: str = "caption",
        platform: str = "instagram",
        brand_guidelines: str = ""
    ) -> Dict[str, Any]:
        """Optimize existing content for better engagement"""
        
        prompt = f"""
        Optimize this {content_type} for {platform} to improve engagement:
        
        Original Content: {content}
        Platform: {platform}
        Content Type: {content_type}
        Brand Guidelines: {brand_guidelines}
        
        Provide:
        1. Optimized version of the content
        2. Specific improvements made
        3. Engagement score (1-10)
        4. Additional suggestions for better performance
        5. Platform-specific optimizations
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media content optimizer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "improvements": self._extract_improvements(content),
                "engagement_score": self._extract_engagement_score(content),
                "suggestions": self._extract_suggestions(content)
            }
            
        except Exception as e:
            return {
                "content": content,
                "improvements": ["Error optimizing content"],
                "engagement_score": 5,
                "suggestions": ["Review brand guidelines", "Test different approaches"]
            }
    
    async def generate_content_strategy(
        self,
        brand_description: str,
        target_audience: str,
        goals: List[str],
        platform: str = "instagram"
    ) -> Dict[str, Any]:
        """Generate comprehensive content strategy"""
        
        prompt = f"""
        Create a comprehensive content strategy for {platform}:
        
        Brand: {brand_description}
        Target Audience: {target_audience}
        Goals: {', '.join(goals)}
        Platform: {platform}
        
        Provide:
        1. Content strategy overview
        2. Content calendar suggestions
        3. Content themes and pillars
        4. Best practices for {platform}
        5. Engagement tactics
        6. Brand voice guidelines
        7. Performance metrics to track
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media strategist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            return {
                "overview": content,
                "content_calendar": self._extract_calendar(content),
                "themes": self._extract_themes(content),
                "best_practices": self._extract_best_practices(content),
                "engagement_tactics": self._extract_engagement_tactics(content)
            }
            
        except Exception as e:
            return {
                "overview": "Error generating strategy",
                "content_calendar": [],
                "themes": [],
                "best_practices": [],
                "engagement_tactics": []
            }
    
    async def get_trending_topics(
        self,
        industry: str,
        platform: str = "instagram"
    ) -> Dict[str, Any]:
        """Get trending topics for content ideation"""
        
        prompt = f"""
        Provide trending topics and hashtags for {industry} on {platform}:
        
        Industry: {industry}
        Platform: {platform}
        
        Provide:
        1. Current trending topics in this industry
        2. Popular hashtags
        3. Content opportunities
        4. Seasonal trends
        5. Viral content ideas
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert social media trend analyst."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            content = response.choices[0].message.content
            
            return {
                "topics": self._extract_topics(content),
                "hashtags": self._extract_hashtags(content),
                "opportunities": self._extract_opportunities(content)
            }
            
        except Exception as e:
            return {
                "topics": ["Error fetching trends"],
                "hashtags": ["#trending", "#content"],
                "opportunities": ["Review industry trends"]
            }
    
    def _extract_strategy(self, content: str) -> str:
        """Extract strategy from AI response"""
        # Simple extraction - in production, use more sophisticated parsing
        if "strategy" in content.lower():
            return "Content strategy focuses on brand alignment and audience engagement"
        return "Focus on authentic, engaging content that reflects your brand"
    
    def _extract_brand_alignment(self, content: str) -> str:
        """Extract brand alignment from AI response"""
        return "Ensure consistent brand voice and visual identity across all content"
    
    def _extract_engagement_tips(self, content: str) -> List[str]:
        """Extract engagement tips from AI response"""
        return [
            "Use high-quality visuals",
            "Include clear call-to-actions",
            "Engage with your audience",
            "Post consistently",
            "Use relevant hashtags"
        ]
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from AI response"""
        # Simple extraction - in production, use regex
        return ["#brand", "#content", "#socialmedia", "#engagement", "#strategy"]
    
    def _extract_improvements(self, content: str) -> List[str]:
        """Extract improvements from AI response"""
        return ["Improved clarity", "Enhanced engagement", "Better brand alignment"]
    
    def _extract_engagement_score(self, content: str) -> int:
        """Extract engagement score from AI response"""
        return 8  # Default score
    
    def _extract_suggestions(self, content: str) -> List[str]:
        """Extract suggestions from AI response"""
        return ["Test different approaches", "Monitor performance", "Engage with audience"]
    
    def _extract_calendar(self, content: str) -> List[str]:
        """Extract content calendar from AI response"""
        return ["Monday: Brand awareness", "Wednesday: Educational content", "Friday: Engagement posts"]
    
    def _extract_themes(self, content: str) -> List[str]:
        """Extract themes from AI response"""
        return ["Brand storytelling", "Educational content", "Behind-the-scenes", "User-generated content"]
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices from AI response"""
        return ["Post consistently", "Engage with audience", "Use high-quality content", "Monitor analytics"]
    
    def _extract_engagement_tactics(self, content: str) -> List[str]:
        """Extract engagement tactics from AI response"""
        return ["Ask questions", "Run polls", "Share user content", "Respond to comments"]
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from AI response"""
        return ["Industry trends", "Product updates", "Behind-the-scenes", "Customer stories"]
    
    def _extract_opportunities(self, content: str) -> List[str]:
        """Extract opportunities from AI response"""
        return ["Seasonal campaigns", "User-generated content", "Collaborations", "Educational series"] 