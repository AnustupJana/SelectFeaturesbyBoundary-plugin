# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectFeaturesbyBoundary
                                 A QGIS plugin
 A QGIS plugin that allows users to select all features within a clicked boundary polygon from another visible vector layer with a single click
                              -------------------
        begin                : 2025-07-13
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.utils import iface
from qgis.core import QgsPointXY, QgsGeometry, QgsFeatureRequest, QgsMapLayer, QgsProject
from qgis.gui import QgsMapTool
from PyQt5.QtCore import Qt
import os.path

# Initialize Qt resources from file resources.py
from .resources import *

class SelectFeaturesInPolygonTool(QgsMapTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas

    def canvasPressEvent(self, event):
        # Get the click position in map coordinates
        point = self.toMapCoordinates(event.pos())
        point_geom = QgsGeometry.fromPointXY(QgsPointXY(point))

        # Get all visible layers
        layer_tree = QgsProject.instance().layerTreeRoot()
        visible_layers = [node.layer() for node in layer_tree.children() if node.isVisible() and node.layer()]

        if not visible_layers:
            iface.messageBar().pushMessage("Error", "No visible layers found", level=3)
            return

        # Find the boundary layer (visible polygon layer with the largest extent)
        boundary_layer = None
        max_extent_area = 0
        for layer in visible_layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == 2:  # Polygon layer
                extent = layer.extent()
                area = extent.width() * extent.height()  # Approximate area of extent
                if area > max_extent_area:
                    max_extent_area = area
                    boundary_layer = layer

        if not boundary_layer:
            iface.messageBar().pushMessage("Error", "No visible polygon layer found for boundary", level=3)
            return

        # Use the active layer as the parcel layer (if visible and a vector layer)
        parcel_layer = iface.activeLayer()
        if not parcel_layer or not layer_tree.findLayer(parcel_layer.id()) or not layer_tree.findLayer(parcel_layer.id()).isVisible() or parcel_layer.type() != QgsMapLayer.VectorLayer:
            # Fallback: Use the first visible vector layer that isn't the boundary layer
            for layer in visible_layers:
                if layer != boundary_layer and layer.type() == QgsMapLayer.VectorLayer:
                    parcel_layer = layer
                    break
            if not parcel_layer:
                iface.messageBar().pushMessage("Error", "No valid parcel layer found (active layer must be a visible vector layer)", level=3)
                return

        # Find the polygon feature in the boundary layer at the clicked point
        request = QgsFeatureRequest().setFilterRect(point_geom.boundingBox())
        clicked_feature = None
        for feature in boundary_layer.getFeatures(request):
            if feature.geometry().intersects(point_geom):  # Check if click intersects polygon
                clicked_feature = feature
                break

        if not clicked_feature:
            iface.messageBar().pushMessage("Error", f"No polygon found at clicked location in {boundary_layer.name()}", level=3)
            return

        # Get the geometry of the clicked polygon
        polygon_geom = clicked_feature.geometry()
        if not polygon_geom.isGeosValid():
            iface.messageBar().pushMessage("Warning", "Clicked polygon has invalid geometry", level=2)

        # Clear previous selection in the parcel layer
        parcel_layer.removeSelection()

        # Create a list to store IDs of parcels that intersect the polygon
        selected_fids = []

        # Iterate through features in the parcel layer
        request = QgsFeatureRequest().setFilterRect(polygon_geom.boundingBox())
        for feature in parcel_layer.getFeatures(request):
            if feature.geometry().within(polygon_geom) or feature.geometry().intersects(polygon_geom):
                selected_fids.append(feature.id())

        # Select features in the parcel layer
        if selected_fids:
            parcel_layer.selectByIds(selected_fids)
            iface.messageBar().pushMessage("Success", f"Selected {len(selected_fids)} features in {parcel_layer.name()}", level=0)
        else:
            iface.messageBar().pushMessage("Info", f"No features found within the clicked polygon in {parcel_layer.name()}", level=1)

        # Deactivate the tool after one click
        iface.mapCanvas().unsetMapTool(self)

class SelectFeaturesbyBoundary:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SelectFeaturesbyBoundary_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Select Features by Boundary')
        self.first_start = None
        self.map_tool = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('SelectFeaturesbyBoundary', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Select Features by Boundary'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip="Select features within a boundary polygon with a single click",
            whats_this="Click a polygon in the largest-extent visible polygon layer to select features in the active layer"
        )
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Select Features by Boundary'),
                action)
            self.iface.removeToolBarIcon(action)
        # Deactivate the map tool if active
        if self.map_tool:
            self.iface.mapCanvas().unsetMapTool(self.map_tool)

    def run(self):
        """Run method that activates the map tool."""
        if self.first_start:
            self.first_start = False
        # Create and activate the map tool
        self.map_tool = SelectFeaturesInPolygonTool(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(self.map_tool)