# Current project state

Date examined: 2026-08-09
Commit examined: `fd573ae0771d42d6074e922bd952aa702ad6a3d6`
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
| 3.27.1.0 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | English, French, German, and Spanish, with numeric suffixes; English fallback | `patches/3.27.1.0/more-stroke-sizes.qmd` |

The 3.27 source deliberately uses the stock translation of `Thin` as its
language marker. It keeps the project translation context separate to avoid a
second translation pass. Thickness 100 is intentionally absent on 3.24 after
a failed physical candidate and present on 3.27 after a complete physical
pass.

## Evidence at reconnaissance

| Firmware | HASH | CI-LOAD | QEMU-UI | HW |
| --- | --- | --- | --- | --- |
| 3.24.0.149 | passed | passed | not tested | passed |
| 3.27.1.0 | passed | passed | not tested | passed |

The strongest current canary is reMarkable 2 firmware `3.27.1.0`, whose
localized QMD and Vellum r1 package passed the full physical matrix.

## Tooling and repository state

- No compatibility manifest, project test scripts, or GitHub Actions workflow
  existed at reconnaissance.
- Current codexctl lists both represented firmware versions for reMarkable 2,
  as well as 3.25, 3.26, and the alternate 3.27.0.97 build.
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

- Exact physical compatibility is claimed only for the two represented
  builds; emulator or CI results must not broaden hardware claims.
- The committed generated QMDs cannot be reproducibly regenerated in public
  CI without proprietary firmware resources and exact private hashtables.
- It remains to prove the 3.27 canary in the current emulator harness before
  interpreting results from additional firmware.
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
or project QMDs.

No source family was collapsed: 3.27 still requires substantive source changes
for its translation context, localization tables, numeric labels, and tested
thickness 100 behavior. No represented version differs only by hashes.
