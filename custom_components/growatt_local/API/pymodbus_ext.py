"""
Extension for pymodbus with custom modbus function codes.
"""
from pymodbus.client.mixin import ModbusClientMixin, T
from pymodbus.pdu.decoders import DecodePDU
from pymodbus.pdu.register_message import ReadInputRegistersRequest, ReadInputRegistersResponse


class ReadMeterRegistersRequest(ReadInputRegistersRequest):
    """ReadMeterRegistersRequest."""

    function_code = 0x20


class ReadMeterRegistersResponse(ReadInputRegistersResponse):
    """ReadMeterRegistersResponse."""

    function_code = 0x20


DecodePDU.add_pdu(ReadMeterRegistersRequest, ReadMeterRegistersResponse)

def read_meter_registers(self,
                         address: int,
                         *,
                         count: int = 1,
                         device_id: int = 1,
                         no_response_expected: bool = False) -> T:
    """Read meter registers (code 0x20).

    :param address: Start address to read from
    :param count: (optional) Number of registers to read
    :param device_id: (optional) Modbus device ID
    :param no_response_expected: (optional) The client will not expect a response to the request
    :raises ModbusException:

    This function is used to read from 1 to approx. 50 contiguous
    meter registers in a remote device. The Request specifies the
    starting register address and the number of registers.

    Registers are addressed starting at zero.
    Therefore devices that specify 1-16 are addressed as 0-15.
    """
    return self.execute(no_response_expected, ReadMeterRegistersRequest(address=address, count=count, dev_id=device_id))

ModbusClientMixin.read_meter_registers = read_meter_registers  # ty:ignore[unresolved-attribute]