@echo off
chcp 65001

REM 检查虚拟环境目录是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境，确保 ".venv" 文件夹存在。
    pause
    exit /b 1
)

REM 启动新命令行窗口并激活虚拟环境
start cmd /K ".venv\Scripts\activate.bat"

REM 检查是否成功启动
if "%VIRTUAL_ENV%"=="" (
    echo [错误] 虚拟环境激活失败。
    pause
    exit /b 1
)
