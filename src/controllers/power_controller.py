# src/controllers/power_controller.py

import subprocess
import ctypes
from typing import List, Dict

from utils import get_logger, PowerControlError, handle_error

logger = get_logger(__name__)

class PowerController:
    def __init__(self):
        self.power_plans = self._get_power_plans()

    def shutdown(self) -> Dict[str, str]:
        """
        Shut down the system.

        Returns:
            Dict[str, str]: A dictionary with the status of the operation.
        """
        try:
            logger.info("Initiating system shutdown")
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            return {"status": "success", "message": "Shutdown initiated"}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initiate shutdown: {str(e)}")
            raise PowerControlError(f"Failed to initiate shutdown: {str(e)}")

    def restart(self) -> Dict[str, str]:
        """
        Restart the system.

        Returns:
            Dict[str, str]: A dictionary with the status of the operation.
        """
        try:
            logger.info("Initiating system restart")
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            return {"status": "success", "message": "Restart initiated"}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initiate restart: {str(e)}")
            raise PowerControlError(f"Failed to initiate restart: {str(e)}")

    def sleep(self) -> Dict[str, str]:
        """
        Put the system to sleep.

        Returns:
            Dict[str, str]: A dictionary with the status of the operation.
        """
        try:
            logger.info("Putting system to sleep")
            ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
            return {"status": "success", "message": "Sleep mode initiated"}
        except Exception as e:
            logger.error(f"Failed to initiate sleep mode: {str(e)}")
            raise PowerControlError(f"Failed to initiate sleep mode: {str(e)}")

    def hibernate(self) -> Dict[str, str]:
        """
        Put the system into hibernation.

        Returns:
            Dict[str, str]: A dictionary with the status of the operation.
        """
        try:
            logger.info("Putting system into hibernation")
            subprocess.run(["shutdown", "/h"], check=True)
            return {"status": "success", "message": "Hibernation initiated"}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initiate hibernation: {str(e)}")
            raise PowerControlError(f"Failed to initiate hibernation: {str(e)}")

    def _get_power_plans(self) -> List[Dict[str, str]]:
        """
        Get the list of available power plans.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing power plan information.
        """
        try:
            output = subprocess.check_output(["powercfg", "/list"], universal_newlines=True)
            plans = []
            for line in output.split('\n'):
                if "GUID" in line:
                    guid = line.split(':')[1].split('(')[0].strip()
                    name = line.split('(')[1].split(')')[0].strip()
                    plans.append({"guid": guid, "name": name})
            return plans
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get power plans: {str(e)}")
            return []

    def get_power_plans(self) -> List[Dict[str, str]]:
        """
        Get the list of available power plans.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing power plan information.
        """
        return self.power_plans

    def set_power_plan(self, guid: str) -> Dict[str, str]:
        """
        Set the active power plan.

        Args:
            guid (str): The GUID of the power plan to set.

        Returns:
            Dict[str, str]: A dictionary with the status of the operation.
        """
        try:
            logger.info(f"Setting power plan to GUID: {guid}")
            subprocess.run(["powercfg", "/setactive", guid], check=True)
            return {"status": "success", "message": f"Power plan set to {guid}"}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to set power plan: {str(e)}")
            raise PowerControlError(f"Failed to set power plan: {str(e)}")

# Example usage
if __name__ == "__main__":
    controller = PowerController()
    print("Available power plans:")
    for plan in controller.get_power_plans():
        print(f"Name: {plan['name']}, GUID: {plan['guid']}")
    
    # Uncomment to test (be careful with shutdown/restart/sleep/hibernate commands!)
    # print(controller.set_power_plan("381b4222-f694-41f0-9685-ff5bb260df2e"))  # Balanced plan GUID
    # print(controller.sleep())