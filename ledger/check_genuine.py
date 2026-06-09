#!/usr/bin/env python3
"""Run Ledger's genuineness attestation against a connected device.

Wraps `python -m ledgerblue.checkGenuineRemote` with the correct --targetId
for the selected model. The attestation proves the Secure Element was
provisioned by Ledger; a counterfeit SE cannot produce the signature.
"""
import argparse
import subprocess
import sys

TARGET_IDS = {
    "nano-s":      "0x31100004",
    "nano-s-plus": "0x33100004",
    "nano-x":      "0x33000004",
    "stax":        "0x33200004",
    "flex":        "0x33300004",
}

PREFLIGHT = """\
Before continuing:
  1. Quit Ledger Live (it holds the USB HID interface).
  2. Connect the device via USB and unlock it with your PIN.
  3. Leave it on the dashboard — do not open an app.
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--device",
        choices=sorted(TARGET_IDS),
        default="nano-s-plus",
        help="Ledger device model (default: nano-s-plus)",
    )
    p.add_argument(
        "--apdu",
        action="store_true",
        help="Print APDU log (useful for debugging a failed check)",
    )
    p.add_argument(
        "--local",
        action="store_true",
        help="Use local-only attestation (ledgerblue.checkGenuine) instead of "
             "the remote HSM check. Note: default issuer key is 'batch 1' and "
             "will fail on newer devices unless --issuerKey is provided upstream.",
    )
    args = p.parse_args()

    target_id = TARGET_IDS[args.device]
    print(PREFLIGHT)
    module = "ledgerblue.checkGenuine" if args.local else "ledgerblue.checkGenuineRemote"
    print(f"Running {module} for {args.device} (targetId={target_id})...\n")

    cmd = [sys.executable, "-m", module, "--targetId", target_id]
    if args.apdu:
        cmd.append("--apdu")
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError:
        print(
            "ERROR: ledgerblue not installed. Run: uv sync --extra ledger",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
