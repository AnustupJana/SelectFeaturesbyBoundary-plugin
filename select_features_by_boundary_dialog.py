# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectFeaturesbyBoundaryDialog
                                 A QGIS plugin
 A QGIS plugin that allows users to select all features within a clicked boundary polygon from another visible vector layer with a single click
                             -------------------
        begin                : 2025-07-13
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'select_features_by_boundary_dialog_base.ui'))


class SelectFeaturesbyBoundaryDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SelectFeaturesbyBoundaryDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        self.setupUi(self)
