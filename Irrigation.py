from pydantic import BaseModel

class Irrigation(BaseModel):
    SoilMoisture: float 
    Temperature: float 
    SoilHumidity: float 