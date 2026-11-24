# The World in One Day — Monday, 23 November 2026
# make.fun news-image-20261123 entry.

.PHONY: compose run check clean

# Rebuild the front page from the panels (deterministic: same bytes twice).
compose:
	python3 compose.py

# Build, then run the entry program exactly as the grader does.
run: compose
	mkdir -p out
	MAKEFUN_OUTPUT_DIR=out node main.ts

# Verify the output: right format, 1024x1024, under 1 MiB, and byte-identical
# to the image in the repository.
check: run
	python3 -c "from PIL import Image; import os; im = Image.open('entry.png'); assert im.size == (1024, 1024), im.size; assert os.path.getsize('entry.png') <= 1048576; print('entry.png OK:', im.format, im.size, os.path.getsize('entry.png'), 'bytes')"
	cmp out/entry.png entry.png && echo "out/entry.png identical to entry.png"

clean:
	rm -rf out
