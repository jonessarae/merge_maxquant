# merge_maxquant

Purpose: Merges Mix 1 and Mix 2 proteinGroups.txt files generated from MaxQuant.

To use:
python merge_maxquant.py -m1 <path/to/file> -m2 <path/to/file> --prefix <string>
Example:
python merge_maxquant.py -m1 LM1C/proteinGroups.txt -m2 LM2C/proteinGroups.txt --prefix Mix12_Con

Paramters:
Required:
-m1: proteinGroups.txt file for Mix 1
-m2: proteinGroups.txt file for Mix 2
Optional:
--prefix: prefix for output file name
"""

## To install

<pre>
git clone https://github.com/jonessarae/merge_maxquant.git
</pre>

## To use
<pre>
python merge_maxquant.py -m1 <path/to/file> -m2 <path/to/file> --prefix <string>
</pre>

Example:
<pre>
python merge_maxquant.py -m1 LM1C/proteinGroups.txt -m2 LM2C/proteinGroups.txt --prefix Mix12_Con
</pre>

Parameters:
Required:
-m1: proteinGroups.txt file for Mix 1
-m2: proteinGroups.txt file for Mix 2
Optional:
--prefix: prefix for output file name

