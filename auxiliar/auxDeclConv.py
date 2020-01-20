# -*- coding: UTF-8 -*-
from qgis.core import *
import math

class AuxiliarDeclConv(object):
    
    def __init__(self, iface):
        super(AuxiliarDeclConv, self).__init__()
        self.iface = iface
        
    def calculateKappa(self, point):
        """Calculates the linear deformation factor (Kappa) for UTM projections
        """
        kappaZero = 0.9996
        latitude = float(point.y())
        longitude = float(point.x())
        centralMeridian = int(abs(longitude)/6)*6 + 3
        if longitude < 0:
            centralMeridian = centralMeridian*(-1)
        
        b = math.cos(math.radians(latitude))*math.sin(math.radians(longitude - centralMeridian))
        
        k = kappaZero/math.sqrt(1 - b*b)
        
        return k
    
    def calculateConvergence(self, point):
        """Calculates the meridian convergence
        """
        latitude = point.y()
        longitude = point.x()

        (a, b) = self.getSemiMajorAndSemiMinorAxis()
        
        centralMeridian = self.getCentralMeridian(longitude)

        deltaLong = abs( centralMeridian - longitude )

        p = 0.0001*( deltaLong*3600 )

        xii = math.sin(math.radians(latitude))*math.pow(10, 4)

        e2 = math.sqrt(a*a - b*b)/b

        c5 = math.pow(math.sin(math.radians(1/3600)), 4)*math.sin(math.radians(latitude))*math.pow(math.cos(math.radians(latitude)), 4)*(2 - math.pow(math.tan(math.radians(latitude)), 2))*math.pow(10, 20)/15

        xiii = math.pow(math.sin(math.radians(1/3600)), 2)*math.sin(math.radians(latitude))*math.pow(math.cos(math.radians(latitude)), 2)*(1 + 3*e2*e2*math.pow(math.cos(math.radians(latitude)), 2) + 2*math.pow(e2, 4)*math.pow(math.cos(math.radians(latitude)), 4))*math.pow(10, 12)/3

        cSeconds = xii*p + xiii*math.pow(p, 3) + c5*math.pow(p, 5)

        if abs(longitude) < abs(centralMeridian):
            c = -cSeconds/3600
        else:
            c = cSeconds/3600

        return c

    def getSemiMajorAndSemiMinorAxis(self):
        """Obtains the semi major axis and semi minor axis from the used ellipsoid
        """
        distanceArea = QgsDistanceArea()
        distanceArea.setEllipsoid(self.iface.mapCanvas().mapSettings().destinationCrs().ellipsoidAcronym())
        a = distanceArea.ellipsoidSemiMajor()
        b = distanceArea.ellipsoidSemiMinor()
        
        return (a,b)
    
    def getPlanarCoordinates(self, lon, lat):
        """Transform the geographic coordinates to projected coordinates
        """
        crsDest = self.iface.mapCanvas().mapRenderer().destinationCrs()
        crsSrc = QgsCoordinateReferenceSystem(crsDest.geographicCRSAuthId())
        
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
        
        utmPoint = coordinateTransformer.transform(QgsPoint(lon, lat))
        
        return utmPoint

    def getGeographicCoordinates(self, ponto):
        """Transform the planar coordinates to geographic coordinates
        """
        crsSrc = self.iface.mapCanvas().mapRenderer().destinationCrs()
        crsDest = QgsCoordinateReferenceSystem(crsSrc.geographicCRSAuthId())

        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject())

        geoPoint = coordinateTransformer.transform(ponto)

        return geoPoint

    def getReprojection(self, ponto, crsSrc, crsDest):
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance())
        repPoint = coordinateTransformer.transform(ponto)
        return repPoint
    
    def getCentralMeridian(self, longitude):
        centralMeridian = int(abs(longitude)/6)*6 + 3
        if longitude < 0:
            centralMeridian = centralMeridian*(-1)

        return centralMeridian
