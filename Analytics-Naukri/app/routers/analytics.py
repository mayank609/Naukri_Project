from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

from app.database import get_db, SocialMediaPost, CompetitorPost
from app.services.starapi_service import StarAPIService
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/performance")
async def get_performance_analytics(
    platform: str = Query("instagram", description="Social media platform"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Get performance analytics for your social media posts"""
    try:
        analytics_service = AnalyticsService(db)
        
        # Get date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get performance data
        performance_data = analytics_service.get_performance_data(
            platform=platform,
            start_date=start_date,
            end_date=end_date
        )
        
        # Calculate week-over-week changes
        wow_changes = analytics_service.calculate_week_over_week_changes(
            platform=platform,
            end_date=end_date
        )
        
        # Get top and bottom performers
        top_performers = analytics_service.get_top_performers(platform=platform, limit=5)
        bottom_performers = analytics_service.get_bottom_performers(platform=platform, limit=5)
        
        return {
            "platform": platform,
            "period": f"Last {days} days",
            "performance_data": performance_data,
            "week_over_week_changes": wow_changes,
            "top_performers": top_performers,
            "bottom_performers": bottom_performers,
            "summary": {
                "total_posts": len(performance_data),
                "avg_engagement_rate": sum(p["engagement_rate"] for p in performance_data) / len(performance_data) if performance_data else 0,
                "total_likes": sum(p["likes"] for p in performance_data),
                "total_comments": sum(p["comments"] for p in performance_data)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching performance data: {str(e)}")

@router.get("/competitor")
async def get_competitor_analytics(
    competitor_username: str = Query(..., description="Competitor username"),
    platform: str = Query("instagram", description="Social media platform"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """Get competitor analytics"""
    try:
        analytics_service = AnalyticsService(db)
        starapi_service = StarAPIService()
        
        # Fetch competitor data from StarAPI
        competitor_data = await starapi_service.get_user_posts(
            username=competitor_username,
            platform=platform
        )
        
        # Analyze competitor performance
        competitor_analysis = analytics_service.analyze_competitor_data(
            competitor_data=competitor_data,
            days=days
        )
        
        return {
            "competitor_username": competitor_username,
            "platform": platform,
            "analysis": competitor_analysis,
            "comparison": analytics_service.compare_with_competitor(
                competitor_analysis=competitor_analysis,
                platform=platform
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching competitor data: {str(e)}")

@router.get("/export")
async def export_data(
    platform: str = Query("instagram", description="Social media platform"),
    format: str = Query("csv", description="Export format (csv, json)"),
    days: int = Query(30, description="Number of days to export"),
    db: Session = Depends(get_db)
):
    """Export raw data as CSV or JSON"""
    try:
        analytics_service = AnalyticsService(db)
        
        # Get data for export
        export_data = analytics_service.get_export_data(
            platform=platform,
            days=days
        )
        
        if format.lower() == "csv":
            # Convert to DataFrame and export as CSV
            df = pd.DataFrame(export_data)
            csv_content = df.to_csv(index=False)
            
            from fastapi.responses import Response
            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={platform}_analytics_{datetime.now().strftime('%Y%m%d')}.csv"}
            )
        else:
            return {"data": export_data}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

@router.get("/dashboard")
async def get_dashboard_data(
    platform: str = Query("instagram", description="Social media platform"),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data"""
    try:
        analytics_service = AnalyticsService(db)
        
        # Get various analytics
        performance = analytics_service.get_performance_data(platform=platform)
        trends = analytics_service.get_trends(platform=platform)
        insights = analytics_service.get_insights(platform=platform)
        
        return {
            "performance": performance,
            "trends": trends,
            "insights": insights,
            "summary": analytics_service.get_summary_stats(platform=platform)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}") 