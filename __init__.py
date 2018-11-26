# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZpboBuilder
                                 A QGIS plugin
 A plugin to create a mosaic of zpbo polygons
                             -------------------
        begin                : 2018-05-02
        copyright            : (C) 2018 by Mohannad ADHAM / Axians
        email                : mohannad.adm@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ZpboBuilder class from file ZpboBuilder.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .zpbo_builder import ZpboBuilder
    return ZpboBuilder(iface)
