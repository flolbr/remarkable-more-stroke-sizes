# Vellum package test summary

Date: 2026-08-08
Hardware: reMarkable 2
Firmware: 3.27.1.0
Package: `more-stroke-sizes-0.1.0-r1.apk`
APK SHA-256: `499aa50f3a65c1ad3c9350ea7df1ed320d6fffd390415ba13643cb676b1c6ac6`
QMD SHA-256: `ad731ad0c846cf2fd7443754fa5947579583921b1028996d331d39b8694b3333`

## Build

- PASS: source URLs were pinned to project commit `fdfbce835da118575b36af9c797e6f807a58794e`.
- PASS: checksums were generated with Vellum's `update-checksums.sh`.
- PASS: Vellum validation and `apkbuild-lint` completed with zero failures or warnings.
- PASS: the official build script produced a signed noarch APK.
- PASS: the packaged QMD was byte-for-byte identical to the physically tested artifact.
- PASS: the package contained only the QMD, MIT license, and SOURCES attribution file.

## Device installation

- Used the current official Vellum v0.3.2 bootstrap; the installed CLI self-reported v0.3.1.
- Vellum installed XOVI 0.3.3-r2, xovi-extensions 19.0.0-r3, and qt-resource-rebuilder 19.0.0-r3 as package dependencies.
- A fresh 3.27.1.0 hashtable was rebuilt with qt-resource-rebuilder 19 and archived privately.
- PASS: the QMD applied without parser, selector, traversal, or rebuild errors.
- PASS: zero failed systemd units and no observed kernel OOM, panic, fatal, or segfault event.

## Physical tests

- PASS: all nine labelled entries appeared in the native thickness selector.
- PASS: Fineliner and Ballpoint could select and draw all sizes.
- PASS: 0.5 and 100 drew correctly, and returning to 1 / Thin worked.
- PASS: Pencil, Marker/Highlighter, Eraser, and Selection remained usable.
- PASS: page switching, notebook reopen, toolbar hide/show, and sleep/wake remained stable.
- PASS: package removal restored the stock three-entry selector.
- PASS: reinstall restored all nine entries and the drawing subset without freezing.
- PASS: Vellum-installed English and French localized-label subsets.
- PASS: standalone-QMD English, French, German, and Spanish localized-label
  subsets before packaging.

## Removal behavior

When no other Vellum package depended on XOVI, removing `more-stroke-sizes`
also removed the automatically installed XOVI and qt-resource-rebuilder
packages as orphan dependencies. Preserved inactive AppLoad and KOReader data
were not deleted. Reinstalling the local APK restored the framework packages
and extension successfully.
