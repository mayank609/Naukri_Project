import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.config import settings

class StarAPIService:
    def __init__(self):
        self.api_key = settings.starapi_key
        self.base_url = "https://starapi1.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "starapi1.p.rapidapi.com"
        }
    
    async def get_user_posts(
        self, 
        username: str, 
        platform: str = "instagram",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get user posts from Instagram using StarAPI"""
        
        try:
            # StarAPI endpoint for Instagram user posts
            url = f"{self.base_url}/instagram/user/posts"
            
            params = {
                "username": username,
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_instagram_posts(data)
            else:
                print(f"StarAPI Error: {response.status_code} - {response.text}")
                return self._get_mock_data(username, platform)
                
        except Exception as e:
            print(f"Error fetching Instagram data: {str(e)}")
            return self._get_mock_data(username, platform)
    
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get user information from Instagram"""
        
        try:
            url = f"{self.base_url}/instagram/user/info"
            
            params = {
                "username": username
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_user_info(data)
            else:
                return self._get_mock_user_info(username)
                
        except Exception as e:
            print(f"Error fetching user info: {str(e)}")
            return self._get_mock_user_info(username)
    
    async def get_hashtag_posts(
        self, 
        hashtag: str, 
        limit: int = 30
    ) -> List[Dict[str, Any]]:
        """Get posts by hashtag"""
        
        try:
            url = f"{self.base_url}/instagram/hashtag/posts"
            
            params = {
                "hashtag": hashtag,
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_instagram_posts(data)
            else:
                return self._get_mock_hashtag_data(hashtag)
                
        except Exception as e:
            print(f"Error fetching hashtag data: {str(e)}")
            return self._get_mock_hashtag_data(hashtag)
    
    async def get_trending_posts(self, platform: str = "instagram") -> List[Dict[str, Any]]:
        """Get trending posts"""
        
        try:
            url = f"{self.base_url}/instagram/trending"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_instagram_posts(data)
            else:
                return self._get_mock_trending_data()
                
        except Exception as e:
            print(f"Error fetching trending data: {str(e)}")
            return self._get_mock_trending_data()
    
    def _parse_instagram_posts(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Instagram posts from API response"""
        posts = []
        
        try:
            # Handle different response structures
            if "data" in data:
                raw_posts = data["data"]
            elif "posts" in data:
                raw_posts = data["posts"]
            elif isinstance(data, list):
                raw_posts = data
            else:
                raw_posts = []
            
            for post in raw_posts:
                try:
                    parsed_post = {
                        "post_id": post.get("id", ""),
                        "username": post.get("owner", {}).get("username", ""),
                        "caption": post.get("caption", ""),
                        "media_type": post.get("media_type", "image"),
                        "likes": post.get("like_count", 0),
                        "comments": post.get("comment_count", 0),
                        "shares": 0,  # Instagram doesn't provide share count
                        "views": post.get("view_count", 0),
                        "engagement_rate": self._calculate_engagement_rate(
                            post.get("like_count", 0),
                            post.get("comment_count", 0),
                            post.get("view_count", 0)
                        ),
                        "posted_at": self._parse_timestamp(post.get("timestamp", "")),
                        "media_url": post.get("media_url", ""),
                        "permalink": post.get("permalink", "")
                    }
                    posts.append(parsed_post)
                except Exception as e:
                    print(f"Error parsing post: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing Instagram posts: {str(e)}")
        
        return posts
    
    def _parse_user_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse user information from API response"""
        try:
            user_data = data.get("data", {})
            return {
                "username": user_data.get("username", ""),
                "full_name": user_data.get("full_name", ""),
                "biography": user_data.get("biography", ""),
                "followers": user_data.get("follower_count", 0),
                "following": user_data.get("following_count", 0),
                "posts_count": user_data.get("media_count", 0),
                "profile_picture": user_data.get("profile_pic_url", ""),
                "is_private": user_data.get("is_private", False),
                "is_verified": user_data.get("is_verified", False)
            }
        except Exception as e:
            print(f"Error parsing user info: {str(e)}")
            return {}
    
    def _calculate_engagement_rate(self, likes: int, comments: int, views: int) -> float:
        """Calculate engagement rate"""
        if views > 0:
            return round(((likes + comments) / views) * 100, 2)
        elif likes > 0:
            return round(((likes + comments) / likes) * 100, 2)
        else:
            return 0.0
    
    def _parse_timestamp(self, timestamp: str) -> Optional[str]:
        """Parse timestamp to ISO format"""
        try:
            if timestamp:
                dt = datetime.fromtimestamp(int(timestamp))
                return dt.isoformat()
        except:
            pass
        return None
    
    def _get_mock_data(self, username: str, platform: str) -> List[Dict[str, Any]]:
        """Generate mock data for testing"""
        import random
        from datetime import datetime, timedelta
        
        mock_posts = []
        for i in range(20):
            post_date = datetime.now() - timedelta(days=random.randint(1, 30))
            likes = random.randint(50, 2000)
            comments = random.randint(5, 200)
            views = random.randint(1000, 10000)
            
            mock_post = {
                "post_id": f"mock_post_{i}",
                "username": username,
                "caption": f"Mock post {i} - This is a sample caption for testing purposes",
                "media_type": random.choice(["image", "video", "carousel"]),
                "likes": likes,
                "comments": comments,
                "shares": random.randint(0, 50),
                "views": views,
                "engagement_rate": self._calculate_engagement_rate(likes, comments, views),
                "posted_at": post_date.isoformat(),
                "media_url": f"https://example.com/mock_media_{i}.jpg",
                "permalink": f"https://instagram.com/p/mock_post_{i}/"
            }
            mock_posts.append(mock_post)
        
        return mock_posts
    
    def _get_mock_user_info(self, username: str) -> Dict[str, Any]:
        """Generate mock user information"""
        return {
            "username": username,
            "full_name": f"Mock User {username}",
            "biography": "This is a mock user for testing purposes",
            "followers": 15000,
            "following": 500,
            "posts_count": 150,
            "profile_picture": "https://example.com/mock_profile.jpg",
            "is_private": False,
            "is_verified": False
        }
    
    def _get_mock_hashtag_data(self, hashtag: str) -> List[Dict[str, Any]]:
        """Generate mock hashtag data"""
        import random
        from datetime import datetime, timedelta
        
        mock_posts = []
        for i in range(10):
            post_date = datetime.now() - timedelta(days=random.randint(1, 7))
            likes = random.randint(100, 5000)
            comments = random.randint(10, 500)
            views = random.randint(2000, 20000)
            
            mock_post = {
                "post_id": f"hashtag_post_{i}",
                "username": f"user_{random.randint(1, 100)}",
                "caption": f"Amazing content with #{hashtag} #trending #viral",
                "media_type": random.choice(["image", "video"]),
                "likes": likes,
                "comments": comments,
                "shares": random.randint(0, 100),
                "views": views,
                "engagement_rate": self._calculate_engagement_rate(likes, comments, views),
                "posted_at": post_date.isoformat(),
                "media_url": f"https://example.com/hashtag_media_{i}.jpg",
                "permalink": f"https://instagram.com/p/hashtag_post_{i}/"
            }
            mock_posts.append(mock_post)
        
        return mock_posts
    
    def _get_mock_trending_data(self) -> List[Dict[str, Any]]:
        """Generate mock trending data"""
        import random
        from datetime import datetime, timedelta
        
        mock_posts = []
        for i in range(15):
            post_date = datetime.now() - timedelta(hours=random.randint(1, 24))
            likes = random.randint(500, 10000)
            comments = random.randint(50, 1000)
            views = random.randint(5000, 50000)
            
            mock_post = {
                "post_id": f"trending_post_{i}",
                "username": f"trending_user_{random.randint(1, 50)}",
                "caption": f"Trending content #{random.randint(1, 1000)} #viral #trending",
                "media_type": random.choice(["image", "video", "carousel"]),
                "likes": likes,
                "comments": comments,
                "shares": random.randint(0, 200),
                "views": views,
                "engagement_rate": self._calculate_engagement_rate(likes, comments, views),
                "posted_at": post_date.isoformat(),
                "media_url": f"https://example.com/trending_media_{i}.jpg",
                "permalink": f"https://instagram.com/p/trending_post_{i}/"
            }
            mock_posts.append(mock_post)
        
        return mock_posts 