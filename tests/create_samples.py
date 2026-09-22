from pathlib import Path
root=Path(__file__).parents[1]/'samples'; root.mkdir(exist_ok=True)
(root/'mixed.bin').write_bytes(b'HEADER'+b'\xff\xd8\xff'+b'JPEG-SAMPLE'+b'\xff\xd9'+b'GAP'*4+b'%PDF-1.7\nDemo\n%%EOF'+b'TAIL')
(root/'truncated.bin').write_bytes(b'noise'+b'\x89PNG\r\n\x1a\n' + b'partial-png')
