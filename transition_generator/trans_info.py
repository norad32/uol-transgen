from dataclasses import dataclass
from typing import Dict, List

@dataclass
class TransInfo:
    description: str
    hashkey: str
    maptiles: List[Dict[str, str]]
    statictiles: List[Dict[str, str]]