from fastapi import FastAPI, HTTPException
from pymodbus.client import ModbusTcpClient
import logging
import asyncio

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

app = FastAPI()

def create_modbus_client():
    try:
        client = ModbusTcpClient('localhost', port=5020)
        if not client.connect():
            raise Exception("Impossible de se connecter au serveur Modbus")
        return client
    except Exception as e:
        _logger.error(f"Erreur de connexion Modbus: {str(e)}")
        raise HTTPException(status_code=503, detail="Serveur Modbus inaccessible")

@app.get("/read_holding_registers/{address}/{count}")
async def read_holding_registers(
    address: int,  # Adresse de départ du registre Modbus à lire (0-65535)
    count: int     # Nombre de registres consécutifs à lire à partir de l'adresse
):
    try:
        client = create_modbus_client()
        response = client.read_holding_registers(address, count)
        client.close()
        
        if response is None:
            raise HTTPException(status_code=500, detail="Erreur de lecture des registres")
            
        if response.isError():
            raise HTTPException(status_code=400, detail=str(response))
            
        return {"data": response.registers}
        
    except Exception as e:
        _logger.error(f"Erreur lors de la lecture: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write_holding_register/{address}/{value}")
async def write_holding_register(
    address: int,  # Adresse du registre Modbus où écrire (0-65535)
    value: int     # Valeur à écrire dans le registre (0-65535)
):
    try:
        # Validation des entrées
        if not 0 <= address <= 65535:
            raise HTTPException(status_code=400, detail="Adresse invalide (doit être entre 0 et 65535)")
        if not 0 <= value <= 65535:
            raise HTTPException(status_code=400, detail="Valeur invalide (doit être entre 0 et 65535)")

        client = create_modbus_client()
        # Ajout d'un délai pour s'assurer que la connexion est établie
        await asyncio.sleep(0.1)
        
        response = client.write_register(address, value)
        client.close()
        
        if response is None or response.isError():
            error_msg = str(response) if response else "Erreur d'écriture du registre"
            _logger.error(f"Erreur Modbus: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
            
        return {"status": "success", "address": address, "value": value}
        
    except Exception as e:
        _logger.error(f"Erreur lors de l'écriture: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    _logger.info("Démarrage de l'API FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8088)