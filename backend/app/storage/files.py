import os
from app.core.config import settings
from fastapi import UploadFile
import shutil
from typing import Tuple

MEDIA_ROOT = settings.MEDIA_ROOT

def save_upload(file: UploadFile, subdir: str = "uploads") -> Tuple[str, str]:
    os.makedirs(os.path.join(MEDIA_ROOT, subdir), exist_ok=True)
    filename = file.filename
    dest = os.path.join(MEDIA_ROOT, subdir, filename)
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    rel = os.path.relpath(dest, MEDIA_ROOT)
    return rel, dest
