import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def checkout(cmd, text):
   
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            encoding="utf-8"
        )
        if text in result.stdout and result.returncode == 0:
            return True
        else:
            
            logger.error(
                f"Command: {cmd}\n"
                f"Output: {result.stdout}\n"
                f"Error: {result.stderr}\n"
                f"Return code: {result.returncode}"
            )
            return False
    except Exception as e:
        logger.exception(f"Error runtime '{cmd}': {e}")
        return False
