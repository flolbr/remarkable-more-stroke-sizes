# 3.27.0.97 emulator test summary

Date: 2026-08-09
Target: reMarkable 2 firmware 3.27.0.97
Build ID: `20260428124824`
QMD SHA-256: `169968131f2eb76fbdd1e26e03ce9458b6a1542cd60d14c53e52ec823d6663e4`

## Result

- PASS: XOVI and qt-resource-rebuilder v17 enumerated the exact image's QML
  resources and QMLDiff wrote a firmware-specific hashtable.
- PASS: QMLDiff reported no compatibility errors for the 3.27 readable source.
- PASS: regeneration against the exact hashtable produced the same hashed QMD
  body as 3.27.1.0, with only the exact `VERSION` guard changed.
- PASS: repository source/artifact/manifest structural validation.
- PASS: pinned rM-docker built and booted the exact firmware after the
  documented emulator-only SSH adaptation.
- PASS: the QEMU guest reported the expected build ID, read and SHA-256
  checked the committed QMD, and matched its thickness values with the
  readable source.
- NOT TESTED: native UI display or interaction (`QEMU-UI`).
- NOT TESTED: physical reMarkable hardware (`HW`).

The headless hashtable build delayed the image's unavailable SWTCON hardware
initialization long enough for QMLDiff's normal saver thread to finish. That
private harness did not alter firmware resources or the project QMD. Firmware,
extracted QML, and the generated hashtable are not published.

This is exact-build `HASH` and `CI-LOAD` evidence only. It must not be used to
claim physical compatibility.
