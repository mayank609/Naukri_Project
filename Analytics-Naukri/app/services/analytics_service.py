from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

from app.database import SocialMediaPost, CompetitorPost

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_performance_data(
        self, 
        platform: str = "instagram",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get performance data for posts"""
        query = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        )
        
        if start_date:
            query = query.filter(SocialMediaPost.posted_at >= start_date)
        if end_date:
            query = query.filter(SocialMediaPost.posted_at <= end_date)
        
        posts = query.order_by(SocialMediaPost.posted_at.desc()).all()
        
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "caption": post.caption,
                "media_type": post.media_type,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "views": post.views,
                "engagement_rate": post.engagement_rate,
                "posted_at": post.posted_at.isoformat() if post.posted_at else None,
                "total_engagement": post.likes + post.comments + post.shares
            }
            for post in posts
        ]
    
    def calculate_week_over_week_changes(
        self, 
        platform: str = "instagram",
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Calculate week-over-week performance changes"""
        if not end_date:
            end_date = datetime.now()
        
        # Current week
        current_week_start = end_date - timedelta(days=7)
        current_week_posts = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.platform == platform,
                SocialMediaPost.posted_at >= current_week_start,
                SocialMediaPost.posted_at <= end_date
            )
        ).all()
        
        # Previous week
        previous_week_start = current_week_start - timedelta(days=7)
        previous_week_posts = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.platform == platform,
                SocialMediaPost.posted_at >= previous_week_start,
                SocialMediaPost.posted_at < current_week_start
            )
        ).all()
        
        # Calculate metrics
        current_metrics = self._calculate_metrics(current_week_posts)
        previous_metrics = self._calculate_metrics(previous_week_posts)
        
        # Calculate changes
        changes = {}
        for metric in ["avg_likes", "avg_comments", "avg_shares", "avg_engagement_rate", "total_posts"]:
            current_val = current_metrics.get(metric, 0)
            previous_val = previous_metrics.get(metric, 0)
            
            if previous_val > 0:
                change_percent = ((current_val - previous_val) / previous_val) * 100
            else:
                change_percent = 0
            
            changes[f"{metric}_change"] = {
                "current": current_val,
                "previous": previous_val,
                "change_percent": round(change_percent, 2)
            }
        
        return changes
    
    def get_top_performers(self, platform: str = "instagram", limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing posts"""
        posts = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        ).order_by(desc(SocialMediaPost.engagement_rate)).limit(limit).all()
        
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "caption": post.caption[:100] + "..." if len(post.caption) > 100 else post.caption,
                "engagement_rate": post.engagement_rate,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "posted_at": post.posted_at.isoformat() if post.posted_at else None,
                "total_engagement": post.likes + post.comments + post.shares
            }
            for post in posts
        ]
    
    def get_bottom_performers(self, platform: str = "instagram", limit: int = 5) -> List[Dict[str, Any]]:
        """Get bottom performing posts"""
        posts = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        ).order_by(SocialMediaPost.engagement_rate).limit(limit).all()
        
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "caption": post.caption[:100] + "..." if len(post.caption) > 100 else post.caption,
                "engagement_rate": post.engagement_rate,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "posted_at": post.posted_at.isoformat() if post.posted_at else None,
                "total_engagement": post.likes + post.comments + post.shares
            }
            for post in posts
        ]
    
    def get_trends(self, platform: str = "instagram") -> Dict[str, Any]:
        """Get performance trends"""
        # Get posts from last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        posts = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.platform == platform,
                SocialMediaPost.posted_at >= start_date,
                SocialMediaPost.posted_at <= end_date
            )
        ).all()
        
        if not posts:
            return {"trends": [], "insights": []}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([
            {
                "posted_at": post.posted_at,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "engagement_rate": post.engagement_rate,
                "media_type": post.media_type
            }
            for post in posts
        ])
        
        # Daily trends
        df['date'] = pd.to_datetime(df['posted_at']).dt.date
        daily_trends = df.groupby('date').agg({
            'likes': 'mean',
            'comments': 'mean',
            'shares': 'mean',
            'engagement_rate': 'mean'
        }).reset_index()
        
        # Media type performance
        media_performance = df.groupby('media_type').agg({
            'engagement_rate': 'mean',
            'likes': 'mean',
            'comments': 'mean'
        }).reset_index()
        
        return {
            "daily_trends": daily_trends.to_dict('records'),
            "media_performance": media_performance.to_dict('records'),
            "total_posts": len(posts),
            "avg_engagement_rate": df['engagement_rate'].mean()
        }
    
    def get_insights(self, platform: str = "instagram") -> List[Dict[str, Any]]:
        """Get actionable insights from data"""
        insights = []
        
        # Get recent posts
        recent_posts = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        ).order_by(desc(SocialMediaPost.posted_at)).limit(20).all()
        
        if not recent_posts:
            return insights
        
        # Analyze engagement patterns
        engagement_rates = [post.engagement_rate for post in recent_posts]
        avg_engagement = np.mean(engagement_rates)
        
        # High performing posts
        high_performers = [post for post in recent_posts if post.engagement_rate > avg_engagement * 1.5]
        low_performers = [post for post in recent_posts if post.engagement_rate < avg_engagement * 0.5]
        
        if high_performers:
            insights.append({
                "type": "success",
                "title": "High Performing Content",
                "message": f"Found {len(high_performers)} posts with above-average engagement",
                "recommendation": "Analyze these posts to understand what resonates with your audience"
            })
        
        if low_performers:
            insights.append({
                "type": "warning",
                "title": "Low Performing Content",
                "message": f"Found {len(low_performers)} posts with below-average engagement",
                "recommendation": "Review these posts and consider adjusting your content strategy"
            })
        
        # Media type analysis
        media_types = {}
        for post in recent_posts:
            if post.media_type not in media_types:
                media_types[post.media_type] = []
            media_types[post.media_type].append(post.engagement_rate)
        
        for media_type, rates in media_types.items():
            avg_rate = np.mean(rates)
            insights.append({
                "type": "info",
                "title": f"{media_type.title()} Performance",
                "message": f"Average engagement rate for {media_type}: {avg_rate:.2f}%",
                "recommendation": f"Consider optimizing {media_type} content for better engagement"
            })
        
        return insights
    
    def get_summary_stats(self, platform: str = "instagram") -> Dict[str, Any]:
        """Get summary statistics"""
        posts = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        ).all()
        
        if not posts:
            return {
                "total_posts": 0,
                "avg_engagement_rate": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0
            }
        
        total_likes = sum(post.likes for post in posts)
        total_comments = sum(post.comments for post in posts)
        total_shares = sum(post.shares for post in posts)
        avg_engagement = np.mean([post.engagement_rate for post in posts])
        
        return {
            "total_posts": len(posts),
            "avg_engagement_rate": round(avg_engagement, 2),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_engagement": total_likes + total_comments + total_shares
        }
    
    def get_export_data(self, platform: str = "instagram", days: int = 30) -> List[Dict[str, Any]]:
        """Get data for export"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        posts = self.db.query(SocialMediaPost).filter(
            and_(
                SocialMediaPost.platform == platform,
                SocialMediaPost.posted_at >= start_date,
                SocialMediaPost.posted_at <= end_date
            )
        ).all()
        
        return [
            {
                "post_id": post.post_id,
                "caption": post.caption,
                "media_type": post.media_type,
                "likes": post.likes,
                "comments": post.comments,
                "shares": post.shares,
                "views": post.views,
                "engagement_rate": post.engagement_rate,
                "posted_at": post.posted_at.isoformat() if post.posted_at else None,
                "created_at": post.created_at.isoformat()
            }
            for post in posts
        ]
    
    def analyze_competitor_data(self, competitor_data: List[Dict], days: int = 30) -> Dict[str, Any]:
        """Analyze competitor data"""
        if not competitor_data:
            return {}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(competitor_data)
        
        # Calculate metrics
        avg_engagement = df['engagement_rate'].mean() if 'engagement_rate' in df.columns else 0
        avg_likes = df['likes'].mean() if 'likes' in df.columns else 0
        avg_comments = df['comments'].mean() if 'comments' in df.columns else 0
        
        # Content type analysis
        media_analysis = {}
        if 'media_type' in df.columns:
            media_analysis = df.groupby('media_type').agg({
                'engagement_rate': 'mean',
                'likes': 'mean',
                'comments': 'mean'
            }).to_dict('index')
        
        return {
            "total_posts": len(competitor_data),
            "avg_engagement_rate": round(avg_engagement, 2),
            "avg_likes": round(avg_likes, 2),
            "avg_comments": round(avg_comments, 2),
            "media_analysis": media_analysis,
            "top_posts": df.nlargest(5, 'engagement_rate').to_dict('records') if 'engagement_rate' in df.columns else []
        }
    
    def compare_with_competitor(self, competitor_analysis: Dict, platform: str = "instagram") -> Dict[str, Any]:
        """Compare your performance with competitor"""
        your_posts = self.db.query(SocialMediaPost).filter(
            SocialMediaPost.platform == platform
        ).all()
        
        if not your_posts:
            return {"comparison": "No data available"}
        
        your_avg_engagement = np.mean([post.engagement_rate for post in your_posts])
        your_avg_likes = np.mean([post.likes for post in your_posts])
        your_avg_comments = np.mean([post.comments for post in your_posts])
        
        competitor_avg_engagement = competitor_analysis.get("avg_engagement_rate", 0)
        competitor_avg_likes = competitor_analysis.get("avg_likes", 0)
        competitor_avg_comments = competitor_analysis.get("avg_comments", 0)
        
        return {
            "engagement_comparison": {
                "yours": round(your_avg_engagement, 2),
                "competitor": competitor_avg_engagement,
                "difference": round(your_avg_engagement - competitor_avg_engagement, 2)
            },
            "likes_comparison": {
                "yours": round(your_avg_likes, 2),
                "competitor": competitor_avg_likes,
                "difference": round(your_avg_likes - competitor_avg_likes, 2)
            },
            "comments_comparison": {
                "yours": round(your_avg_comments, 2),
                "competitor": competitor_avg_comments,
                "difference": round(your_avg_comments - competitor_avg_comments, 2)
            }
        }
    
    def _calculate_metrics(self, posts: List[SocialMediaPost]) -> Dict[str, float]:
        """Calculate metrics for a list of posts"""
        if not posts:
            return {
                "avg_likes": 0,
                "avg_comments": 0,
                "avg_shares": 0,
                "avg_engagement_rate": 0,
                "total_posts": 0
            }
        
        return {
            "avg_likes": np.mean([post.likes for post in posts]),
            "avg_comments": np.mean([post.comments for post in posts]),
            "avg_shares": np.mean([post.shares for post in posts]),
            "avg_engagement_rate": np.mean([post.engagement_rate for post in posts]),
            "total_posts": len(posts)
        } 