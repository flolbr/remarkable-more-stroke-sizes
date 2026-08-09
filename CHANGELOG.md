# Changelog

## 0.1.0 — 2026-08-08

- Extract the native thickness-menu behavior from rmHacks into a standalone QMD.
- Add exact-build artifacts for reMarkable OS 3.24.0.149 and 3.27.1.0 on reMarkable 2.
- Add the `translationContext()` model method required for labels on 3.27.1.0.
- Record physical menu, drawing, restart, reboot, removal, and reinstall tests.
- Add the locally validated Vellum package definition and package test summary.
- Add physically tested English, French, German, and Spanish labels with the
  numeric thickness appended and English fallback for other languages.
- Add manifest-driven source/artifact checks and exact-build rm2 QEMU
  CI-LOAD coverage, with canary-first GitHub Actions orchestration.
