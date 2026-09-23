import math


class Porto():
    def __init__(self,nome,latitude,longitude):
        self._nome = nome
        self._latitude = latitude
        self._longitude = longitude
        # self.velocidade_maxima_permitida = math.inf


    def getLatitude(self):
        return self._latitude

    def getLongitude(self):
        return self._longitude

    def getNome(self):
        return self._nome

    def getCoordenadas(self):
        return (self._latitude,self._longitude)