import logging

from logging_setup import setup_root_logger
from processors.user import process_user

logger = logging.getLogger(__name__)


def main():
    logger.info("Application started")

    for user_id in range(1, 6):
        process_user(user_id)

    logger.info("Application finished")


if __name__ == "__main__":
    setup_root_logger()
    main()

    import requests
    requests.get("https://swapi.dev/api/people/1/?format=json")
