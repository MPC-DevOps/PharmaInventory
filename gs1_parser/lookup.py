"""
GTIN database lookup — queries MongoDB Medication / Drug Data collection.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient

GTIN_MONGO_URI = os.getenv(
    "GTIN_MONGO_URI",
    "mongodb+srv://mohammedfouly:bousia11BB@clusterone.m3nsbla.mongodb.net/",
)
GTIN_MONGO_DB = os.getenv("GTIN_MONGO_DB", "Medication")
GTIN_MONGO_COLLECTION = os.getenv("GTIN_MONGO_COLLECTION", "Drug Data")

_client: Optional[MongoClient] = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(GTIN_MONGO_URI, serverSelectionTimeoutMS=10_000)
    return _client[GTIN_MONGO_DB][GTIN_MONGO_COLLECTION]


def lookup_gtin(gtin: str, **_kwargs) -> Optional[Dict[str, Any]]:
    """
    Lookup a GTIN in MongoDB and return the matching record.

    Args:
        gtin: 14-digit GTIN string (exact match).

    Returns:
        The matching record dict (without _id), or None if not found.
    """
    if not gtin:
        return None

    col = _get_collection()
    record = col.find_one({"GTIN Code": gtin.strip()}, {"_id": 0})
    return record or None
