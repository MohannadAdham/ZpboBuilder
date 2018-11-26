# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZpboBuilderDialog
                                 A QGIS plugin
 A plugin to create a mosaic of zpbo polygons
                             -------------------
        begin                : 2018-05-02
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Mohannad ADHAM / Axians
        email                : mohannad.adm@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

# # FORM_CLASS, _ = uic.loadUiType(os.path.join(
# #     os.path.dirname(__file__), 'zpbo_builder_dialog_base.ui'))


# # class ZpboBuilderDialog(QtGui.QDialog, FORM_CLASS):
# #     def __init__(self, parent=None):
# #         """Constructor."""
# #         super(ZpboBuilderDialog, self).__init__(parent)
# #         # Set up the user interface from Designer.
# #         # After setupUI you can access any designer object by doing
# #         # self.<objectname>, and you can use autoconnect slots - see
# #         # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
# #         # #widgets-and-dialogs-with-auto-connect
# #         self.setupUi(self)

# from ui_zpbo_builder import Ui_ZpboBuilderDialogBase

# class ZpboBuilderDialog(QtGui.QDialog):
#     def __init__(self):
#         """Constructor."""
#         # super(ZpboBuilderDialog, self).__init__(parent)
#         QtGui.QDialog.__init__(self)
#         # Set up the user interface from Designer.
#         self.ui = Ui_ZpboBuilderDialogBase()
#         # Set up the user interface from Designer.
#         # After setupUI you can access any designer object by doing
#         # self.<objectname>, and you can use autoconnect slots - see
#         # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
#         # #widgets-and-dialogs-with-auto-connect
#         self.ui.setupUi(self)

#     #     # test to configure the folder browsers
#     #     def open_browse_dialog(self):
#     #         self.browse_temp_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

#     #     # self.browse_temp_path = None
#     #     self.ui.temp_path_btn.clicked.connect(open_browse_dialog)
#     #     # self.ui.temp_path_line.setText(unicode(self.browse_temp_path.text()))


#     # # def open_browse_dialog():
#     # #     self.browse_temp_path = QFileDialog().getExistingDirectory()



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'zpbo_builder_dialog_base.ui'))


class ZpboBuilderDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ZpboBuilderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
