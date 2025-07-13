# Select Features by Boundary QGIS Plugin
![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/icon.png?raw=true)

## Overview
The **Select Features by Boundary** plugin for QGIS enables users to select all features within a clicked boundary polygon from another visible vector layer with a single click. It automatically detects the boundary layer (the visible polygon layer with the largest spatial extent) and uses the active layer as the target layer, streamlining spatial selection tasks for cadastral data, urban planning, or spatial analysis.

## Features
- **Automatic Layer Detection**: Identifies the boundary layer (largest-extent visible polygon layer) and the target layer (active or fallback visible vector layer) without manual configuration.
- **One-Click Selection**: Activates a map tool to select all features (points, lines, or polygons) in the target layer that are within or intersect a clicked boundary polygon.
- **Error Handling**: Validates layer visibility, geometry types, and spatial relationships, providing clear feedback via the QGIS message bar (e.g., success, warnings, or errors).
- **Efficient Workflow**: Mimics MapInfo-style one-click selection, optimized for performance with large datasets using bounding box filters.

## Installation
1. **From QGIS Plugin Repository**:
   - In QGIS, go to `Plugins > Manage and Install Plugins`.
     ![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/doc/1st.png?raw=true)
   - Search for "Select Features by Boundary" in the `All` tab.
     ![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/doc/2nd.png?raw=true)
   - Click `Install Plugin`.

2. **From ZIP File**:
   - Download the plugin ZIP file from the [GitHub Releases](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin.git) page.
   - In QGIS, go to `Plugins > Manage and Install Plugins > Install from ZIP`.
   - Select the downloaded ZIP file and click `Install Plugin`.

3. **Manual Installation**:
   - Clone or download the plugin repository to your local machine.
   - Copy the `SelectFeaturesbyBoundary` folder to the QGIS plugins directory:
     - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
     - Windows: `C:\Users\<YourUsername>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
     - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - Restart QGIS to enable the plugin.

## Usage
1. **Load Vector Layers**:
   - Add at least two vector layers to your QGIS project:
     - A boundary layer (polygons, typically with the largest spatial extent, e.g., administrative boundaries).
     - A target layer (points, lines, or polygons, e.g., parcels) set as the active layer in the Layers Panel.

2. **Open the Plugin**:
   - Click the plugin icon in the QGIS toolbar or select **Select Features by Boundary** from the **Plugins** menu.
     ![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/doc/3rd.png?raw=true)

3. **Select Features**:
   - The plugin activates a map tool, changing the cursor to a crosshair.
   - Click a polygon in the boundary layer (automatically detected as the visible polygon layer with the largest extent).
   - Features in the target layer (active layer) that are within or intersect the clicked polygon are selected.
     ![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/doc/4th.png?raw=true)
   - A message in the QGIS message bar indicates success (e.g., "Selected 5 features in Parcels") or issues (e.g., "No polygon found").
     ![Diagram of the System](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/doc/5th.png?raw=true)

4. **Repeat**:
   - The map tool deactivates after one click. Click the toolbar button again to select features in another boundary polygon.

## Requirements
- **QGIS Version**: 3.0 or higher (tested up to QGIS 3.34).
- **Layer Types**: At least one visible polygon layer (boundary) and one visible vector layer (target, active layer) with compatible Coordinate Reference Systems (CRS).

## Troubleshooting
- **"No polygon found at clicked location"**:
  - Ensure you click inside a polygon in the boundary layer.
  - Zoom in for precise clicking.
  - Verify the boundary layer is visible and contains valid polygon geometries (use **Processing Toolbox > Check Validity** and **Fix Geometries**).
- **No features selected**:
  - Confirm the target layer is active and visible in the Layers Panel.
  - Ensure the boundary and target layers use the same CRS (check in **Layer Properties > Information**).
  - Test manually with **Processing Toolbox > Select by Location**.
- **Plugin not visible**:
  - Verify the plugin folder (`SelectFeaturesbyBoundary`) is in the correct QGIS plugins directory with all required files (`select_features_by_boundary.py`, `metadata.txt`, `resources.py`, `icon.png`, `__init__.py`).
  - Restart QGIS after installation.
- **Log Output**:
  - Check the QGIS Python Console (Ctrl+Alt+P) for error messages or debug information.

## Plugin Structure
- `select_features_by_boundary.py`: Main plugin logic.
- `metadata.txt`: Plugin metadata.
- `resources.py`: Compiled Qt resources for the icon.
- `icon.png`: Toolbar icon (24x24 PNG).
- `__init__.py`: Marks the directory as a Python package.

## Development
To modify or rebuild the plugin:
1. Edit `select_features_by_boundary.py` for core functionality.
2. Update `resources.qrc` and recompile `resources.py` using:
   ```bash
   pyrcc5 -o resources.py resources.qrc
   ```
3. Ensure `icon.png` exists in the plugin directory.

## Contributing
- Fork the repository and submit pull requests with improvements or bug fixes.
- Report issues or feature requests via the [GitHub issue tracker](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/issues).

## License
This plugin is licensed under the **GNU General Public License v2.0 or later**. See the [LICENSE](https://github.com/AnustupJana/SelectFeaturesbyBoundary-plugin/blob/main/LICENSE) file for details.

## Author
- **Name**: Anustup Jana
- **Email**: anustupjana21@gmail.com
- **Copyright**: © 2025 Anustup Jana
