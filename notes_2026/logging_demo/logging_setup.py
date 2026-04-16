import logging
import sys
from pythonjsonlogger.json import JsonFormatter


class Filter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return "Application" not in record.getMessage()


def setup_root_logger():
    root_loger = logging.getLogger()
    root_loger.setLevel(logging.DEBUG)

    log_format = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
    formater = logging.Formatter(log_format)

    json_formater = JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(module)s %(message)s",
        rename_fields={"levelname": "level"},
        static_fields={"version": "1.34.12",
                       "environment": "production"}
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formater)
    handler.addFilter(Filter())
    root_loger.addHandler(handler)

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(json_formater)
    file_handler.addFilter(Filter())
    root_loger.addHandler(file_handler)
