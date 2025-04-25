def check_result_type(result, expected_type=str, fallback=""):
    """
    Checks if the result is of the expected type.
    If not, logs a warning and returns a fallback value.
    """
    from app.core.logger import logger

    if not isinstance(result, expected_type):
        logger.warning(f"Result type mismatch: expected {expected_type}, got {type(result)}. Returning fallback.")
        return fallback
    return result
