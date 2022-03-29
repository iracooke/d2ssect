import unittest
import tempfile
import filecmp
import os, shutil
import d2ssect.jellyfish as jellyfish

## import other functions to be tested

class TestJellyfish(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def test_jfcount(self):
        inputf="data/fasta/DI-1-1_S6.fasta"
        outputf=tempfile.mkstemp()[1]

        os.system("cat "+outputf)
        jellyfish.count(inputf,outputf)

        expected_output="data/jf/DI-1-1_S6.jf"

        # Note files are compared on size 
        # only as jellyfish will not produce identical files from separate runs
        self.assertTrue(os.path.getsize(outputf),os.path.getsize(expected_output))

  
    def test_jfdump(self):
        inputf = "data/jf/DI-1-1_S6.jf"
        outputf = os.path.join(self.test_dir, "DI-1-1_S6.nkz")
        
        jellyfish.dump(inputf, outputf)
        print(outputf)
        expected_output = "data/nkz/DI-1-1_S6.nkz"

        self.assertTrue(filecmp.cmp(outputf, expected_output))

    def test_charfreq(self):
        inputf = "data/fasta/DI-1-1_S6.fasta"
        outputf = os.path.join(self.test_dir, "DI-1-1_S6.CharFreq")

        os.system(f"python v0/Composition_of_InputSeqs_py3.py --fasta {inputf} --freq {outputf}")
        expected_output = "data/charfreq/DI-1-1_S6.CharFreq"

        self.assertTrue(filecmp.cmp(outputf, expected_output))

    def test_d2s_cal(self):
        sample1 = "DI-1-1_S6"
        sample2 = "FI-2-21_S28"
        outputf = os.path.join(self.test_dir, "DI-1-1_S6_FI-2-21_S28.txt")

        os.system(f"python v0/Calculate_D2S_py3.py --kmerset1 data/nkz/{sample1}.nkz --kmerset1_freq data/charfreq/{sample1}.CharFreq \
            --kmerset2 data/nkz/{sample2}.nkz --kmerset2_freq data/charfreq/{sample2}.CharFreq --D2S_out {outputf}")
        expected_output = "data/d2s/DI-1-1_S6-FI-2-21_S28.txt"

        self.assertTrue(filecmp.cmp(outputf,expected_output))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()
