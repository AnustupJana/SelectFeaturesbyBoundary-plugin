# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SelectFeaturesbyBoundary
                                 A QGIS plugin
 A QGIS plugin that allows users to select all features within a clicked boundary polygon from another visible vector layer with a single click
                             -------------------
        begin                : 2025-07-13
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SelectFeaturesbyBoundary class from file SelectFeaturesbyBoundary.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .select_features_by_boundary import SelectFeaturesbyBoundary
    return SelectFeaturesbyBoundary(iface)
