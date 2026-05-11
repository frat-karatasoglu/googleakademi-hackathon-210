from supabase import create_client, Client
from app.config import settings

# Workaround: disable HTTP/2 for postgrest Sync client to avoid
# intermittent "Server disconnected" errors in httpcore/httpx on Windows.
# We monkeypatch the SyncPostgrestClient.create_session method to force
# http2=False when building the underlying httpx client.
try:
    from postgrest._sync.client import SyncPostgrestClient
    from postgrest.utils import SyncClient

    def _create_session_no_http2(self, base_url, headers, timeout, verify=True):
        return SyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
            verify=verify,
            follow_redirects=True,
            http2=False,
        )

    # Apply monkeypatch at import time.
    SyncPostgrestClient.create_session = _create_session_no_http2
except Exception:
    # If postgrest internals change or import fails, fall back to default behavior.
    pass

_client: Client | None = None


def get_db() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _client
