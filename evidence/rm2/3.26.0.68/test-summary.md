# 3.26.0.68 emulator test summary

Date: 2026-08-10
Target: reMarkable 2 firmware 3.26.0.68
Build ID: `20260310084634`
QMD SHA-256: `428137c7fc5eb44d09f576b7289c2eb31a6bf07665eac2fbe09586d466417617`

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
