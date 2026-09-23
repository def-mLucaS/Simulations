from ..Entidades.PlantaInstalacao import PlantaInstalacao


class PlantaCabosExportacaoOnshore(PlantaInstalacao):
    def __init__(self, dictRoteamento):
        super().__init__(dictRoteamento)
