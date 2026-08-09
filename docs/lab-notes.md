# Emulator and CI lab notes

This log records sanitized engineering outcomes. It intentionally excludes
firmware contents, extracted proprietary QML, hashtables, credentials, tablet
addresses, and private device logs.

## 2026-08-09 — Phase 14 reconnaissance

Firmware canary: reMarkable 2 `3.27.1.0`
Repository commit: `fd573ae0771d42d6074e922bd952aa702ad6a3d6`

Action:

- Reconciled the complete current repository before making changes.
- Established a persistent `rmstroke` tmux session.
- Inspected the current codexctl firmware list and upstream emulator, CI,
  XOVI, and QMLDiff implementations.

Result:

- The repository has two readable source families and exact generated
  artifacts for 3.24.0.149 and 3.27.1.0.
- No compatibility manifest, automated tests, or workflow existed.
- 3.27.1.0 is the strongest known-working canary based on physical evidence.

Next:

- Add tests derived from the readable QMD sources, then prove the canary in
  the current headless emulator/CI harness before expanding the matrix.

## 2026-08-09 — 3.27.1.0 headless canary

Firmware: reMarkable 2 `3.27.1.0`
Build ID: `20260506100933`
Emulator: rM-docker `4b6a612941cc29adc7ca23c1da38e641655d2ed2`

Action:

- Added a compatibility manifest and checks that derive thickness expectations
  from the readable QMD source.
- Built the pinned rM-docker headless target and captured its first boot.

Observation:

- Unmodified rM-docker booted the current firmware but could not reach SSH:
  systemd waited for absent USB/Wi-Fi devices, while all vendor Dropbear
  sockets were bound to those devices and encrypted `home.mount` introduced a
  circular dependency for the harness.
- Added a scoped rM-docker patch that shortens absent-device waits and creates
  a separate emulator-only Dropbear socket. No firmware or project QMD source
  was modified.

Result:

- PASS: clean canary image reached SSH and completed rM-docker's first-boot
  snapshot.
- PASS: the guest reported the exact expected build ID.
- PASS: the byte-exact QMD was copied into the guest, read, SHA-256 checked,
  and compared with its source-derived thickness list.
- QEMU-UI remains untested; this result is CI-LOAD only.

Next:

- Run the same guest check for the manifest's remaining 3.24.0.149 target.

## 2026-08-09 — 3.24.0.149 matrix target

Firmware: reMarkable 2 `3.24.0.149`
Build ID: `20251130114409`

Result:

- PASS: pinned clean QEMU image reached SSH and completed its first-boot
  snapshot after the 3.27 canary passed.
- PASS: exact guest build ID, artifact SHA-256, QMD versions, and
  source-derived thickness values.
- QEMU-UI remains untested; this result is CI-LOAD only.

Interpretation:

- Both currently represented firmware targets work in the headless guest
  harness.
- The two versions remain separate source families. The 3.27 translation
  context, localization tables, numeric labels, and thickness 100 are
  substantive source differences, not hash-only changes.
