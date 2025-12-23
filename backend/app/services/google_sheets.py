"""
Google Sheets import helper.

Requires service account JSON path in GS_SERVICE_ACCOUNT_JSON env var.
This uses `gspread` library.
"""
from typing import List
from app.core.config import settings
import gspread
import pandas as pd

def import_sheet(sheet_url: str, worksheet_name: str = None) -> List[dict]:
    if not settings.GS_SERVICE_ACCOUNT_JSON:
        raise RuntimeError("GS_SERVICE_ACCOUNT_JSON not configured")
    gc = gspread.service_account(filename=settings.GS_SERVICE_ACCOUNT_JSON)
    sh = gc.open_by_url(sheet_url)
    ws = sh.sheet1 if worksheet_name is None else sh.worksheet(worksheet_name)
    data = ws.get_all_records()
    # Convert to list of standardized dicts; frontend should align columns
    return data
