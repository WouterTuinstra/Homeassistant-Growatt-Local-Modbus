class ModbusException(Exception):
    """Raised when the Modbus communication has error."""

    def __init__(self, status):
        """Initialize."""
        super(ModbusException, self).__init__(status)
        self.status = status


class ModbusPortException(ModbusException):
    """Raised when the Serial port in not available."""
