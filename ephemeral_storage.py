"""
Ephemeral Video Storage - In-Memory Only
Videos exist only in the current session and disappear on page refresh
No database, no file persistence
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import threading

# In-memory video storage (thread-safe)
VIDEO_STORAGE: Dict[str, Dict[str, Any]] = {}
STORAGE_LOCK = threading.Lock()


class EphemeralVideoManager:
    """
    Manage videos in-memory only for current session
    Videos auto-expire after inactivity or on browser refresh
    """
    
    @staticmethod
    def store_video(video_data: bytes, filename: str, metadata: Dict) -> str:
        """
        Store video in memory with auto-expiry
        Returns: video_id
        """
        video_id = str(uuid.uuid4())[:8]
        
        with STORAGE_LOCK:
            VIDEO_STORAGE[video_id] = {
                'data': video_data,
                'filename': filename,
                'metadata': metadata,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(hours=2),  # 2 hour max
                'accessed_at': datetime.now(),
            }
        
        print(f"[EPHEMERAL] Video stored: {video_id} ({len(video_data) / 1024 / 1024:.1f} MB)")
        return video_id
    
    @staticmethod
    def get_video(video_id: str) -> Optional[tuple]:
        """
        Retrieve video from memory
        Returns: (data, metadata) or None
        """
        with STORAGE_LOCK:
            if video_id not in VIDEO_STORAGE:
                print(f"[EPHEMERAL] Video not found: {video_id}")
                return None
            
            video = VIDEO_STORAGE[video_id]
            
            # Check expiry
            if datetime.now() > video['expires_at']:
                del VIDEO_STORAGE[video_id]
                print(f"[EPHEMERAL] Video expired: {video_id}")
                return None
            
            # Update access time
            video['accessed_at'] = datetime.now()
            
            return (video['data'], video['metadata'])
    
    @staticmethod
    def list_videos() -> list:
        """List all active videos in current session"""
        with STORAGE_LOCK:
            # Clean expired
            expired = [vid for vid, data in VIDEO_STORAGE.items() 
                      if datetime.now() > data['expires_at']]
            for vid in expired:
                del VIDEO_STORAGE[vid]
            
            # Return active videos
            videos = []
            for video_id, video in VIDEO_STORAGE.items():
                videos.append({
                    'id': video_id,
                    'filename': video['filename'],
                    'created_at': video['created_at'].isoformat(),
                    'size_mb': len(video['data']) / 1024 / 1024,
                    'metadata': video['metadata'],
                })
            
            print(f"[EPHEMERAL] Active videos: {len(videos)}")
            return videos
    
    @staticmethod
    def cleanup_all():
        """Clear all videos (called on app restart or manual cleanup)"""
        with STORAGE_LOCK:
            count = len(VIDEO_STORAGE)
            VIDEO_STORAGE.clear()
            print(f"[EPHEMERAL] Cleaned up {count} videos")


def get_storage_stats():
    """Get memory usage stats"""
    with STORAGE_LOCK:
        total_size = sum(len(v['data']) for v in VIDEO_STORAGE.values())
        return {
            'active_videos': len(VIDEO_STORAGE),
            'total_size_mb': total_size / 1024 / 1024,
        }
