import logging
from typing import Dict, List
from dataclasses import asdict
import argparse
from pathlib import Path

from .terrain_parser import TerrainParser
from .transition_type_parser import TransitionTypeParser
from .transition_parser import TransitionParser
from .trans_info import TransInfo
from .xml_renderer import XMLRenderer

logger = logging.getLogger(__name__)


class TransitionGenerator:
    def __init__(
        self,
        args: argparse.Namespace,
        terrain_file: str = "terrain.xml",
    ):
        """
        Initializes the TransitionGenerator with the given arguments and file paths.

        :param args: Parsed command-line arguments.
        :param terrain_file: Path to the terrain XML file.
        :param transition_types_file: Path to the transition types XML file.
        """
        self.args = args
        self.terrain_parser = TerrainParser(terrain_file)
        self.transition_type_parser = TransitionTypeParser()
        self.transition_parser = TransitionParser(args.input_transitions)

        self.xml_renderer = XMLRenderer()
        self.trans_infos: List[TransInfo] = []
        # Initialize Terrain A and Terrain B (optional)
        self.terrain_a: Dict[str, str] = {}

    def replace_hashkey_placeholders(
        self, hashkey: str, terrain_a_hex: str, terrain_b_hex: str
    ) -> str:
        """
        Replaces 'A' and 'B' in the HashKey with the hex representations of Terrain A and B IDs.

        :param hashkey: The original hashkey with placeholders.
        :param terrain_a_hex: 2-digit Hex ID of Terrain A.
        :param terrain_b_hex: 2-digit Hex ID of Terrain B.
        :return: The final hashkey with placeholders replaced.
        """
        result: List[str] = []
        for char in hashkey.upper():
            if char == "A":
                result.append(terrain_a_hex)
            elif char == "B":
                result.append(terrain_b_hex)
            else:
                result.append(char)
        return "".join(result)

    def generate_trans_infos_for_pair(
        self, terrain_b: Dict[str, str]
    ) -> List[TransInfo]:
        """
        Generates TransInfo objects for a specific Terrain A and Terrain B pair.

        :param terrain_b: Dictionary containing Terrain B data.
        :return: List of TransInfo objects for the pair.
        """
        transitions: List[TransInfo] = self.transition_parser.get_transitions()
        trans_infos_for_pair: List[TransInfo] = []

        for entry in transitions:
            transition_type: str = entry.description  # Preserve original case
            for tt in self.transition_type_parser.get_transition_types():
                if transition_type == tt:
                    for (
                        hashkey
                    ) in self.transition_type_parser.get_hashkeys_by_transition_type(
                        tt
                    ):
                        final_hashkey = self.replace_hashkey_placeholders(
                            hashkey, self.terrain_a["ID_hex"], terrain_b["ID_hex"]
                        )
                        trans_infos_for_pair.append(
                            TransInfo(
                                description=entry.description,  # Preserve original case
                                hashkey=final_hashkey,
                                maptiles=entry.maptiles,
                                statictiles=entry.statictiles,
                            )
                        )
        return trans_infos_for_pair

    def generate_trans_infos(self) -> List[Dict[str, str]]:
        """
        Generates TransInfo objects based on command-line arguments.
        Returns a list of Terrain B dictionaries to process.

        :return: List of dictionaries containing Terrain B data.
        """
        # Validate presence of Terrain A
        terrain_a = self.terrain_parser.get_terrain_by_str(self.args.terrain_a)
        if not terrain_a:
            logger.error(f"Terrain A '{self.args.terrain_a}' not found in terrain.xml.")
            raise ValueError("Invalid Terrain A.")
        self.terrain_a = terrain_a

        # Check if Terrain B is provided
        if self.args.terrain_b:
            # Validate Terrain B
            terrain_b = self.terrain_parser.get_terrain_by_str(self.args.terrain_b)
            if not terrain_b:
                logger.error(
                    f"Terrain B '{self.args.terrain_b}' not found in terrain.xml."
                )
                raise ValueError("Invalid Terrain B.")
            logger.info("\n--- Generating for Specified Terrain B ---")
            return [terrain_b]  # Return a list with a single Terrain B
        else:
            # Generate for all Terrain B's except Terrain A
            all_terrains = self.terrain_parser.terrains.values()
            terrains_b = [
                terrain
                for terrain in all_terrains
                if terrain["Name"] != self.terrain_a["Name"]
            ]
            if not terrains_b:
                logger.error("No other terrains available to generate transitions.")
                raise ValueError("No Terrain B available.")
            logger.info("\n--- Generating for All Terrains Except Terrain A ---")
            return terrains_b  # Return a list of Terrain B's

    def generate_output_filenames(self, terrain_b: Dict[str, str]) -> str:
        """
        Generates output filenames based on Terrain A and Terrain B data.

        :param terrain_a: Dictionary containing Terrain A data.
        :param terrain_b: Dictionary containing Terrain B data.
        :return: Output filename.
        """
        terrain_a_id_dec = self.terrain_a["ID_dec"]
        terrain_a_name = self.terrain_a["Name"].replace(" ", "_")
        terrain_b_id_dec = terrain_b["ID_dec"]
        terrain_b_name = terrain_b["Name"].replace(" ", "_")
        output = f"{terrain_a_id_dec}-{terrain_a_name}_To_{terrain_b_id_dec}-{terrain_b_name}.xml"

        return output

    def generate_transitions_xml_for_pair(self, terrain_b: Dict[str, str]) -> None:
        """
        Generates the Transitions XML for a specific Terrain A and Terrain B pair and saves it to a file.

        :param terrain_a: Dictionary containing Terrain A data.
        :param terrain_b: Dictionary containing Terrain B data.
        """
        # Generate TransInfo objects for the pair
        trans_infos_for_pair = self.generate_trans_infos_for_pair(terrain_b)
        if not trans_infos_for_pair:
            logger.warning(
                f"No transitions generated for Terrain B '{terrain_b['Name']}'."
            )
            return

        # Generate output filename
        output_filename: str = self.generate_output_filenames(terrain_b)
        context = {"trans_infos": [asdict(info) for info in trans_infos_for_pair]}
        try:
            rendered_xml = self.xml_renderer.render_template("template.xml.j2", context)
        except Exception:
            logger.error("Failed to render XML template.")
            raise

        try:
            Path("output").mkdir(parents=True, exist_ok=True)
            with open(Path("output") / output_filename, "w", encoding="utf-8") as f:
                f.write(rendered_xml)
            logger.info(f"Transition XML generated and saved to {output_filename}")
        except IOError as e:
            logger.error(f"Error writing XML to file: {e}")
            raise

    def run(self) -> None:
        """
        Executes the transition generation process.
        """
        try:
            terrains_b = self.generate_trans_infos()
        except ValueError as e:
            logger.error(f"Error: {e}")
            return

        for terrain_b in terrains_b:
            try:
                self.generate_transitions_xml_for_pair(terrain_b)
            except Exception:
                logger.error(
                    f"Failed to generate Transitions XML for Terrain B '{terrain_b['Name']}'."
                )
                continue
