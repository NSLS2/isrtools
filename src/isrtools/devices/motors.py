"""Motor device definitions."""

from ophyd_async.core import StandardReadable
from ophyd_async.epics.core import EpicsDevice
from ophyd_async.epics.motor import Motor, VeloAndAcclRespectingMotorMock


class DCM(StandardReadable, EpicsDevice):
    """DCM motor device."""

    def __init__(self, prefix: str, name: str = ""):
        with self.add_children_as_readables():
            self.brag_th = Motor(prefix + "-Ax:th}Mtr")
            self.cb = Motor(prefix + "-Ax:CB}Mtr")
            self.z = Motor(prefix + "-Ax:Z}Mtr")
            self.y2 = Motor(prefix + "-Ax:Y2}Mtr")
            self.th2 = Motor(prefix + "-Ax:th2}Mtr")
            self.chi2 = Motor(prefix + "-Ax:chi2}Mtr")

            self.th2f = Motor(prefix + "-Ax:th2f}Mtr")
            self.chi2f = Motor(prefix + "-Ax:chi2f}Mtr")

        super().__init__(prefix, name=name)


Motor._mock_class = VeloAndAcclRespectingMotorMock  # noqa: SLF001
