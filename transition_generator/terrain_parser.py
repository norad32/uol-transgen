import logging
import re
import xml.etree.ElementTree as ET
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class TerrainParser:
    def __init__(self, file_path: str):
        """
        Initializes the TerrainParser with the given XML file path.
        Parses the terrains upon initialization.
        """
        self.file_path = file_path
        self.terrains: Dict[str, Dict[str, str]] = {}
        self.terrains_by_hex: Dict[str, Dict[str, str]] = {}
        self.terrains_by_dec: Dict[str, Dict[str, str]] = {}
        self.parse_terrains()

    def parse_terrains(self) -> None:
        """
        Parses the terrain.xml file to extract terrain names and their IDs.
        Populates self.terrains, self.terrains_by_hex, and self.terrains_by_dec dictionaries.
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            logger.error(f"Failed to parse terrain XML: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Terrain file not found: {self.file_path}")
            raise

        for terrain in root.findall("Terrain"):
            name = terrain.get("Name", "").strip()
            id_string = terrain.get("ID", "").strip()

            if not name or not id_string:
                logger.warning(
                    f"Terrain with missing Name or ID: Name='{name}', ID='{id_string}'"
                )
                continue

            try:
                terrain_id = int(id_string, 10)
                terrain_id_hex = f"{terrain_id:02X}"  # Ensure 2-digit hex
                name_lower = name.lower()
                terrain_data: Dict[str, str] = {
                    "Name": name,
                    "ID_dec": str(terrain_id),
                    "ID_hex": terrain_id_hex,
                }
                self.terrains[name_lower] = terrain_data
                self.terrains_by_hex[terrain_id_hex] = terrain_data
                self.terrains_by_dec[str(terrain_id)] = terrain_data
            except ValueError:
                logger.error(f"Invalid ID format for terrain '{name}': '{id_string}'")
                continue

    def get_terrain_by_str(self, input_str: str) -> Optional[Dict[str, str]]:
        """
        Retrieves a terrain based on user input (name, hex ID, or decimal ID).

        :param input_str: User input string representing terrain name or ID.
        :return: Dictionary containing terrain data if found, else None.
        """
        input_lower = input_str.strip().lower()

        # Check by name
        if input_lower in self.terrains:
            return self.terrains[input_lower]

        # Check by Hex ID with '0x' prefix
        hex_match = re.fullmatch(r"0x([0-9a-f]+)", input_lower, re.IGNORECASE)
        if hex_match:
            input_hex = hex_match.group(1).upper()
            return self.terrains_by_hex.get(input_hex)

        # Check by Decimal ID
        if input_lower.isdigit():
            return self.terrains_by_dec.get(input_lower)

        logger.error(
            "Invalid terrain. Please enter a valid Terrain Name, Hex ID (e.g., 0x29 or AB), or Decimal ID."
        )
        return None
