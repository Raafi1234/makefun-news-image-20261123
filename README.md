# The World in One Day — Monday, 23 November 2026

An entry for the make.fun competition `news-image-20261123`: one image
that sums up the world's news of Monday, 23 November 2026.

The front page (`entry.png`, 1024×1024) leads with Nvidia's board
reinstating Jensen Huang as chief executive — shares jumped 31.5% after
President Trump intervened, and the US blacklisted the firm Megaspeed
the same day. Around it: NATO's emergency session after Russian missiles
landed in Poland; the revelation that a US drone helped Mexico catch
"El Chapo Isidro"; the factory fire in Indonesia, its death toll
confirmed at 24; India's $1.62bn package for flood-hit Nepal; and the
death toll rising to 11 after a Russian drone strike on Dymer, Ukraine.

Every story is documented with sources in [NEWS.md](NEWS.md). All text on
the page is drawn programmatically by `compose.py` (Python + Pillow) over
six text-free editorial illustrations in `panels/`; the program
`main.ts` (Node 22, standard library only) simply copies the finished
`entry.png` to the output directory.

## Build

```sh
make compose   # rebuild entry.png from panels/ (deterministic)
make run       # build, then run main.ts exactly as the grader does
make check     # verify entry.png is 1024×1024, ≤ 1 MiB, and that
               # out/entry.png is byte-identical to entry.png
make clean     # remove out/
```

## Files

- `compose.py` — draws the newspaper front page from `panels/`
- `panels/` — six text-free illustrations, one per story
- `entry.png` — the finished front page (JPEG bytes in a `.png` name,
  as the competition rules allow)
- `main.ts` — the entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`)
- `NEWS.md` — the six stories with sources
- `LICENSE` — MIT
