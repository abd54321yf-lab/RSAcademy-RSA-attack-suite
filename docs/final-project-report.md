# RSAcademy — Final Project Report

## Problem and motivation
Deleted, damaged, or embedded files may remain as byte ranges inside a disk image. RSAcademy demonstrates a transparent recovery pipeline based on Magic Bytes, bounded Header/Footer matching, structural checks, entropy, hashes, and forensic reporting.

## Architecture
The implementation separates input reading, backend selection, carving, validation, artifact modeling, forensic analysis, reporting, and CLI orchestration. The Pure Python backend is the reference path; YARA is an optional integration seam.

## Results
The project supports single-file carving, directory and recursive batch analysis, explicit file lists, JSON configuration, extracted artifacts, MD5/SHA-256, entropy labels, offset maps, JSON reports, self-contained HTML reports, ASCII summaries, and automated binary tests.

## Limitations
The current version does not claim 100% reconstruction of highly fragmented files, full filesystem parsing, advanced compressed container recovery, or a configured YARA ruleset. Very large images should use a future streaming matcher with chunk carry-over.

## Future work
Add streaming scanning, richer JPEG/PDF/ZIP validators, filesystem-aware slack-space analysis, SVG visualization, configurable YARA rules, TOML parsing, and parallel workers after correctness benchmarks.
