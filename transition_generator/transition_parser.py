import logging
from typing import Dict, List
import xml.etree.ElementTree as ET
import re

from .trans_info import TransInfo

logger = logging.getLogger(__name__)


class TransitionParser:
    def __init__(self, file_path: str):
        """
        Initializes the TransitionParser with the given XML file path.
        Parses the transitions upon initialization.

        :param file_path: Path to the transitions XML file.
        """
        self.file_path = file_path
        self.transition_entries: List[TransInfo] = []
        self.parse_transitions()

    def parse_transitions(self) -> None:
        """
        Parses the input Transition XML file to extract TransInfo.
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            logger.error(f"Failed to parse input transition XML: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Input transition file not found: {self.file_path}")
            raise

        for transition_type in root.findall("TransitionType"):
            description = transition_type.get("Description", "").strip()
            if not description:
                logger.warning(
                    "TransitionType element missing 'Description' attribute."
                )
                continue

            transition_type_name = description

            # Extract MapTiles
            maptiles: List[Dict[str, str]] = []
            maptiles_element = transition_type.find("MapTiles")
            if maptiles_element is not None:
                for map_tile in maptiles_element.findall("MapTile"):
                    tile_id = map_tile.get("TileID", "").strip()
                    
                    hex_match = re.fullmatch(r"0x([0-9a-fA-F]+)$", tile_id, re.IGNORECASE)  
                    if hex_match:
                      tile_id = str(int(hex_match.group(1), 16))
                    
                    alt_id_mod = map_tile.get("AltIDMod", "").strip()
                    if tile_id and alt_id_mod:
                        maptiles.append({"TileID": tile_id, "AltIDMod": alt_id_mod})

            # Extract StaticTiles
            statictiles: List[Dict[str, str]] = []
            statictiles_element = transition_type.find("StaticTiles")
            if statictiles_element is not None:
                for static_tile in statictiles_element.findall("StaticTile"):
                    tile_id = static_tile.get("TileID", "").strip()
                    
                    hex_match = re.fullmatch(r"0x([0-9a-fA-F]+)$", tile_id, re.IGNORECASE)  
                    if hex_match:
                      tile_id = str(int(hex_match.group(1), 16))
                      
                    alt_id_mod = static_tile.get("AltIDMod", "").strip()
                    if tile_id and alt_id_mod:
                        statictiles.append({"TileID": tile_id, "AltIDMod": alt_id_mod})

            self.transition_entries.append(
                TransInfo(
                    description=transition_type_name,
                    hashkey="",
                    maptiles=maptiles,
                    statictiles=statictiles,
                )
            )

    def get_transitions(self) -> List[TransInfo]:
        """Returns a list of all transitions."""
        return list(self.transition_entries)
