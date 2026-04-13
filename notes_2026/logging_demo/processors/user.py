import logging
import random
import time


logger = logging.getLogger(__name__)


def process_user(user_id: int):
    logger.info(f"Start processing user {user_id}")

    # Імітація випадкових ситуацій
    action = random.choice(["ok", "slow", "error"])

    if action == "ok":
        logger.debug(f"User {user_id}: normal processing")
        time.sleep(0.5)
        logger.info(f"User {user_id}: processed successfully")

    elif action == "slow":
        logger.warning(f"User {user_id}: slow response detected")
        time.sleep(1.5)
        logger.info(f"User {user_id}: processed with delay")

    elif action == "error":
        try:
            raise ValueError("Something went wrong!")
        except Exception as e:
            logger.error(f"User {user_id}: error occurred: {e}")
