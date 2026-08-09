# 3.24.0.149 emulator test summary

Date: 2026-08-09
Target: reMarkable 2 firmware 3.24.0.149
Build ID: `20251130114409`
QMD SHA-256: `f6df3250bae225a8b65dac5bf6be78e2d404b8025b3025fd98499ea10b068093`

## Result

- PASS: repository source/artifact/manifest structural validation.
- PASS: pinned rM-docker built the exact firmware after the documented,
  emulator-only SSH boot adaptation.
- PASS: exact-build QEMU guest reached SSH and reported the expected build ID.
- PASS: the guest read and SHA-256 checked the committed QMD.
- PASS: readable and generated QMD thickness values matched inside the guest.
- PASS: GitHub Actions run
  [`31304766640`](https://github.com/flolbr/remarkable-more-stroke-sizes/actions/runs/31304766640)
  completed this target after the 3.27 canary passed.
- NOT TESTED: QMLDiff application to xochitl in the emulator.
- NOT TESTED: native UI display or interaction (`QEMU-UI`).

This is `CI-LOAD` evidence only. Physical `HW` evidence remains separately
documented in `evidence/3.24-test-summary.md` and is not inferred from QEMU.
