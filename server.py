from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import asyncio
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

async def run_modbus_server():
    _logger.info("Démarrage du serveur Modbus...")
    
    # Initialisation du datastore (simulation des registres Modbus)
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),  # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [17]*100),  # Coils
        hr=ModbusSequentialDataBlock(0, [17]*100),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [17]*100))  # Input Registers
    context = ModbusServerContext(slaves=store, single=True)

    # Identification du device
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    # Démarrer le serveur TCP
    _logger.info("Démarrage du serveur TCP sur localhost:5020...")
    await StartAsyncTcpServer(context, identity=identity, address=("localhost", 5020))
    _logger.info("Serveur démarré avec succès!")

if __name__ == "__main__":
    _logger.info("Initialisation de l'application...")
    asyncio.run(run_modbus_server())