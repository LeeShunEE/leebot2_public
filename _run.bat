@echo off
setlocal

:: 启动 NapCat.Shell_run.bat
echo Starting NapCat.Shell_run.bat...
if not exist "NapCat.Shell\_run.bat" (
    echo NapCat.Shell_run.bat does not exist. Exiting...
    exit /b 1
)
pushd NapCat.Shell
start _run.bat > NapCat_Shell_run.log 2>&1
popd
:: 检查是否启动成功
if %errorlevel% neq 0 (
    echo Failed to start NapCat.Shell_run.bat. Exiting...
    exit /b %errorlevel%
)


:: 启动 container\__run_no_env.bat
echo Starting container\__run_no_env.bat...
if not exist "container\__run_no_env.bat" (
    echo container\__run_no_env.bat does not exist. Exiting...
    exit /b 1
)
pushd container
start __run_no_env.bat > container_run_no_env.log 2>&1
popd

:: 检查是否启动成功
if %errorlevel% neq 0 (
    echo Failed to start container\__run_no_env.bat. Exiting...
    exit /b %errorlevel%
)

echo Both scripts started successfully.
pause