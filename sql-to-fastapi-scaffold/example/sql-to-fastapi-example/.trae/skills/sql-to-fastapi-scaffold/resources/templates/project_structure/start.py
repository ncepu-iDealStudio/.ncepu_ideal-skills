"""应用入口文件

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

import uvicorn
from config import settings
from app import create_app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "start:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
