# More Stroke Sizes for reMarkable

A standalone [QMLDiff](https://github.com/asivery/qmldiff) extension that adds
more pen thicknesses directly to reMarkable's native thickness menu. It does
not require rmHacks or add a separate gesture, preset panel, or floating
toolbar.

## Compatibility

Only these exact reMarkable 2 firmware builds have been physically tested:

| Firmware | Thicknesses | Artifact |
| --- | --- | --- |
| 3.24.0.149 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8 | `patches/3.24.0.149/more-stroke-sizes.qmd` |
| 3.27.1.0 | 0.5, 1, 1.5, 2, 2.5, 3, 5, 8, 100 | `patches/3.27.1.0/more-stroke-sizes.qmd` |

The QMD files have exact `VERSION` guards. Support for other hardware or
firmware versions is not claimed.

## Requirements

- reMarkable 2 on one of the exact builds above
- [XOVI](https://github.com/asivery/rm-xovi-extensions)
- `qt-resource-rebuilder` v17 or newer compatible version
- A hashtable rebuilt on the installed firmware

XOVI is intentionally tethered. Start it explicitly after boot; do not add an
xochitl systemd preload or otherwise force XOVI to auto-start.

## Install

First rebuild the hashtable after every firmware update:

```sh
ssh -t rm2 'xovi/rebuild_hashtable'
```

Copy only the artifact matching the exact installed firmware:

```sh
scp patches/3.27.1.0/more-stroke-sizes.qmd \
  rm2:/home/root/xovi/exthome/qt-resource-rebuilder/more-stroke-sizes.qmd
ssh -t rm2 'xovi/debug'
```

Use `xovi/debug` first and return to stock immediately if QMLDiff reports an
error or xochitl becomes unstable. After validation, use the supported
`xovi/start` workflow when desired.

## Uninstall

Return to stock before removing the QMD:

```sh
ssh rm2 'xovi/stock'
ssh rm2 'rm -f /home/root/xovi/exthome/qt-resource-rebuilder/more-stroke-sizes.qmd'
```

Starting XOVI again without the file restores the stock three-entry thickness
menu.

## Testing

Both builds passed physical testing of the native menu with Fineliner and
Ballpoint, visible width changes, tool and page switching, notebook reopen,
sleep/wake, XOVI restart, stability/navigation checks, and clean removal.
The 3.27.1.0 build additionally passed a normal tablet reboot and reinstall
test. See [`evidence/`](evidence/) for the exact summaries.

Thickness `100` is intentionally absent from the 3.24 artifact after a
perceived UI hang and an `unhandled thickness 100` stock-journal warning. It
passed the full test matrix on 3.27.1.0.

AppLoad, KOReader, LAMY-button mappings, split-screen extensions, and other
third-party-mod coexistence are not claimed for the 3.27.1.0 artifact.

## Development

Readable sources live under `src/<firmware>/`. Hashed artifacts are generated
from those sources with the exact firmware-specific QMLDiff hashtable:

```sh
cp src/3.27.1.0/more-stroke-sizes-readable.qmd /tmp/more-stroke-sizes.qmd
qmldiff hash-diffs /path/to/hashtab-3.27.1.0 /tmp/more-stroke-sizes.qmd
```

`hash-diffs` modifies its input in place. Hashtable files are deliberately not
published here.

## Provenance and license

Derived from rmHacks' `more_stroke_sizes_hack.qmd` at upstream commit
`69f905c2747da6bfc6fa79f7c505d43d559acbf2`. See [ATTRIBUTION.md](ATTRIBUTION.md).
Distributed under the [MIT License](LICENSE), preserving the upstream notice.
