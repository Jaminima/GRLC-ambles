@echo off
:main
garlicoin-cli getblockchaininfo
timeout 60
goto main