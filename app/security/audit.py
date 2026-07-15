import logging
logger = logging.getLogger("audit")
def audit_log(actor: str, action: str, resource: str, status: str = "success", **extra) -> None:
    """所有敏感操作/工具调用都要审计。Week3接入不可篡改存储。"""
    logger.info(
    "AUDIT",
    extra={}, # trace_id由logging中间件注入
    )

    logger.info(
    f"actor={actor} action={action} resource={resource} "
    f"status={status} extra={extra}"
    )
