# Current project state

Date examined: 2026-08-10
Commit examined: `fa48052`
Branch: `main`
Initial working tree: clean and synchronized with `origin/main`

## Canonical implementation

Readable QMD files under `src/<firmware>/` are the source of truth. Files
under `patches/<firmware>/` are generated with QMLDiff and the exact firmware
hashtable. Firmware QML, hashtables, and extracted resources are private test
inputs and are not stored in this repository.

There are currently two source families:

| Firmware | Thickness values | Labels | Generated QMD |
| --- | --- | --- | --- |
| 3.24.0.149 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8 | English, without numeric suffixes | `patches/3.24.0.149/more-stroke-sizes.qmd` |
| 3.25.1.1 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | English, French, German, and Spanish, with numeric suffixes; English fallback | `patches/3.25.1.1/more-stroke-sizes.qmd` |
| 3.26.0.68 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | English, French, German, and Spanish, with numeric suffixes; English fallback | `patches/3.26.0.68/more-stroke-sizes.qmd` |
| 3.27.0.97 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | English, French, German, and Spanish, with numeric suffixes; English fallback | `patches/3.27.0.97/more-stroke-sizes.qmd` |
| 3.27.1.0 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | English, French, German, and Spanish, with numeric suffixes; English fallback | `patches/3.27.1.0/more-stroke-sizes.qmd` |

The 3.27 source deliberately uses the stock translation of `Thin` as its
language marker. It keeps the project translation context separate to avoid a
second translation pass. Thickness 100 is intentionally absent on 3.24 after
a failed physical candidate and present in the 3.27 source family after a
complete physical pass on 3.27.1.0.

## Current evidence

| Firmware | HASH | CI-LOAD | QEMU-UI | HW |
| --- | --- | --- | --- | --- |
| 3.24.0.149 | passed | passed | not tested | passed |
| 3.25.1.1 | passed | passed | not tested | not tested |
| 3.26.0.68 | passed | passed | not tested | not tested |
| 3.27.0.97 | passed | passed | not tested | not tested |
| 3.27.1.0 | passed | passed | not tested | passed |

The strongest current canary is reMarkable 2 firmware `3.27.1.0`, whose
localized QMD and Vellum r1 package passed the full physical matrix.

## Tooling and repository state

- No compatibility manifest, project test scripts, or GitHub Actions workflow
  existed at reconnaissance.
- Current codexctl lists all three represented firmware versions for
  reMarkable 2, as well as 3.25 and 3.26.
- `Eeems-Org/run-in-remarkable-action` v1.2 pins rM-docker commit
  `4b6a612941cc29adc7ca23c1da38e641655d2ed2` and accepts an explicit firmware
  version.
- rM-docker supplies an ARM QEMU environment and an optional rm2fb display
  emulator. The GitHub action is appropriate for headless in-device commands;
  it does not by itself establish a QEMU-UI result.
- Current QMLDiff commit examined:
  `25681c3cc7addb93fdbb41ceac1f1bdce8b2625d`.
- Current rm-xovi-extensions commit examined:
  `7874154dba6793cc68a15fae0fb9dd272c4ed20a`.

## Known limitations and open questions

- Exact physical compatibility is claimed only for 3.24.0.149 and 3.27.1.0;
  emulator or CI results must not broaden hardware claims.
- The committed generated QMDs cannot be reproducibly regenerated in public
  CI without proprietary firmware resources and exact private hashtables.
- The public workflow uses a live headless QEMU guest; it does not apply the
  QMD to xochitl or exercise the native display.
- Other hardware, third-party-mod coexistence, and firmware versions not
  represented by exact artifacts remain out of scope until separately tested.

## Phase 14 result

Both manifest targets passed the same exact-build QEMU guest check. The 3.27
target passed first as the canary; only then was 3.24 enabled. In each guest,
the test verified `/etc/version`, copied and read the committed artifact,
checked its manifest SHA-256, and compared the generated thickness values with
those derived from the readable source.

Current rM-docker required a documented emulator-only adaptation for these
firmwares: shorter waits for absent emulated devices, a generic Dropbear
socket independent of USB/Wi-Fi/encrypted home, and an exact codexctl pin. The
adaptation is stored in `ci/rm-docker-3.27.patch` and does not modify firmware
or project QMDs. CI boots the resulting `qemu-debug` image as a normal
container rather than taking a first-boot snapshot inside BuildKit.

The 3.24 and 3.27 implementations remain separate source families. The two
3.27 builds share one readable implementation; their generated files differ
only by the exact `VERSION` guard because every QMD-relevant hash is identical.

GitHub Actions run
[`31304766640`](https://github.com/flolbr/remarkable-more-stroke-sizes/actions/runs/31304766640)
passed repository validation, the 3.27.1.0 canary, and then 3.24.0.149 at
commit `f4ff81505f22cf6689e7f63e3f8de896e4b8a36e`.

## 3.27.0.97 emulator expansion

The exact 3.27.0.97 image reported build ID `20260428124824`. XOVI and
qt-resource-rebuilder v17 generated its hashtable inside the emulator while a
headless-only preload delayed the unavailable SWTCON device initialization;
the proprietary hashtable and extracted resources remain private.

QMLDiff reported no compatibility errors for the existing 3.27 readable
source. Regenerating against the exact hashtable produced the same hashed QMD
body as 3.27.1.0 with only the required `VERSION 3.27.0.97` guard changed.
Repository validation and the exact-build QEMU guest check passed. This adds
`HASH` and `CI-LOAD` evidence only: `QEMU-UI` and physical hardware remain
untested, and the Vellum package remains constrained to physically validated
3.27.1.0.

GitHub Actions run
[`31308187236`](https://github.com/flolbr/remarkable-more-stroke-sizes/actions/runs/31308187236)
passed repository validation, the 3.27.1.0 canary, and then both remaining
targets in sequence, including exact-build 3.27.0.97, at implementation commit
`c2d3c65d1abfa0f978fe8d4481ecf4b933bd5892`.

## 3.25 and 3.26 emulator expansion

The pinned codexctl downloader selected exact rM2 builds `3.25.1.1`
(`20260210094933`) and `3.26.0.68` (`20260310084634`). The unchanged
3.27.1.0 canary passed before either candidate was interpreted.

XOVI and qt-resource-rebuilder v17 enumerated each exact image and wrote a
private firmware-specific hashtable. Both the 3.24 and localized 3.27 readable
sources hashed without compatibility errors; every QMD-relevant identifier is
identical across the five represented builds. The new artifacts use the
current localized source family and differ from 3.27.1.0 only in their exact
`VERSION` guards.

Both candidates passed repository validation and the exact-build live QEMU
guest check. This establishes `HASH` and `CI-LOAD` only. Native UI display and
physical hardware were not tested, and the Vellum package remains constrained
to physically validated 3.27.1.0.
