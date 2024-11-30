<h1 align="center">UO Landscaper Transition XML Generator</h1>

<div align="center">
    
  [![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/norad32/uol-transgen)
  [![GitHub Issues](https://img.shields.io/github/issues/norad32/uol-transgen.svg)](https://github.com/norad32/uol-transgen/issues)
  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/norad32/uol-transgen.svg)](https://github.com/norad32/uo-uol-transgen/pulls)
  [![License](https://img.shields.io/github/license/norad32/uol-transgen.svg)](https://github.com/norad32/uol-transgen/blob/main/LICENSE)
  
</div>

---

<p align="center"> A Python tool for generating transition XML files for Ultima Online Landscaper, enabling seamless map tile transitions for custom Ultima Online maps.
    <br> 
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About ](#about-)
- [Features ](#features-)
- [Getting Started ](#getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage ](#usage-)
  - [Running the Generator](#running-the-generator)
  - [Examples](#examples)
- [Authors ](#authors-)
- [Acknowledgements ](#acknowledgements-)

## About <a name="about"></a>

**UOL Transgen** is a Python-based tool designed to create transition XML files for [UO Landscaper](https://uo.wzk.cz/uolandscaper/), a popular mapping tool for Ultima Online. These XML files define how different terrain types transition between each other.

By automating the generation of these transition files, the tool makes the modding process easier without the hassle of manual XML editing.

## Features <a name="features"></a>

- **Automated XML Generation:** Simplifies the creation of complex transition tables between different terrains.
- **Terrain Selection:** Generate transitions for specific terrain pairs or batch-process all available terrains.
- **Robust Parsing:** Handles various input formats for terrains, including names, hexadecimal IDs, and decimal IDs.

## Getting Started <a name="getting-started"></a>

Follow these instructions to set up and use **UOL Transgen** on your local machine.

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7 or higher**: The scripting language used for the generator. [Download Python](https://www.python.org/downloads/)
- **Git**: For version control and repository management. [Download Git](https://git-scm.com/downloads)

Additional recommended tools:

- **UO Landscaper**: The mapping tool that utilizes the generated transition XML files. [Download UO Landscaper](https://uo.wzk.cz/uolandscaper/)

### Installation

Follow these steps to set up **UOL Transgen**:

1. **Clone the Repository**

   Open your terminal or command prompt and execute the following command to clone the repository:

   ```bash
   git clone https://github.com/norad32/uol-transgen.git
   ```

   This will create a `uol-transgen` folder with all the necessary source files.

2. **Navigate to the Project Directory**

   Open your terminal or command prompt and execute the following command to clone the repository:

   ```bash
   cd uol-transgen
   ```

3. **Install Dependencies**

   Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Required Data Files**

- **Terrain Definitions:** Ensure you have a terrain.xml file that defines all terrain types.
- **Input Transition Definitions:** Provide an input-transition.xml file that outlines the base transitions.

## Usage <a name="usage"></a>

Use `UOL Transgen` to create transition XML files based on your terrain configurations.

Command-Line Arguments <a name="command-line-arguments"></a>
The tool accepts the following command-line arguments:

- `i`, `--input-transitions` (required): Path to the input Transition XML file.
- `a`, `--terrain-a` (required): Name or ID of Terrain A.
- `b`, `--terrain-b` (optional): Name or ID of Terrain B. If omitted, transitions for all terrains except Terrain A are generated.

### Running the Generator

Execute the main script with the necessary arguments:

```bash
Copy code
python main.py -i input-transition.xml -a Grass -b 0
```

Arguments Explanation:

- `i input-transition.xml`: Specifies the input file containing base transition definitions.
- `a Grass`: Defines "Grass" as Terrain A.
- `b 0`: (Optional) Defines "No Draw" as Terrain B. If not provided, the tool generates transitions for all terrains except Terrain A.

### Examples

1. Generate Transitions Between Specific Terrains
   Generate transitions between "Grass" and "No Draw":

   ```bash
   Copy code
   python main.py -i input-transition.xml -a Grass -b "No Draw"
   ```

   _This will create an XML file named 1-Grass_To_0-No_Draw.xml in the output/ directory._

2. Generate Transitions for All Terrains Except Terrain A
   Generate transitions for "Grass" with all other terrains:

   ```bash
   Copy code
   python main.py -i input-transition.xml -a Grass
   ```

   _This will create multiple XML files, each representing a transition from "Grass" to another terrain._

## Authors <a name = "authors"></a>

- [@norad32](https://github.com/norad32)

## Acknowledgements <a name = "acknowledgement"></a>

- **Dknight** and **Admin Khaybel** of [OrBSydia](https://orbsydia.com/) for creating UO Landscaper.
- **Darus** for creating the best BMP2MAP conversion tool worldwide.
- **Richard Garriott**, **Starr Long**, **Raph Koster**, **Rick Delashmit**, **Scott Phillips**, **Kirk Winterrowd**, **Joe Basquez** and **Hal Milton** for creating Worlds.
- The **Ultima Online Free Shard Community** for their continuous support and inspiration.
