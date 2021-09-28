import logging
from utils.SimpleLogger import SimpleLogger


class ConsoleLogger(SimpleLogger):
    def __init__(self, logger_path: str, verbose_level: int = logging.INFO) -> None:
        handlers=[logging.StreamHandler()]
        if logger_path:
            handlers.append(logging.FileHandler(logger_path))
        
        logging.basicConfig(
            level=verbose_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers)
        self.log = logging.getLogger("ConsoleLogger")

    def debug(self, msg: str) -> None:
        self.log.debug(msg)

    def info(self, msg: str) -> None:
        self.log.info(msg)

    def warning(self, msg: str) -> None:
        self.log.warning(msg)

    def error(self, msg: str) -> None:
        self.log.error(msg)
