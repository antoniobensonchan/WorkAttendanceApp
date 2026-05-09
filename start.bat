@echo off
chcp 65001 >nul
echo ========================================
echo   企业工地考勤管理系统 - 启动脚本
echo ========================================
echo.
echo 正在启动服务器...
echo.
echo 访问地址:
echo   本机访问: http://localhost:8501
echo   局域网访问: http://[您的IP地址]:8501
echo.
echo 提示: 按 Ctrl+C 可停止服务器
echo.
echo ========================================
echo.

streamlit run main.py --server.port=8501 --server.address=0.0.0.0

pause
