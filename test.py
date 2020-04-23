import os, subprocess
import unittest
import liftOverCNV as L
import filecmp
# import CrossMap


class Tests(unittest.TestCase):
    def test_placeholder(self):
        pass
    
    # def test_cross_map_installed(self):
    #     result = L.checkCrossMapInstalled()
    #     self.assertTrue(result)

    # def test_bad_path_to_CNV_file(self):
    #     self.assertTrue(type(L.convertCNVtoBED('bad_path')), FileNotFoundError)

    # def test_bad_path_to_chain_file(self):
    #     self.assertTrue(type(L.convertCNVtoBED('bad_path')), FileNotFoundError)

    
    # def test_convert_to_bed(self):
    #     test_variant_file = 'test_files/CNVs_hg18_5Lines.txt'
    #     expected_intermediate_file = 'test_files/CNVs_hg18_5Lines.txt.temp.bed'
    #     reference_file =             'test_files/CNVs_hg18_5Lines.bed'

    #     L.convertCNVtoBED(test_variant_file)
        
    #     self.assertTrue(
    #         filecmp.cmp(expected_intermediate_file, reference_file, shallow=False)
    #     )

    #     os.remove('test_files/CNVs_hg18_5Lines.txt.temp.bed')

if __name__ == '__main__':
    unittest.main()