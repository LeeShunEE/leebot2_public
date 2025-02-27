@echo off
chcp 65001
REM 检查虚拟环境目录是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境，确保 "venv" 文件夹存在。
    pause
    exit /b 1
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 检查激活是否成功
if "%VIRTUAL_ENV%"=="" (
    echo [错误] 虚拟环境激活失败。
    pause
    exit /b 1
)

REM 运行 Leebot2
echo 正在启动 Nonebot2框架...
nb run

REM 暂停窗口以查看结果
pause
