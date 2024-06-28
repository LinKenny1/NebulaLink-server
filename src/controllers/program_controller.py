# src/controllers/program_controller.py

import psutil
from typing import List, Dict
from src.utils import get_logger, ProgramControlError

logger = get_logger(__name__)


class ProgramController:
    def get_running_programs(self) -> List[Dict[str, str]]:
        try:
            programs = []
            for proc in psutil.process_iter(["pid", "name"]):
                programs.append({"pid": proc.info["pid"], "name": proc.info["name"]})
            return programs
        except Exception as e:
            logger.error(f"Failed to get running programs: {str(e)}")
            raise ProgramControlError(f"Failed to get running programs: {str(e)}")

    def pause_program(self, pid: int) -> Dict[str, str]:
        try:
            process = psutil.Process(pid)
            process.suspend()
            logger.info(f"Paused program with PID {pid}")
            return {"status": "success", "message": f"Program with PID {pid} paused"}
        except psutil.NoSuchProcess:
            logger.error(f"No process found with PID {pid}")
            raise ProgramControlError(f"No process found with PID {pid}")
        except Exception as e:
            logger.error(f"Failed to pause program: {str(e)}")
            raise ProgramControlError(f"Failed to pause program: {str(e)}")

    def resume_program(self, pid: int) -> Dict[str, str]:
        try:
            process = psutil.Process(pid)
            process.resume()
            logger.info(f"Resumed program with PID {pid}")
            return {"status": "success", "message": f"Program with PID {pid} resumed"}
        except psutil.NoSuchProcess:
            logger.error(f"No process found with PID {pid}")
            raise ProgramControlError(f"No process found with PID {pid}")
        except Exception as e:
            logger.error(f"Failed to resume program: {str(e)}")
            raise ProgramControlError(f"Failed to resume program: {str(e)}")


if __name__ == "__main__":
    controller = ProgramController()
    print(controller.get_running_programs())
    # Be careful when testing pause and resume!
    # print(controller.pause_program(1234))
    # print(controller.resume_program(1234))
