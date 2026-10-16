"""Regressions for cache-versioned CSS and its cascade order (no network)."""
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'performance'))
from optimize_site import local_file, optimize_site


class VersionedStylesheets(unittest.TestCase):
    def test_versioned_middle_layer_stays_in_cascade_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site/'assets').mkdir()
            (site/'zh').mkdir()
            (site/'build-manifest.json').write_text('{}')
            originals = {'base.css':'h1{color:red}', 'fullsite.css':'h1{color:blue}',
                         'readiness.css':'h1{color:green}'}
            for name, text in originals.items():
                (site/'assets'/name).write_text(text)
            page = site/'zh/index.html'
            page.write_text('<html><head>'+''.join(
                f'<link rel="stylesheet" href="../assets/{name}">'
                for name in ['base.css','fullsite.css?v=home-art-15','readiness.css'])+
                '</head><body><h1>Same content</h1></body></html>')
            report = optimize_site(site)
            css = [(name, data) for name, data in report['bundles'].items() if data['type']=='css']
            self.assertEqual(len(css), 1)
            name, detail = css[0]
            self.assertEqual(detail['inputs'], list(originals))
            bundled = (site/'assets'/name).read_text()
            self.assertLess(bundled.index('color:red'), bundled.index('color:blue'))
            self.assertLess(bundled.index('color:blue'), bundled.index('color:green'))
            self.assertEqual(page.read_text().count('rel="stylesheet"'), 1)
            for name, text in originals.items():
                self.assertEqual((site/'assets'/name).read_text(), text)

    def test_only_local_static_version_queries_are_eligible(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site/'assets').mkdir()
            file = site/'assets/theme.css'
            file.write_text('h1{}')
            page = site/'zh/index.html'
            self.assertEqual(local_file(site,page,'../assets/theme.css?v=1'),file)
            self.assertIsNone(local_file(site,page,'../assets/theme.css?transform=dark'))
            self.assertIsNone(local_file(site,page,'https://example.com/assets/theme.css?v=1'))
            self.assertIsNone(local_file(site,page,'../assets/../../outside.css?v=1'))


if __name__ == '__main__':
    unittest.main()
