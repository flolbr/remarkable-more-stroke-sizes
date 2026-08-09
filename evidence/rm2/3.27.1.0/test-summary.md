# 3.27.1.0 emulator test summary

Date: 2026-08-09
Target: reMarkable 2 firmware 3.27.1.0
Build ID: `20260506100933`
QMD SHA-256: `ad731ad0c846cf2fd7443754fa5947579583921b1028996d331d39b8694b3333`

## Result

- PASS: repository source/artifact/manifest structural validation.
- PASS: pinned rM-docker built the exact firmware after the documented,
  emulator-only SSH boot adaptation.
- PASS: exact-build QEMU guest reached SSH and reported the expected build ID.
- PASS: the guest read and SHA-256 checked the committed QMD.
- PASS: readable and generated QMD thickness values matched inside the guest.
- NOT TESTED: QMLDiff application to xochitl in the emulator.
- NOT TESTED: native UI display or interaction (`QEMU-UI`).

This is `CI-LOAD` evidence only. Physical `HW` evidence remains separately
documented in `evidence/3.27-test-summary.md` and is not inferred from QEMU.
