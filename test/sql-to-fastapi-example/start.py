"""应用入口文件

此文件由 SQL-to-FastAPI-Scaffold 自动生成

推荐启动方式（uv）：
    uv run uvicorn start:app --reload
    uv run python start.py
"""

import uvicorn

from app import create_app
from config import settings


app = create_app()


def main() -> None:
    """供 `uv run python start.py` 或直接 `python start.py` 调用的入口。"""
    uvicorn.run(
        "start:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
