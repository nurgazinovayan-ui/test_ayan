import httpx
from app.core.config import get_settings

settings = get_settings()


class InstagramClient:
    def __init__(self):
        self.base = f"https://graph.facebook.com/{settings.instagram_graph_version}"

    def create_media_container(self, image_url: str, caption: str) -> str:
        url = f"{self.base}/{settings.instagram_business_account_id}/media"
        payload = {'image_url': image_url, 'caption': caption, 'access_token': settings.instagram_access_token}
        res = httpx.post(url, data=payload, timeout=30)
        res.raise_for_status()
        return res.json()['id']

    def publish_media(self, creation_id: str) -> str:
        url = f"{self.base}/{settings.instagram_business_account_id}/media_publish"
        res = httpx.post(url, data={'creation_id': creation_id, 'access_token': settings.instagram_access_token}, timeout=30)
        res.raise_for_status()
        return res.json()['id']
