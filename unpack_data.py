"""Decompress every data/**/*.jsonl.gz next to itself and create analysis/work. Run once from the repository root."""
import gzip, shutil, pathlib
for gz in pathlib.Path('data').rglob('*.jsonl.gz'):
    out = gz.with_suffix('')
    if not out.exists():
        with gzip.open(gz, 'rb') as fi, open(out, 'wb') as fo:
            shutil.copyfileobj(fi, fo)
        print('unpacked', out)
pathlib.Path('analysis/work').mkdir(parents=True, exist_ok=True)
