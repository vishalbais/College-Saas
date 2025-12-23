import qrcode
from PIL import Image
import os
import io
from app.core.config import settings
from uuid import uuid4

MEDIA_ROOT = settings.MEDIA_ROOT

def generate_uid(prefix: str = "") -> str:
    return f"{prefix}{uuid4().hex[:12]}"

def generate_qr(uid: str, event_id: int, subpath: str = "qrs") -> str:
    """
    Create QR PNG under MEDIA_ROOT/subpath/<event_id> and return relative path.
    QR payload encodes uid and event_id.
    """
    payload = {"uid": uid, "event_id": event_id}
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img: Image.Image = qr.make_image(fill_color="black", back_color="white")

    event_dir = os.path.join(MEDIA_ROOT, subpath, str(event_id))
    os.makedirs(event_dir, exist_ok=True)

    filename = f"{uid}.png"
    path = os.path.join(event_dir, filename)
    img.save(path)
    # return path relative to MEDIA_ROOT
    rel = os.path.relpath(path, MEDIA_ROOT)
    return rel
