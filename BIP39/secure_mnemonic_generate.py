#!/usr/bin/env python3
"""
Secure Mnemonic Generator

Two modes:
  --quick    : For petty cash / hot wallets (basic protections)
  --secure   : For cold storage (maximum precautions, air-gapped recommended)

Security features:
  - No shell history (run with leading space to avoid history)
  - Screen clearing after display
  - Memory overwriting attempt
  - Timed display with auto-clear
  - Security checklist for serious seeds

Usage:
  uv run python secure_mnemonic_generate.py --quick
  uv run python secure_mnemonic_generate.py --secure
"""

import sys
import os
import time
import gc
import ctypes

from mnemonic import Mnemonic


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def secure_clear_string(s: str) -> None:
    """
    Attempt to overwrite string in memory.
    Note: Python strings are immutable, so this is best-effort.
    The GC and memory reuse make this imperfect, but better than nothing.
    """
    try:
        # Try to overwrite the string's buffer (CPython implementation detail)
        str_size = sys.getsizeof(s)
        # Create a mutable buffer and try to zero it
        if hasattr(ctypes, 'memset'):
            location = id(s)
            ctypes.memset(location, 0, str_size)
    except Exception:
        pass  # Best effort - may not work on all platforms
    finally:
        gc.collect()


def print_security_banner(mode: str):
    """Print security information banner."""
    if mode == "secure":
        print("\n" + "=" * 60)
        print("🔒 SECURE SEED GENERATION MODE")
        print("=" * 60)
        print("""
⚠️  SECURITY CHECKLIST - Confirm before proceeding:

    [ ] This machine is DISCONNECTED from the internet
    [ ] No screen sharing / remote access is active
    [ ] No one is watching your screen
    [ ] You have paper/metal ready to write the seed
    [ ] You will NOT photograph or digitally store this seed
    [ ] Terminal history is disabled (prefix command with space)
        """)
    else:
        print("\n" + "-" * 60)
        print("⚡ QUICK MODE - For petty cash / hot wallets only")
        print("-" * 60)


def countdown_display(mnemonic: str, display_seconds: int = 30):
    """
    Display mnemonic with countdown, then clear.
    """
    words = mnemonic.split()
    
    # Display in a readable grid format
    print("\n" + "=" * 60)
    print("📝 YOUR MNEMONIC SEED (write it down NOW)")
    print("=" * 60 + "\n")
    
    # Display as numbered grid (4 columns for 24 words, 3 for 12)
    cols = 4 if len(words) == 24 else 3
    for i, word in enumerate(words, 1):
        print(f"  {i:2}. {word:12}", end="")
        if i % cols == 0:
            print()
    
    if len(words) % cols != 0:
        print()
    
    print("\n" + "=" * 60)
    print(f"⏱️  Screen will clear in {display_seconds} seconds...")
    print("    Press Ctrl+C to clear immediately")
    print("=" * 60)
    
    try:
        for remaining in range(display_seconds, 0, -1):
            sys.stdout.write(f"\r    Clearing in {remaining:2} seconds... ")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # Clear screen
    clear_screen()
    print("\n✅ Screen cleared. Seed is no longer displayed.")
    print("   If you didn't write it down, generate a new one.\n")


def generate_secure_mnemonic(strength: int = 256) -> str:
    """Generate mnemonic using the standard library."""
    mnemo = Mnemonic('english')
    return mnemo.generate(strength=strength)


def quick_mode():
    """Quick generation for petty cash wallets."""
    print_security_banner("quick")
    
    response = input("\nGenerate 24-word (more secure) or 12-word seed? [24/12]: ").strip()
    strength = 128 if response == "12" else 256
    
    mnemonic = generate_secure_mnemonic(strength)
    countdown_display(mnemonic, display_seconds=60)
    
    # Attempt to clear from memory
    secure_clear_string(mnemonic)
    del mnemonic
    gc.collect()


def secure_mode():
    """Maximum security generation for cold storage."""
    print_security_banner("secure")
    
    response = input("\nHave you confirmed all items above? [yes/no]: ").strip().lower()
    if response not in ['yes', 'y']:
        print("\n❌ Aborting. Please ensure security checklist is complete.")
        print("   For petty cash, use: python secure_generate.py --quick\n")
        return
    
    # Check for network (basic check)
    print("\n🔍 Running basic security checks...")
    
    # Warn about potential issues
    if os.environ.get('SSH_CONNECTION') or os.environ.get('SSH_CLIENT'):
        print("\n⚠️  WARNING: SSH session detected!")
        print("   Seed generation over SSH is NOT recommended.")
        response = input("   Continue anyway? [yes/no]: ").strip().lower()
        if response not in ['yes', 'y']:
            return
    
    if os.environ.get('DISPLAY') and os.environ.get('SSH_CONNECTION'):
        print("\n⚠️  WARNING: X11 forwarding may be active!")
    
    print("\n✅ Generating seed with 256-bit entropy (24 words)...")
    print("   This is the maximum security level.\n")
    
    mnemonic = generate_secure_mnemonic(256)
    
    # Shorter display time for secure mode - encourages writing quickly
    countdown_display(mnemonic, display_seconds=45)
    
    # Aggressive cleanup
    secure_clear_string(mnemonic)
    del mnemonic
    gc.collect()
    
    print("🔒 Memory cleanup attempted.")
    print("   For maximum security, close this terminal session now.\n")


def show_help():
    """Show usage information."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║            SECURE MNEMONIC GENERATOR                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Usage:                                                      ║
║    uv run python secure_mnemonic_generate.py --quick         ║
║    uv run python secure_mnemonic_generate.py --secure        ║
║    uv run python secure_mnemonic_generate.py --help          ║
║                                                              ║
║  Or use the task runner:                                     ║
║    make quick / make secure       (Mac/Linux)                ║
║    uv run python tasks.py quick   (Cross-platform)           ║
║                                                              ║
║  Pro Tips:                                                   ║
║    • Prefix with space to avoid shell history                ║
║    • For cold storage, use an air-gapped machine             ║
║    • Never photograph or digitally store your seed           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    mode = sys.argv[1].lower().strip('-')
    
    if mode == 'help':
        show_help()
    elif mode == 'quick':
        quick_mode()
    elif mode == 'secure':
        secure_mode()
    else:
        print(f"Unknown mode: {sys.argv[1]}")
        show_help()


if __name__ == "__main__":
    main()

