@echo off
echo Building Orion System Components...

echo.
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Building Go captcha solver...
go mod tidy
go build -o captcha_solver.exe captcha_solver.go

echo.
echo [3/4] Building Rust proxy manager...
cargo build --release

echo.
echo [4/4] Setting up configuration files...
if not exist captcha_config.json (
    echo {"api_keys": {"2captcha": null, "anticaptcha": null}} > captcha_config.json
)

if not exist payment_config.json (
    echo {"wallets": {"bitcoin": "bc1qtj2huh70untgqarkm8g5d362qd657a3mk369j3", "ethereum": "0xAE909dDcf7e38F7Ed866c17D7245b36E8077dc77"}, "api_keys": {"etherscan": null}} > payment_config.json
)

echo.
echo Build complete! Orion system ready for deployment.
echo.
echo To start:
echo 1. Run: python orion_core.py
echo 2. Or use individual modules as needed
echo.
pause