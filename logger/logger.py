import logging

# Configure logging only once at module level
_logging_configured = False


def get_logger(scope: str, level=logging.DEBUG):
    """
    get_logger - Returns a logger instance for the given scope.
    Configures logging format only once to prevent duplicate log messages.
    """
    global _logging_configured
    
    if not _logging_configured:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
        )
        _logging_configured = True
    
    return logging.getLogger(scope)
