#!/usr/bin/env python3
"""
Cross-platform task runner for Cryptography Resources.

Works on Windows, Mac, and Linux without Make.

Usage:
    uv run python tasks.py <command>

Commands:
    help         Show this help message
    install      Install dependencies
    install-all  Install all dependencies including Solana
    quick        Generate seed (quick/petty cash mode)
    secure       Generate seed (secure/cold storage mode)
    mnemonic     Basic seed gen (no security features)
    eth          Generate Ethereum wallet
    btc          Generate Bitcoin keys
    solana       Generate Solana keys
    test         Run functionality tests
    test-entropy Run entropy validation suite
    clean        Remove cached files
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()
BIP39_DIR = PROJECT_ROOT / "BIP39"


def run_command(cmd: list[str], cwd: Path = PROJECT_ROOT) -> int:
    """Run a command and return the exit code."""
    try:
        result = subprocess.run(cmd, cwd=cwd)
        return result.returncode
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return 1


def show_help():
    """Show help message."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║       Cryptography Resources - Cross-Platform Tasks          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Usage: uv run python tasks.py <command>                     ║
║                                                              ║
║  Commands:                                                   ║
║    help         Show this help message                       ║
║    install      Install dependencies                         ║
║    install-all  Install all deps including Solana            ║
║                                                              ║
║  Seed Generation:                                            ║
║    quick        Secure seed gen (petty cash mode)            ║
║    secure       Secure seed gen (cold storage mode)          ║
║    mnemonic     Basic seed gen (no security features)        ║
║                                                              ║
║  Chain-Specific:                                             ║
║    eth          Generate Ethereum wallet                     ║
║    btc          Generate Bitcoin keys                        ║
║    solana       Generate Solana keys                         ║
║                                                              ║
║  Testing:                                                    ║
║    test         Run functionality tests                      ║
║    test-entropy Run entropy validation suite                 ║
║                                                              ║
║    clean        Remove cached files                          ║
║                                                              ║
║  Mac/Linux users can also use: make <command>                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def cmd_install():
    """Install dependencies."""
    return run_command(["uv", "sync"])


def cmd_install_all():
    """Install all dependencies including extras."""
    return run_command(["uv", "sync", "--all-extras"])


def cmd_quick():
    """Generate seed in quick mode."""
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "secure_mnemonic_generate.py"), "--quick"]
    )


def cmd_secure():
    """Generate seed in secure mode."""
    print("⚠️  TIP: For maximum security, disconnect from the internet first.")
    print("")
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "secure_mnemonic_generate.py"), "--secure"]
    )


def cmd_mnemonic():
    """Generate basic mnemonic (no security features)."""
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "mnemonic_generator.py")]
    )


def cmd_eth():
    """Generate Ethereum wallet."""
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "generate_eth.py")]
    )


def cmd_btc():
    """Generate Bitcoin keys."""
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "derive_bitcoin_keys.py")]
    )


def cmd_solana():
    """Generate Solana keys."""
    return run_command(
        ["uv", "run", "python", str(BIP39_DIR / "derive_solana_keys.py")]
    )


def cmd_test():
    """Run functionality tests."""
    return run_command(
        ["uv", "run", "python", str(PROJECT_ROOT / "tests" / "test_functionality.py")]
    )


def cmd_test_entropy():
    """Run entropy validation suite."""
    return run_command(
        ["uv", "run", "python", str(PROJECT_ROOT / "tests" / "test_entropy_validation.py")]
    )


def cmd_clean():
    """Remove cached files."""
    cleaned = 0
    
    # Remove __pycache__ directories
    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)
            cleaned += 1
    
    # Remove .pyc files
    for pyc in PROJECT_ROOT.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)
        cleaned += 1
    
    print(f"✅ Cleaned {cleaned} cached items")
    return 0


# Command mapping
COMMANDS = {
    "help": show_help,
    "install": cmd_install,
    "install-all": cmd_install_all,
    "quick": cmd_quick,
    "secure": cmd_secure,
    "mnemonic": cmd_mnemonic,
    "eth": cmd_eth,
    "btc": cmd_btc,
    "solana": cmd_solana,
    "test": cmd_test,
    "test-entropy": cmd_test_entropy,
    "clean": cmd_clean,
}


def main():
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1].lower().strip()
    
    if command in COMMANDS:
        result = COMMANDS[command]()
        return result if result is not None else 0
    else:
        print(f"❌ Unknown command: {command}")
        print("   Run 'uv run python tasks.py help' for available commands.")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)

