import logging
import re
import xml.etree.ElementTree as ET
from typing import Dict, List

logger = logging.getLogger(__name__)


class TransitionTypeParser:
    def __init__(self):
        """
        Initializes the TransitionTypeParser with the given XML file path.
        Parses the transition types upon initialization.
        """
        self.file_path = "data/transition_types.xml"
        self.transition_types: Dict[str, List[str]] = {}
        self.parse_transition_types()

    def parse_transition_types(self) -> None:
        """
        Parses the transition_types.xml file to extract transition types and their HashKeys.
        Populates self.transition_types dictionary.
        """
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            logger.error(f"Failed to parse transition types XML: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Transition types file not found: {self.file_path}")
            raise

        for transition_type in root.findall("TransitionType"):
            name = transition_type.get("name", "").strip()
            if not name:
                logger.warning("TransitionType element missing 'name' attribute.")
                continue

            # Preserve original case for transition type names
            name_original = name

            hashkeys_element = transition_type.find("HashKeys")
            if hashkeys_element is not None:
                hashkeys: List[str] = []
                for hashkey in hashkeys_element.findall("HashKey"):
                    value = hashkey.get("value", "").strip()
                    if value:
                        if self.validate_hashkey(value):
                            hashkeys.append(value)
                        else:
                            logger.warning(
                                f"Invalid HashKey format: '{value}' in TransitionType '{name}'"
                            )
                if hashkeys:
                    self.transition_types[name_original] = hashkeys
            else:
                logger.warning(f"No HashKeys found for TransitionType '{name}'.")

    def validate_hashkey(self, hashkey: str) -> bool:
        """
        Validates the format of a hashkey. Assuming hashkeys are hexadecimal strings.

        :param hashkey: HashKey string to validate.
        :return: True if valid, False otherwise.
        """
        # Example validation: only hexadecimal characters
        return bool(re.fullmatch(r"[A-Fa-f0-9]+", hashkey))

    def get_transition_types(self) -> List[str]:
        """Returns a list of all transition type names with original casing."""
        return list(self.transition_types.keys())

    def get_hashkeys_by_transition_type(self, name: str) -> List[str]:
        """
        Returns the list of hashkeys for a given transition type name.

        :param name: Name of the transition type.
        :return: List of hashkeys if transition type exists, else empty list.
        """
        return self.transition_types.get(name, [])
