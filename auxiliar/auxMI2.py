# -*- coding: utf-8 -*-
import os

class Auxiliar:

    def __init__(self):
        super(Auxiliar, self).__init__()
        '''Constructor'''

    def pathGpkg(self):
        filePath = os.path.dirname(__file__)
        filePathGpkg = os.path.join(filePath, "shp", "mapaIndice.gpkg")
        return filePathGpkg

