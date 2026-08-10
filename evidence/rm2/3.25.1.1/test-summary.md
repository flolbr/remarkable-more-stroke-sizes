# 3.25.1.1 emulator test summary

Date: 2026-08-10
Target: reMarkable 2 firmware 3.25.1.1
Build ID: `20260210094933`
QMD SHA-256: `91a81071dec748ccb2ec8e2dea929683d1fabe8e224a0a74056c383f5cc54ab1`

## Result

- PASS: the unchanged 3.27.1.0 canary completed before candidate interpretation.
- PASS: XOVI and qt-resource-rebuilder v17 enumerated the exact image and
  QMLDiff wrote a private firmware-specific hashtable.
- PASS: QMLDiff reported no compatibility errors for the current localized
  readable source.
- PASS: the generated hashed body matches 3.27.1.0; only the exact `VERSION`
  guard differs.
- PASS: repository source/artifact/manifest structural validation.
- PASS: the exact-build QEMU guest reported the expected build ID, verified
  the artifact SHA-256, and matched its thicknesses with the readable source.
- NOT TESTED: native UI display or interaction (`QEMU-UI`).
- NOT TESTED: physical reMarkable hardware (`HW`).

The headless-only SWTCON delay allowed QMLDiff's saver thread to finish; it
did not modify firmware resources or the project QMD. Firmware, extracted QML,
and the generated hashtable are not published. This is exact-build `HASH` and
`CI-LOAD` evidence only.
