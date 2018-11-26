# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZpboBuilder
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

import PyQt4
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import psycopg2
import psycopg2.extras
import xml.etree.ElementTree as ET
import xlrd
import xlwt
import os.path
import os
import subprocess
import osgeo.ogr  
import processing



from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qgis
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from zpbo_builder_dialog import ZpboBuilderDialog
import os.path




class ZpboBuilder:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
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
            'ZpboBuilder_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)



        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Zpbo Builder')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ZpboBuilder')
        self.toolbar.setObjectName(u'ZpboBuilder')

        # Create the dialog (after translation) and keep reference
        self.dlg = ZpboBuilderDialog()

        self.temp_line_edit = self.dlg.findChild(QLineEdit, "lineEdit_temp_folder")
        self.result_line_edit = self.dlg.findChild(QLineEdit, "lineEdit_result_folder")
        self.density_spinbox = self.dlg.findChild(QDoubleSpinBox, "doubleSpinBox_density")


#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" lsitner autojmatic dimensioning """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
        #creation du bouton "connexion BD"
        Button_connexion_BD= self.dlg.findChild(QPushButton,"pushButton_connexion")
        QObject.connect(Button_connexion_BD, SIGNAL("clicked()"),self.connectToDb)
        #mot de passe en etoile
        self.dlg.lineEdit_Password.setEchoMode(QLineEdit.Password)

        # # Connect the button "pushButton_verifier_topologie"
        Button_verification = self.dlg.findChild(QPushButton, "pushButton_verification")
        QObject.connect(Button_verification, SIGNAL("clicked()"), self.generate_zpbo_jointives)

        # # Connect the button "pushButton_orientation"
        Button_temp_folder = self.dlg.findChild(QPushButton, "pushButton_temp_folder")
        QObject.connect(Button_temp_folder, SIGNAL("clicked()"), self.select_temp_folder)

        # # Connect the button "pushButton_orientation"
        Button_result_folder = self.dlg.findChild(QPushButton, "pushButton_result_folder")  
        QObject.connect(Button_result_folder, SIGNAL("clicked()"), self.select_result_folder)

        # # Connect the button "pushButton_orientation"
        Button_remove = self.dlg.findChild(QPushButton, "pushButton_remove")  
        QObject.connect(Button_remove, SIGNAL("clicked()"), self.remove_temp_layers)

        # # Connect the button "pushButton_fibres_utiles"
        # Button_fibres_utiles = self.dlg.findChild(QPushButton, "pushButton_fibres_utiles")
        # QObject.connect(Button_fibres_utiles, SIGNAL("clicked()"), self.calcul_fibres_utiles)

        # # Connect the button "pushButton_"
        # Button_dimensios = self.dlg.findChild(QPushButton, "pushButton_dimensions")
        # QObject.connect(Button_dimensios, SIGNAL("clicked()"), self.calcul_boite_dimensions)

        # # Connect the butoon "pushButton_mettre_a_jour_chemin"
        # Button_verify_capacity = self.dlg.findChild(QPushButton, "pushButton_verify_capacity")
        # QObject.connect(Button_verify_capacity, SIGNAL("clicked()"), self.verify_capacite_chambre)

        # # Connect the button "pushButton_mettre_a_jour_ebp"
        # Button_mettre_a_jour_ebp = self.dlg.findChild(QPushButton, "pushButton_mettre_a_jour_ebp")
        # QObject.connect(Button_mettre_a_jour_ebp, SIGNAL("clicked()"), self.update_p_ebp)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ZpboBuilder', message)


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


        # Create the dialog (after translation) and keep reference
        # self.dlg = BoiteDimensioningDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action



    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ZpboBuilder/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Crée zpbo jointives'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Zpbo Builder'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    # def run(self):
    #     """Run method that performs all the real work"""
    #     # get a list of all the layers in the map canvas
    #     layers = self.iface.legendInterface().layers()

    #     # reset all the comboboxes
    #     self.dlg.ui.combo_zpbo.clear()
    #     self.dlg.ui.combo_zsro.clear()
    #     self.dlg.ui.combo_t_noeud.clear() 

    #     # add the names of the layers to the comboboxes
    #     for layer in layers:
    #         self.dlg.ui.combo_zpbo.addItem(layer.name())
    #         self.dlg.ui.combo_zsro.addItem(layer.name())
    #         self.dlg.ui.combo_t_noeud.addItem(layer.name())

    #     # show the dialog
    #     self.dlg.show()
    #     # Run the dialog event loop
    #     result = self.dlg.exec_()
    #     # See if OK was pressed
    #     if result:
    #         # Do something useful here - delete the line containing pass and
    #         # substitute with your code.
    #         # print self.dlg.ui.density_spinbox.text()
    #         print type(self)
    #         print type(self.dlg)
    #         print type(self.dlg.ui)
    #         print type(self.dlg.ui.density_spinbox)
    #         print "zpbo: " + self.dlg.ui.combo_zpbo.currentText()
    #         print "zsro: " + self.dlg.ui.combo_zsro.currentText()
    #         print "t_noeud: " + self.dlg.ui.combo_t_noeud.currentText()
    #         print self.dlg.ui.density_spinbox.text()

    #         zpbo_name = self.dlg.ui.combo_zpbo.currentText()
    #         zsro_name = self.dlg.ui.combo_zsro.currentText()
    #         t_noeud_name = self.dlg.ui.combo_t_noeud.currentText()

    #         # The script

    #         import processing

    #         # Define the necissary layers

    #         zpbo = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName(zpbo_name)[0]
    #         t_noeud = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName(zsro_name)[0]
    #         zsro = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName(t_noeud_name)[0]

    #         temp = "D:/Mohannad/NRO101_temp_test/"

    #         # select only the nodes within zpbo
    #         processing.runalg("qgis:selectbylocation", t_noeud, zpbo, ['intersects'], 0, 0)

    #         # Generate random points within zpbo polygons
    #         processing.runalg("qgis:randompointsinsidepolygonsfixed", zpbo, 1, 0.1, 0.5, temp + "random_points.shp")

    #         # Load random points into the map
    #         random_points = self.iface.addVectorLayer(temp + "random_points.shp", "random_points", "ogr")
    #         if not random_points :
    #             print "random_points.shp failed to load"

             
    #         # Union the random points with t_noeud
    #         processing.runalg("qgis:union", random_points, t_noeud, temp + "union_random_t_noeud.shp")


    #         # Load the union layer into the map
    #         union = self.iface.addVectorLayer(temp + "union_random_t_noeud.shp", "union_random_t_noeud", "ogr")
    #         if not union :
    #             print "union_random_t_noeud.shp failed to load"
                

    #         # Delete the fields of t_noeud from the union layer
    #         for i in range(len(union.fields()) + 1):
    #             res = union.dataProvider().deleteAttributes([0])
    #             union.updateFields()
                

    #         # Get the extent of the union layer
    #         ext = union.extent()
    #         (xmax, xmin, ymax, ymin) = (ext.xMaximum(), ext.xMinimum(), ext.yMaximum(), ext.yMinimum())
    #         print "extent : " + str((xmax, xmin, ymax, ymin))


    #         # create two new points
    #         feat1 = qgis.core.QgsFeature(union.fields())
    #         feat1x = xmax + (xmax - xmin) 
    #         feat1y = ymin - (ymax - ymin)
    #         feat1.setGeometry(qgis.core.QgsGeometry.fromPoint(qgis.core.QgsPoint(feat1x, feat1y)))

    #         feat2 = qgis.core.QgsFeature(union.fields())
    #         feat2x = xmin - (xmax - xmin)
    #         feat2y = ymax + (ymax - ymin)
    #         feat2.setGeometry(qgis.core.QgsGeometry.fromPoint(qgis.core.QgsPoint(feat2x, feat2y)))

    #         # create a memory layer to hold the two points

    #         extend_lyr = qgis.core.QgsVectorLayer("Point?crs=epsg:2154", "extend_lyr", "memory")
    #         pr = extend_lyr.dataProvider()
    #         pr.addFeatures([feat1, feat2])
    #         fields = pr.fields()
    #         extend_lyr.updateExtents()

    #         # write the memory layer to the disk (We had a problem when trying to union the memory layer with the union layer)
    #         # problem solved
    #         error = qgis.core.QgsVectorFileWriter.writeAsVectorFormat(extend_lyr, temp + "extend_lyr.shp", "utf-8", None, "ESRI Shapefile")
    #         if error == qgis.core.QgsVectorFileWriter.NoError:
    #             print("success!")


    #         # union the union layer with the memory layer
    #         # processing.runalg("qgis:union", union, extend_lyr, temp + "union_extended.shp")


    #         # load the newly saved layer
    #         extend_lyr = self.iface.addVectorLayer(temp + "extend_lyr.shp", "extend_layer", "ogr")

    #         # union the union layer with the memory layer
    #         processing.runalg("qgis:union", union, extend_lyr, temp + "union_extended.shp")

    #         # load the new layer
    #         union_extended = self.iface.addVectorLayer(temp + "union_extended.shp", "union_extended", "ogr")

    #         # spatially join the point layer with zpbo
    #         union_joined = processing.runalg("qgis:joinattributesbylocation", union_extended, zpbo, u'intersects', 0, 0, 'mean', 1, temp + "union_points_joined.shp")

    #         # load the joined layer
    #         union_joined = self.iface.addVectorLayer(temp + "union_points_joined.shp", "union_joined", "ogr")

    #         # We had a problem with join by location tool, so we will depend temporarely on a layer created manually
    #         #voronoi = processing.runalg("qgis:voronoipolygons", temp + "union_points_joined_manual.shp", 0, temp + "voronoi.shp")

    #         # create Voronoi polygons
    #         voronoi = processing.runalg("qgis:voronoipolygons", union_joined, 0, temp + "voronoi.shp")

    #         # load voronoi layer
    #         voronoi = self.iface.addVectorLayer(temp + "voronoi.shp", "voronoi", "ogr")

    #         # dissolve voronoi polygons on the basis of zp_id
    #         processing.runalg("qgis:dissolve", voronoi, False, "zp_id", temp + "voronoi_dissolved.shp")

    #         # load voronoi dissolved layer
    #         voronoi_dissolved = self.iface.addVectorLayer(temp + "voronoi_dissolved.shp", "voronoi_dissolved", "ogr")

    #         # clip the dissolved layer by zsro polygon
    #         processing.runalg("qgis:clip", voronoi_dissolved, zsro, temp + "zpbo_final_zs_1")

    #         # add the clipped layer
    #         zpbo_final_zsro_1 = self.iface.addVectorLayer(temp + "zpbo_final_zs_1.shp", "zpbo_final_zsro_1", "ogr")

    #         # delete the field "FID" from the final layer
    #         res = zpbo_final_zsro_1.dataProvider().deleteAttributes([0])
    #         zpbo_final_zsro_1.updateFields()
                

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        # self.fenetreMessage(QMessageBox, "info", "within run method")
        self.GetParamBD(self.dlg.lineEdit_BD, self.dlg.lineEdit_Password, self.dlg.lineEdit_User, self.dlg.lineEdit_Host, self.dlg.Schema_grace)
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def fenetreMessage(self,typeMessage,titre,message):
        try:
            msg = QMessageBox()
            # msg.setIcon(typeMessage)
            msg.setWindowTitle(titre)
            msg.setText(str(message))
            msg.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)
            msg.exec_()
        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning,"Erreur_fenetreMessage",str(e))



    def GetParamBD(self, dbname, password, user, serveur, sche):
        try:
            path_absolute = QgsProject.instance().fileName()
            
            if path_absolute != "":
                
                
                tree = ET.parse(path_absolute)
                sche.setText("gracethd")
                root = tree.getroot()

                listeModify = []
                
                for source in root.iter('datasource'):
                    
                    if "dbname" in source.text : 
                        modify = str(source.text)
                        listeModify = modify.split("sslmode")
                        if len(listeModify) > 1:
                            
                            break

                if len(listeModify) > 1 :
                    
                    infosConnexion = listeModify[0].replace("'","")
                    infosConnexion = infosConnexion.split(" ")
                    for info in infosConnexion:
                        inf = info.split("=")
                        if inf[0] == "dbname":
                            dbname.setText(inf[1])
                        if inf[0] == "password":
                            password.setText(inf[1])
                        if inf[0] == "user":
                            user.setText(inf[1])
                        if inf[0] == "host":
                            serveur.setText(inf[1])
                    schemainfo = listeModify[1].replace("'","")
                    schemainfo = schemainfo.split(" ")
                    for sch in schemainfo:
                        sh = sch.split("=")
                        if sh[0] == "table":
                            schema = sh[1].split(".")
                            # sche.setText(schema[0].replace('"',''))
                            sche.setText("gracethd")
        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning,"Erreur_GetParamBD",str(e))
            # print str(e)


    def remplir_menu_deroulant_reference(self, combobox, rq_sql, DefValChamp):
        listVal = []
        combobox.clear()
        result = self.executerRequette(rq_sql, True)
        for elm in result:
            listVal.append(elm[0])
        combobox.addItems(listVal)
        try:
            combobox.setCurrentIndex(combobox.findText(DefValChamp))
        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning,"Erreur_remplir_menu_deroulant_reference",str(e))




    def executerRequette(self, Requette, boool):
        global conn
        try:
            cursor = conn.cursor()
            cursor.execute(Requette)
            conn.commit()
            if boool:
                result = cursor.fetchall()
                cursor.close()
                try :
                    if len(result)>0:
                        return result
                except:
                    return None
            else:
                cursor.close()
            
        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning,"Erreur_executerRequette",str(e))
            cursor.close()




    def connectToDb(self):
        global conn
        Host = self.dlg.lineEdit_Host.text()
        DBname = self.dlg.lineEdit_BD.text()
        User = self.dlg.lineEdit_User.text()
        Password = self.dlg.lineEdit_Password.text()
        Schema = self.dlg.Schema_grace.text()
        Schema_prod = self.dlg.Schema_prod.text()

        
        conn_string = "host='"+Host+"' dbname='"+DBname+"' user='"+User+"' password='"+Password+"'"

        try:
            conn = psycopg2.connect(conn_string)
            #recuperer tout les schemas
            shema_list=[]
            cursor = conn.cursor()
            sql =  "select schema_name from information_schema.schemata "
            cursor.execute(sql)
            result=cursor.fetchall()
            for elm in result:
                shema_list.append(elm[0].encode("utf8"))
            #passer au deuxieme onglet si la connexion est etablit et si le schema existe
            if Schema in shema_list:
                # Do Something
                # Enable the Comboboxes and Buttons

                self.dlg.findChild(QComboBox,"comboBox_zsro").setEnabled(True)
                self.dlg.findChild(QComboBox,"comboBox_zpbo").setEnabled(True)
                self.dlg.findChild(QComboBox,"comboBox_noeud").setEnabled(True)
                # self.dlg.findChild(QComboBox, "comboBox_ebp").setEnabled(True)
                # self.dlg.findChild(QComboBox, "comboBox_ptech").setEnabled(True)
                self.dlg.findChild(QComboBox, "comboBox_zs_refpm").setEnabled(True)
                self.dlg.findChild(QPushButton, "pushButton_verification").setEnabled(True)
                self.dlg.findChild(QPushButton, "pushButton_remove").setEnabled(True)
                # self.dlg.findChild(QPushButton, "pushButton_orientation").setEnabled(True)
                # self.dlg.findChild(QPushButton, "pushButton_verifier_orientation").setEnabled(True)

                # self.dlg.findChild(QPushButton, "pushButton_fibres_utiles").setEnabled(True)
                # self.dlg.findChild(QPushButton, "pushButton_dimensions").setEnabled(True)
                # self.dlg.findChild(QPushButton, "pushButton_verify_capacity").setEnabled(True)
                # self.dlg.findChild(QPushButton, "pushButton_mettre_a_jour_ebp").setEnabled(True)

                # self.dlg.findChild(QPushButton, "pushButton_mettre_a_jour_chemin")
                # self.dlg.findChild(QPushButton, "pushButton_mettre_a_jour_cable").setEnabled(True)
                # Disable connection button
                self.dlg.findChild(QPushButton, "pushButton_connexion").setEnabled(False)

                # Search for the names of the required tables in each schema
                # 1 - in gracethd
                self.remplir_menu_deroulant_reference(self.dlg.comboBox_zsro, ("SELECT tablename as table_lise FROM pg_tables WHERE schemaname = '"+self.dlg.Schema_grace.text()+"' ;"), 't_zsro')
                self.remplir_menu_deroulant_reference(self.dlg.comboBox_noeud, ("SELECT tablename as table_lise FROM pg_tables WHERE schemaname = '"+self.dlg.Schema_grace.text()+"' ;"), 't_noeud')
                
                # 2 - in prod
                self.remplir_menu_deroulant_reference(self.dlg.comboBox_zpbo, ("SELECT tablename as table_lise FROM pg_tables WHERE schemaname = '"+self.dlg.Schema_grace.text()+"' ;"), 't_zpbo')
                # self.remplir_menu_deroulant_reference(self.dlg.comboBox_ebp, ("SELECT tablename as table_lise FROM pg_tables WHERE schemaname = '"+self.dlg.Schema_prod.text()+"' ;"), 'p_ebp')
                # self.remplir_menu_deroulant_reference(self.dlg.comboBox_ptech, ("SELECT tablename as table_lise FROM pg_tables WHERE schemaname = '"+self.dlg.Schema_prod.text()+"' ;"), 'p_ptech') 
                # self.fenetreMessage(QMessageBox.Warning,"Query for zs_refpm", "SELECT zs_refpm FROM " + self.dlg.Schema_grace.text() + ".t_zsro;")
                # result = self.executerRequette("SELECT zs_refpm FROM " + self.dlg.Schema_grace.text() + ".t_zsro;", True)
                # for elm in result:
                #     print elm[0]
                #     self.fenetreMessage(QMessageBox.Warning,"result of query", elm[0])

                # 3 - ZSRO (zs_refpm)
                self.remplir_menu_deroulant_reference(self.dlg.comboBox_zs_refpm, ("SELECT zs_refpm as refpm FROM " + self.dlg.Schema_prod.text() + ".p_zsro ;"), 'PMT_26325_FO01')

                # print "SELECT zs_refpm FROM " + self.dlg.Schema_grace.text() + ".t_zsro;"


                print "Schema found"
                # self.dlg2.findChild(QPushButton,"pushButton_controle_avt_migration").setEnabled(True)
            else:
                # self.dlg2.findChild(QPushButton,"pushButton_controle_avt_migration").setEnabled(False)
                # self.dlg2.findChild(QPushButton,"pushButton_migration").setEnabled(False)
                print "Schema not found"
        except Exception as e:
                pass
          


    def generate_zpbo_jointives(self):
        zs_refpm = self.dlg.comboBox_zs_refpm.currentText()
        self.create_temp_zsro_table(zs_refpm)
        self.add_pg_layer("temp", "t_zsro_" +  zs_refpm.split("_")[2].lower())
        self.create_temp_zpbo_table(zs_refpm)
        self.add_pg_layer("temp", "t_zpbo_" +  zs_refpm.split("_")[2].lower())
        self.create_temp_noeud_table(zs_refpm)
        self.add_pg_layer("temp", "t_noeud_" +  zs_refpm.split("_")[2].lower())

        # -----------------------------------------------------------------------

        try:
            import processing

            zsro = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName("t_zsro_" +  zs_refpm.split("_")[2].lower())[0]
            zpbo = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName("t_zpbo_" +  zs_refpm.split("_")[2].lower())[0]
            t_noeud = qgis.core.QgsMapLayerRegistry.instance().mapLayersByName("t_noeud_" +  zs_refpm.split("_")[2].lower())[0]



            # temp = "D:/Mohannad/NRO55_temp_test/"
            temp = self.temp_folder
            result = self.result_folder

        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning, "Erreur_fenetreMessage", str(e))   
                    

        self.fenetreMessage(QMessageBox, "info", "random points will be generated")

        density = self.density_spinbox.value()

        # Generate random points within zpbo polygons
        processing.runalg("qgis:randompointsinsidepolygonsfixed", zpbo, 1, density, 0.5, temp + "random_points_" +  zs_refpm.split("_")[2].lower() + ".shp")




        self.fenetreMessage(QMessageBox, "info", "random points are generated. Density was = " + str(density))

        # Load random points into the map
        random_points = self.iface.addVectorLayer(temp + "random_points_" +  zs_refpm.split("_")[2].lower() + ".shp", "random_points_" +  zs_refpm.split("_")[2].lower(), "ogr")
        if not random_points :
            print "random_points_" +  zs_refpm.split("_")[2].lower() + ".shp failed to load"


        # Union the random points with t_noeud
        processing.runalg("qgis:union", random_points, t_noeud, temp + "union_random_t_noeud_" +  zs_refpm.split("_")[2].lower() + ".shp")


        # Load the union layer into the map
        union = self.iface.addVectorLayer(temp + "union_random_t_noeud_" +  zs_refpm.split("_")[2].lower() + ".shp", "union_random_t_noeud_" +  zs_refpm.split("_")[2].lower() + "", "ogr")
        if not union :
            print "union_random_t_noeud_" +  zs_refpm.split("_")[2].lower() + ".shp failed to load"


        # Delete the fields of t_noeud from the union layer
        for i in range(len(union.fields())):
            res = union.dataProvider().deleteAttributes([0])
            union.updateFields()
            

        # Get the extent of the union layer
        ext = union.extent()
        (xmax, xmin, ymax, ymin) = (ext.xMaximum(), ext.xMinimum(), ext.yMaximum(), ext.yMinimum())
        print "extent : " + str((xmax, xmin, ymax, ymin))


        # create two new points
        feat1 = QgsFeature(union.fields())
        feat1x = xmax + (xmax - xmin) / 1.5
        feat1y = ymin - (ymax - ymin) / 1.5
        feat1.setGeometry(QgsGeometry.fromPoint(QgsPoint(feat1x, feat1y)))

        feat2 = QgsFeature(union.fields())
        feat2x = xmin - (xmax - xmin) / 1.5
        feat2y = ymax + (ymax - ymin) / 1.5
        feat2.setGeometry(QgsGeometry.fromPoint(QgsPoint(feat2x, feat2y)))

        # create a memory layer to hold the two points

        extend_lyr = QgsVectorLayer("Point?crs=epsg:2154", "extend_lyr_" +  zs_refpm.split("_")[2].lower(), "memory")
        pr = extend_lyr.dataProvider()
        pr.addFeatures([feat1, feat2])
        fields = pr.fields()
        extend_lyr.updateExtents()

        # write the memory layer to the disk (We had a problem when trying to union the memory layer with the union layer)
        # problem solved
        error = QgsVectorFileWriter.writeAsVectorFormat(extend_lyr, temp + "extend_lyr_" +  zs_refpm.split("_")[2].lower() + ".shp", "utf-8", None, "ESRI Shapefile")
        if error == QgsVectorFileWriter.NoError:
            self.fenetreMessage(QMessageBox, "info", "Sucess")


        # union the union layer with the memory layer
        # processing.runalg("qgis:union", union, extend_lyr, temp + "union_extended.shp")

        self.fenetreMessage(QMessageBox, "info", "The layer extend_lyr will be loaded")

        # load the newly saved layer
        try:
            extend_lyr = self.iface.addVectorLayer(temp + "extend_lyr_" +  zs_refpm.split("_")[2].lower() + ".shp", "extend_layer_" +  zs_refpm.split("_")[2].lower(), "ogr")

        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning, "Erreur_fenetreMessage", str(e)) 
                    

        self.fenetreMessage(QMessageBox, "info", "The layer union_extended_" +  zs_refpm.split("_")[2].lower() + " is loaded")

        # union the union layer with the memory layer
        processing.runalg("qgis:union", union, extend_lyr, temp + "union_extended_" +  zs_refpm.split("_")[2].lower() + ".shp")

        # load the new layer
        union_extended = self.iface.addVectorLayer(temp + "union_extended_" +  zs_refpm.split("_")[2].lower() + ".shp", "union_extended_" +  zs_refpm.split("_")[2].lower(), "ogr")

        # spatially join the point layer with zpbo
        union_joined = processing.runalg("qgis:joinattributesbylocation", union_extended, zpbo, u'intersects', 0, 0, 'mean', 1, temp + "union_points_joined_" +  zs_refpm.split("_")[2].lower() + ".shp")

        # load the joined layer
        union_joined = self.iface.addVectorLayer(temp + "union_points_joined_" +  zs_refpm.split("_")[2].lower() + ".shp", "union_joined_" +  zs_refpm.split("_")[2].lower() + "", "ogr")


        # create Voronoi polygons
        voronoi = processing.runalg("qgis:voronoipolygons", union_joined, 0, temp + "voronoi_" +  zs_refpm.split("_")[2].lower() + ".shp")

        # load voronoi layer
        voronoi = self.iface.addVectorLayer(temp + "voronoi_" +  zs_refpm.split("_")[2].lower() + ".shp", "voronoi_" +  zs_refpm.split("_")[2].lower(), "ogr")


        # dissolve voronoi polygons on the basis of zp_id
        processing.runalg("qgis:dissolve", voronoi, False, "zp_uuid", temp + "voronoi_dissolved_" +  zs_refpm.split("_")[2].lower() + ".shp")


        # load voronoi dissolved layer
        voronoi_dissolved = self.iface.addVectorLayer(temp + "voronoi_dissolved_" +  zs_refpm.split("_")[2].lower() + ".shp", "voronoi_dissolved_" +  zs_refpm.split("_")[2].lower(), "ogr")

        # clip the dissolved layer by zsro polygon
        processing.runalg("qgis:clip", voronoi_dissolved, zsro, result + "zpbo_final_zs_" + zs_refpm.split("_")[2].lower())

        # add the clipped layer
        zpbo_final_zsro = self.iface.addVectorLayer(result + "zpbo_final_zs_" + zs_refpm.split("_")[2].lower() + ".shp", "zpbo_final_zsro_" + zs_refpm.split("_")[2].lower(), "ogr")

        # activate the button that removes the temporary layers
        self.dlg.findChild(QPushButton, "pushButton_remove").setEnabled(True)


   



    def create_temp_zsro_table(self, zs_refpm):
        # drop previous version if exists
        query_drop = "DROP TABLE IF EXISTS temp.t_zsro_" +  zs_refpm.split("_")[2] + " CASCADE;"
        # self.fenetreMessage(QMessageBox, "Drop!", query_drop)
        self.executerRequette(query_drop, False)
        # temporarry Cheminement table
        # query_inner = "SELECT * FROM temp.p_cheminement WHERE cm_zs_code like '%" + zs_refpm.split("_")[2] + "%' AND cm_typelog IN ('TD', 'DI', 'RA')"
        query_inner = "SELECT * FROM gracethd.t_zsro WHERE zs_refpm = '" + zs_refpm +"'"
        query_outer = """CREATE TABLE temp.t_zsro_""" + zs_refpm.split("_")[2] + """ as (""" + query_inner + """);
         ALTER TABLE temp.t_zsro_""" + zs_refpm.split("_")[2] + """ ADD PRIMARY KEY (zs_code);
         CREATE INDEX ON temp.t_zsro_""" + zs_refpm.split("_")[2] + """ USING GIST(geom); 
         """
        self.executerRequette(query_outer, False)



    def create_temp_noeud_table(self, zs_refpm):
        # drop previous version if exists
        query_drop = "DROP TABLE IF EXISTS temp.t_noeud_" +  zs_refpm.split("_")[2] + " CASCADE;"
        # self.fenetreMessage(QMessageBox, "Drop!", query_drop)
        self.executerRequette(query_drop, False)
        # temporarry Cheminement table
        # query_inner = "SELECT * FROM temp.p_cheminement WHERE cm_zs_code like '%" + zs_refpm.split("_")[2] + "%' AND cm_typelog IN ('TD', 'DI', 'RA')"
        query_inner = "SELECT nd.* FROM gracethd.t_noeud as nd JOIN temp.t_zsro_" + zs_refpm.split("_")[2] + " AS zs On ST_CONTAINS(zs.geom, nd.geom)"
        query_outer = """CREATE TABLE temp.t_noeud_""" + zs_refpm.split("_")[2] + """ as (""" + query_inner + """);
         ALTER TABLE temp.t_noeud_""" + zs_refpm.split("_")[2] + """ ADD PRIMARY KEY (nd_code);
         CREATE INDEX ON temp.t_noeud_""" + zs_refpm.split("_")[2] + """ USING GIST(geom);
         """
        self.executerRequette(query_outer, False)


    def create_temp_zpbo_table(self, zs_refpm):
        # drop previous version if exists
        query_drop = "DROP TABLE IF EXISTS temp.t_zpbo_" +  zs_refpm.split("_")[2] + " CASCADE;"
        # self.fenetreMessage(QMessageBox, "Drop!", query_drop)
        self.executerRequette(query_drop, False)
        # temporarry Cheminement table
        # query_inner = "SELECT * FROM temp.p_cheminement WHERE cm_zs_code like '%" + zs_refpm.split("_")[2] + "%' AND cm_typelog IN ('TD', 'DI', 'RA')"
        query_inner = "SELECT zp.* FROM gracethd.t_zpbo as zp JOIN temp.t_zsro_" + zs_refpm.split("_")[2] + " AS zs On zs_code = zp_zs_code"
        query_outer = """CREATE TABLE temp.t_zpbo_""" + zs_refpm.split("_")[2] + """ as (""" + query_inner + """);
         ALTER TABLE temp.t_zpbo_""" + zs_refpm.split("_")[2] + """ ADD PRIMARY KEY (zp_code);
         CREATE INDEX ON temp.t_zpbo_""" + zs_refpm.split("_")[2] + """ USING GIST(geom); 
         """
        self.executerRequette(query_outer, False)



    def add_pg_layer(self, schema, table_name):
        # Create a data source URI
        uri = QgsDataSourceURI()

        # set host name, port, database name, username and password
        uri.setConnection(self.dlg.lineEdit_Host.text(), "5432", self.dlg.lineEdit_BD.text(), self.dlg.lineEdit_User.text(), self.dlg.lineEdit_Password.text())

        # set database schema, table name, geometry column and optionally subset (WHERE clause)
        # uri.setDataSource('temp', 'cheminement_al01', "geom")
        uri.setDataSource(schema, table_name, "geom")

        vlayer = QgsVectorLayer(uri.uri(False), table_name, "postgres")

        # if not vlayer.isValid():
        #     self.fenetreMessage(QMessageBox, "Error", "The layer %s is not valid" % vlayer.name())
        #     return


        # check first if the layer is already added to the map
        layer_names = [layer.name() for layer in QgsMapLayerRegistry.instance().mapLayers().values()]
        if table_name not in layer_names:
            # Add the vector layer to the map
            QgsMapLayerRegistry.instance().addMapLayers([vlayer])
            self.fenetreMessage(QMessageBox, "Success", "Layer %s is loaded" % vlayer.name())

        else :
            self.fenetreMessage(QMessageBox, "Success", "Layer %s already exists but it has been updated" % vlayer.name())




    def select_temp_folder(self):

        QSettings().setValue("UI/lastProjectDir","D:/Mohannad")
        # self.temp_line_edit.text("test1")
        # fileName = QFileDialog.getOpenFileName()
        try:
            self.temp_folder = QFileDialog.getExistingDirectory(None, None, "C:/", QFileDialog.ShowDirsOnly) + "\\"
            self.temp_line_edit.setText(self.temp_folder)
            self.fenetreMessage(QMessageBox, "info", self.temp_folder)

        except Exception as e:
            self.fenetreMessage(QMessageBox.Warning, "Erreur_fenetreMessage", str(e))



    def select_result_folder(self):
        # QSettings().setValue("UI/lastProjectDir","D:/Mohannad")
        # fileName = QFileDialog.getOpenFileName()
        self.result_folder = QFileDialog.getExistingDirectory(None, None, "C:/", QFileDialog.ShowDirsOnly) + "\\"
        self.result_line_edit.setText(self.result_folder)
        self.fenetreMessage(QMessageBox, "info", self.result_folder)


    def remove_temp_layers(self):
        zs_refpm = self.dlg.comboBox_zs_refpm.currentText()
        zs_code = zs_refpm.split("_")[2].lower()
        layers_names = ["t_zpbo_" + zs_code, "t_zsro_" + zs_code, "t_noeud_" + zs_code, "random_points_" + zs_code,
        "union_random_t_noeud_" + zs_code, "extend_layer_" + zs_code, "union_extended_" + zs_code, "union_joined_" + zs_code,
        "voronoi_" + zs_code, "voronoi_dissolved_" + zs_code]

        for layer_name in layers_names:
            try:
                layer = QgsMapLayerRegistry.instance().mapLayersByName(layer_name)[0]
                shp_path = layer.dataProvider().dataSourceUri().split('|')[0]
                # self.fenetreMessage(QMessageBox, "info", layer.name)
                QgsMapLayerRegistry.instance().removeMapLayer(layer)
                QgsVectorFileWriter.deleteShapeFile(shp_path)
            except Exception as e:
                self.fenetreMessage(QMessageBox, "error", str(e))



