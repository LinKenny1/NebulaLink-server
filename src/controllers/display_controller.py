# src/controllers/display_controller.py

import ctypes
import ctypes.wintypes
import win32api  # type: ignore
import win32con  # type: ignore
from typing import List, Dict, Any
from src.utils import get_logger, DisplayControlError

logger = get_logger(__name__)


# Windows API structures and constants
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.wintypes.WORD),
        ("dmDriverVersion", ctypes.wintypes.WORD),
        ("dmSize", ctypes.wintypes.WORD),
        ("dmDriverExtra", ctypes.wintypes.WORD),
        ("dmFields", ctypes.wintypes.DWORD),
        ("dmPositionX", ctypes.wintypes.LONG),
        ("dmPositionY", ctypes.wintypes.LONG),
        ("dmDisplayOrientation", ctypes.wintypes.DWORD),
        ("dmDisplayFixedOutput", ctypes.wintypes.DWORD),
        ("dmColor", ctypes.wintypes.SHORT),
        ("dmDuplex", ctypes.wintypes.SHORT),
        ("dmYResolution", ctypes.wintypes.SHORT),
        ("dmTTOption", ctypes.wintypes.SHORT),
        ("dmCollate", ctypes.wintypes.SHORT),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.wintypes.WORD),
        ("dmBitsPerPel", ctypes.wintypes.DWORD),
        ("dmPelsWidth", ctypes.wintypes.DWORD),
        ("dmPelsHeight", ctypes.wintypes.DWORD),
        ("dmDisplayFlags", ctypes.wintypes.DWORD),
        ("dmDisplayFrequency", ctypes.wintypes.DWORD),
        ("dmICMMethod", ctypes.wintypes.DWORD),
        ("dmICMIntent", ctypes.wintypes.DWORD),
        ("dmMediaType", ctypes.wintypes.DWORD),
        ("dmDitherType", ctypes.wintypes.DWORD),
        ("dmReserved1", ctypes.wintypes.DWORD),
        ("dmReserved2", ctypes.wintypes.DWORD),
        ("dmPanningWidth", ctypes.wintypes.DWORD),
        ("dmPanningHeight", ctypes.wintypes.DWORD),
    ]


class DisplayController:
    def __init__(self):
        self.displays = self._get_displays()

    def _get_displays(self) -> List[Dict[str, Any]]:
        displays = []
        i = 0
        while True:
            try:
                device = win32api.EnumDisplayDevices(None, i)
                settings = win32api.EnumDisplaySettings(
                    device.DeviceName, win32con.ENUM_CURRENT_SETTINGS
                )
                displays.append(
                    {
                        "id": i,
                        "name": device.DeviceName,
                        "friendly_name": device.DeviceString,
                        "resolution": f"{settings.PelsWidth}x{settings.PelsHeight}",
                        "refresh_rate": settings.DisplayFrequency,
                    }
                )
                i += 1
            except win32api.error:
                break
        return displays

    def get_display_info(self) -> List[Dict[str, Any]]:
        return self.displays

    def set_resolution(
        self, display_id: int, width: int, height: int
    ) -> Dict[str, str]:
        try:
            if display_id < 0 or display_id >= len(self.displays):
                raise DisplayControlError(f"Invalid display ID: {display_id}")

            device_name = self.displays[display_id]["name"]
            devmode = DEVMODE()
            devmode.dmSize = ctypes.sizeof(DEVMODE)
            devmode.dmDriverExtra = 0
            devmode.dmFields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
            devmode.dmPelsWidth = width
            devmode.dmPelsHeight = height

            result = ctypes.windll.user32.ChangeDisplaySettingsExW(
                device_name,
                ctypes.byref(devmode),
                None,
                win32con.CDS_UPDATEREGISTRY,
                None,
            )

            if result == win32con.DISP_CHANGE_SUCCESSFUL:
                logger.info(
                    f"Resolution of display {display_id} set to {width}x{height}"
                )
                return {
                    "status": "success",
                    "message": f"Resolution set to {width}x{height}",
                }
            else:
                raise DisplayControlError(
                    f"Failed to set resolution. Error code: {result}"
                )
        except DisplayControlError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Failed to set resolution: {str(e)}")
            raise DisplayControlError(f"Failed to set resolution: {str(e)}")

    def set_refresh_rate(self, display_id: int, rate: int) -> Dict[str, str]:
        try:
            if display_id < 0 or display_id >= len(self.displays):
                raise DisplayControlError(f"Invalid display ID: {display_id}")

            device_name = self.displays[display_id]["name"]
            devmode = DEVMODE()
            devmode.dmSize = ctypes.sizeof(DEVMODE)
            devmode.dmDriverExtra = 0
            devmode.dmFields = win32con.DM_DISPLAYFREQUENCY
            devmode.dmDisplayFrequency = rate

            result = ctypes.windll.user32.ChangeDisplaySettingsExW(
                device_name,
                ctypes.byref(devmode),
                None,
                win32con.CDS_UPDATEREGISTRY,
                None,
            )

            if result == win32con.DISP_CHANGE_SUCCESSFUL:
                logger.info(f"Refresh rate of display {display_id} set to {rate}Hz")
                return {"status": "success", "message": f"Refresh rate set to {rate}Hz"}
            else:
                raise DisplayControlError(
                    f"Failed to set refresh rate. Error code: {result}"
                )
        except DisplayControlError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Failed to set refresh rate: {str(e)}")
            raise DisplayControlError(f"Failed to set refresh rate: {str(e)}")

    def enable_dummy_display(self) -> Dict[str, str]:
        # This functionality requires a third-party driver like Mirage Driver
        # For now, we'll just log the action and return a placeholder response
        logger.info("Enabling dummy display (placeholder)")
        return {"status": "success", "message": "Dummy display enabled (placeholder)"}

    def disable_dummy_display(self) -> Dict[str, str]:
        # This functionality requires a third-party driver like Mirage Driver
        # For now, we'll just log the action and return a placeholder response
        logger.info("Disabling dummy display (placeholder)")
        return {"status": "success", "message": "Dummy display disabled (placeholder)"}


if __name__ == "__main__":
    controller = DisplayController()
    print(controller.get_display_info())
    # Uncomment to test (be careful with changing display settings!)
    # print(controller.set_resolution(0, 1920, 1080))
    # print(controller.set_refresh_rate(0, 60))
    print(controller.enable_dummy_display())
    print(controller.disable_dummy_display())
