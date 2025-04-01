import sys
from datetime import datetime
from loguru import logger as _logger
from pathlib import Path


# 默认日志级别
PRINT_LEVEL = "INFO"
LOGFILE_LEVEL = "DEBUG"
PROJECT_ROOT =Path(__file__).resolve().parent  # 获取项目根目录的绝对路径


def setup_logger(print_level=PRINT_LEVEL, logfile_level=LOGFILE_LEVEL, name: str = None, log_to_file: bool = True):
    """配置 Loguru 日志"""
    _logger.remove()  # 清除默认的日志处理器

    # 生成日志文件名
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    log_name = f"{name}_{current_date}" if name else current_date
    log_file_path = PROJECT_ROOT / f"logs/{log_name}.log"

    # 控制台日志
    _logger.add(
        sys.stdout,  # 输出到控制台
        level=print_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8"
    )

    # 文件日志
    if log_to_file:
        _logger.add(
            log_file_path,  # 输出到文件
            level=logfile_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            encoding="utf-8",
            rotation=0,  # "10 MB" 日志文件达到 10MB 自动分割
            retention="7 days",  # 只保留 7 天的日志
            compression=None  # "zip"  旧日志压缩存储
        )
    
    return _logger


# 初始化 logger
logger = setup_logger()

__all__ = [
    "logger"
]