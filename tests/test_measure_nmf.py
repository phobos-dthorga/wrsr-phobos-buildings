"""Malformed independent fixtures must not become plausible comparison evidence."""
import struct
import tempfile
from pathlib import Path
import unittest
from scripts.measure_nmf import measure


def fixture(mask=1,indices=(0,1,2),subsets=((0,3,0,0),)):
    pack=lambda fmt,*v:struct.pack('<'+fmt,*v)
    identity=(1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.)
    name=lambda n:n.encode().ljust(64,b'\0')
    node=pack('2I',0,0)+name('one')+pack('hH',-1,0)+pack('32f',*identity,*identity)+pack('6f',0,0,0,1,1,0)
    node+=pack('I',1)+pack('7I',0,3,len(indices),len(subsets),0,mask,0)
    node+=pack(str(len(indices))+'H',*indices)+pack('9f',0,0,0,1,0,0,0,1,0)
    node+=b''.join(pack('2I2H',*s) for s in subsets)
    node=node[:4]+pack('I',len(node))+node[8:]
    return b'B3DMH\x0010'+pack('3I',1,1,20+64+len(node))+name('surface')+node


class MeasurementTests(unittest.TestCase):
    def read(self,data):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'fixture.nmf'
            path.write_bytes(data)
            return measure(path)

    def test_counts_and_dimensions(self):
        result=self.read(fixture())
        self.assertEqual(result['levels'][0]['triangles'],1)
        self.assertEqual(result['levels'][0]['dimensions_xyz_m'],[1.,1.,0.])

    def test_truncation_fails(self):
        with self.assertRaises(ValueError): self.read(fixture()[:-1])

    def test_out_of_range_index_fails(self):
        with self.assertRaisesRegex(ValueError,'vertex index'): self.read(fixture(indices=(0,1,9)))

    def test_unknown_vertex_attribute_fails(self):
        with self.assertRaisesRegex(ValueError,'vertex layout'): self.read(fixture(mask=1|(1<<12)))

    def test_overlapping_subsets_fail(self):
        with self.assertRaisesRegex(ValueError,'overlap'):
            self.read(fixture(indices=(0,1,2,0,1,2),subsets=((0,3,0,0),(0,3,0,0))))


if __name__=='__main__': unittest.main()
