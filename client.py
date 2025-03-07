import asyncio
from pymodbus.client import ModbusTcpClient

async def test_client():
    client = ModbusTcpClient('localhost', port=5020)
    client.connect()
    result = client.read_holding_registers(0, 1)
    print(f"Valeur lue : {result.registers}")
    client.close()

if __name__ == "__main__":
    asyncio.run(test_client())