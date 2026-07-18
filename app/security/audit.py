import logging
logger = logging.getLogger("audit")

def audit_log(actor: str, action: str, resource: str, status: str = "success", **extra) -> None:
    """security operation starts from week3。"""
    logger.info(
    "AUDIT",
    extra={}, # trace_id added from logging middleware
    )
    logger.info(
    f"actor={actor} action={action} resource={resource} "
    f"status={status} extra={extra}"
    )
