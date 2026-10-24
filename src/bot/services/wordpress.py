import os
import mimetypes
import httpx
import structlog

from typing import List, Optional, Dict, Any
from ...core.config import config

logger = structlog.get_logger()

AUTH = (config.wp.user, config.wp.application_password.get_secret_value())

async def upload_media_to_wordpress(file_bytes: bytes, filename: str = "photo.jpg") -> Optional[int]:
    url = f"{config.wp.url}/wp-json/wp/v2/media"

    content_type, _ = mimetypes.guess_type(filename)
    if not content_type:
        content_type = "image/jpeg"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": content_type,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                url, 
                content=file_bytes, 
                headers=headers, 
                auth=AUTH
            )
            
            if response.status_code == 201:
                return response.json().get("id")
            else:
                logger.warning("wordpress_connection_failed", status_code=response.status_code, text=response.text)
                return None
        except Exception as e:
            logger.error("wordpress_load_failed", error=str(e))
            return None


async def create_lisfinity_listing(
    title: str,
    content: str,
    price: int,
    category_id: Optional[int] = None,
    media_ids: Optional[List[int]] = None,
    taxonomy_slug: str = "listing-category"
) -> Optional[int]:
    url = f"{config.wp.url}/wp-json/custom/v1/create-listing"

    media_ids = media_ids or []
    featured_media = media_ids[0] if media_ids else None

    payload: Dict[str, Any] = {
        "title": title,
        "content": content,
        "status": "publish",
    }

    if featured_media: 
        payload["featured_media"] = featured_media
    
    payload["meta"] = {
        "price": price,
    }

    if len(media_ids) > 1:
        payload["meta"]["gallery_images"] = media_ids

    if category_id:
        payload[taxonomy_slug] = [category_id]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload, auth=AUTH)
            
            if response.status_code in (200, 201):
                post_data = response.json()
                return post_data.get("id")
            else:
                logger.warning("wordpress_connection_failed", status_code=response.statu_code, text=response.text)
                return None
        except Exception as e:
            logger.error("wordpress_advert_creation_failed", error=str(e))
            return None