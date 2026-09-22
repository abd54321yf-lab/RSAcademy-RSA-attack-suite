import tempfile, unittest
from pathlib import Path
from rsa.entropy import shannon_entropy
from rsa.matcher import find_all
from rsa.signature import get_signatures
from rsa.pipeline import rsa_one, rsa_many

class CoreTests(unittest.TestCase):
    def test_entropy_bounds(self):
        self.assertEqual(shannon_entropy(b''),0.0); self.assertLess(shannon_entropy(b'aaaa'),1.0)
    def test_match_valid_jpeg(self):
        data=b'prefix'+b'\xff\xd8\xff'+b'payload'+b'\xff\xd9'; m=find_all(data,get_signatures(['jpg']))
        self.assertEqual(len(m),1); self.assertEqual(m[0].offset,6); self.assertFalse(m[0].truncated)
    def test_pipeline_reports(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'sample.bin'; source.write_bytes(b'X'*20+b'\x89PNG\r\n\x1a\n'+b'contentIEND\xaeB`\x82'+b'Y'*10)
            out=Path(d)/'out'; report=rsa_one(source,out)
            self.assertEqual(len(report['artifacts']),1); self.assertTrue((out/'report.json').exists()); self.assertTrue((out/'report.html').exists())
    def test_batch_continues_after_bad_file(self):
        with tempfile.TemporaryDirectory() as d:
            good=Path(d)/'good.bin'; good.write_bytes(b'%PDF-hello%%EOF')
            bad=Path(d)/'missing.bin'
            result=rsa_many([good,bad],Path(d)/'results')
            self.assertEqual(result['total_images_processed'],2); self.assertEqual(len(result['errors']),1)

if __name__=='__main__': unittest.main()
