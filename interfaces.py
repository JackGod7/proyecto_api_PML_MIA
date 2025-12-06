from abc import ABC, abstractmethod
import pandas as pd

class FuenteDeDatos(ABC):
    """
    Interfaz para fuentes de datos.
    """
    
    @abstractmethod
    def obtener_datos(self) -> pd.DataFrame:
        """
        Método obligatorio para obtener datos desde la fuente específica.
        """
        pass