import logging

from processors.user import process_user


logging.basicConfig(
    level=logging.WARN,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Application started")

    for user_id in range(1, 6):
        process_user(user_id)

    logger.info("Application finished")


if __name__ == "__main__":
    main()
