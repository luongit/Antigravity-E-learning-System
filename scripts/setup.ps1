<#
.SYNOPSIS
    Script thiết lập môi trường 1 chạm cho Hệ thống Sản xuất E-Learning & Video Animation.
.DESCRIPTION
    Tự động:
    1. Thiết lập Python Virtual Environment (.venv) & cài thư viện lõi.
    2. Cài đặt các thư viện Node.js cho HyperFrames Renderer (engines/hyperframes/renderer).
    3. Kiểm tra FFmpeg và các công cụ render.
.EXAMPLE
    .\scripts\setup.ps1
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 BẮT ĐẦU THIẾT LẬP MÔI TRƯỜNG DỰ ÁN E-LEARNING (1-CLICK SETUP)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Kiểm tra Python
$pyCmd = ""
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pyCmd = "py -3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pyCmd = "python"
} else {
    Write-Host "❌ Không tìm thấy Python! Vui lòng cài đặt Python 3.10+ từ python.org" -ForegroundColor Red
    exit 1
}

# 2. Chạy prepare_env.py
Invoke-Expression "$pyCmd scripts/prepare_env.py"

Write-Host "Hoàn tất thiết lập môi trường!" -ForegroundColor Green
