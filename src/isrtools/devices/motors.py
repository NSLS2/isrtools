"""Motor device definitions."""

from ophyd_async.core import DeviceVector, SignalRW, StandardReadable, StandardReadableFormat as Format
from ophyd_async.epics.core import EpicsDevice, epics_signal_rw, epics_signal_r
from ophyd_async.epics.motor import Motor, VeloAndAcclRespectingMotorMock
from nslsii.ophyd_async.devices import XYPitchRollYawStage, MotorizedStage, AxisSuffix, XYStage
from typing import Annotated as A, Literal, cast


class DCM(StandardReadable, EpicsDevice):
    """DCM motor device."""

    def __init__(self, prefix: str, name: str = ""):
        with self.add_children_as_readables():
            self.energy = Motor(prefix + "-Ax:En}Mtr")
            self.brag_th = Motor(prefix + "-Ax:th}Mtr")
            self.cb = Motor(prefix + "-Ax:CB}Mtr")
            self.z = Motor(prefix + "-Ax:Z}Mtr")
            self.y2 = Motor(prefix + "-Ax:Y2}Mtr")
            self.th2 = Motor(prefix + "-Ax:th2}Mtr")
            self.chi2 = Motor(prefix + "-Ax:chi2}Mtr")

            #self.th2f = Motor(prefix + "-Ax:th2f}Mtr")
            #self.chi2f = Motor(prefix + "-Ax:chi2f}Mtr")

        super().__init__(prefix, name=name)


class FMPiezoBender(StandardReadable, EpicsDevice):

    def __init__(self, prefix: str, name: str = ""):
        with self.add_children_as_readables(Format.CONFIG_SIGNAL):
            self.feedback = epics_signal_rw(bool, prefix + "PID1.FBON")
            self.kp = epics_signal_rw(float, prefix + "PID1.KP")
            self.ki = epics_signal_rw(float, prefix + "PID1.KI")
            self.kd = epics_signal_rw(float, prefix + "PID1.KD")
            self.p = epics_signal_rw(float, prefix + "PID1.P")
            self.i = epics_signal_rw(float, prefix + "PID1.I")
            self.d = epics_signal_rw(float, prefix + "PID1.D")
            self.low_limit = epics_signal_rw(float, prefix + "PID1.DRVL")
            self.high_limit = epics_signal_rw(float, prefix + "PID1.DRVH")
            self.delta_time = epics_signal_rw(float, prefix + "PID1.DT")
        with self.add_children_as_readables(Format.HINTED_UNCACHED_SIGNAL):
            self.piezo_volt = epics_signal_rw(float, prefix + "E-I", prefix + "E-SP")
            self.output = epics_signal_r(float, prefix + "PID1.OVAL")
            self.bender_force = epics_signal_rw(float, prefix + "W-I", prefix + "PID1.VAL")
        super().__init__(prefix, name=name)


class FocusingMirror(XYPitchRollYawStage):

    xu: Motor
    xd: Motor
    yu: Motor
    ydo: Motor
    ydi: Motor

    def __init__(self, prefix: str, name: str = ""):
        with self.add_children_as_readables():
            self.piezo_bender = FMPiezoBender(prefix + "-Ax:Bender}")
        super().__init__(prefix, name=name)


class DPPSingle(StandardReadable, EpicsDevice):
    def __init__(self, prefix: str, number: Literal[1, 2], name: str = ""):
        with self.add_children_as_readables():
            self.x = Motor(prefix + f"-Ax:{number}X}}Mtr")
            self.y = Motor(prefix + f"-Ax:{number}Y}}Mtr")
            self.yaw = Motor(prefix + f"-Ax:{number}yaw}}Mtr")
            self.chi = Motor(prefix + f"-Ax:{number}chi}}Mtr")
            self.th = Motor(prefix + f"-Ax:{number}th}}Mtr")
            self.tth = Motor(prefix + f"-Ax:{number}tth}}Mtr")
            self.sample_y = Motor(prefix + f"-Ax:{number}Z}}Mtr")  # Why is sample y called z?
        super().__init__(prefix, name=name)


class DPP(MotorizedStage):
    table_x: A[Motor, AxisSuffix("Tbl_X")]
    table_y1: A[Motor, AxisSuffix("Tbl_YU")]
    table_y2: A[Motor, AxisSuffix("Tbl_YDI")]
    table_y3: A[Motor, AxisSuffix("Tbl_YDO")]
    pitch: A[Motor, AxisSuffix("Pitch")]

    def __init__(self, prefix: str, name: str = ""):
        self.dpp_components = DeviceVector(
            {
                i: DPPSingle(prefix, cast(Literal[1, 2], i)) for i in range(1, 3)
            }
        )
        super().__init__(prefix, name=name)



Motor._mock_class = VeloAndAcclRespectingMotorMock  # noqa: SLF001
