# merge_maxquant

Script to merge Mix 1 and Mix 2 *proteinGroups.txt* files generated from MaxQuant and outputs a new *proteinGroups.txt*.
This should be only used for triple SILAC mass spec experiments.

## To install

Python 3 should already be installed on your computer.

Run the following command to download the script:

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
* -m1: proteinGroups.txt file for Mix 1
* -m2: proteinGroups.txt file for Mix 2

Optional:
* --prefix: prefix for output file name

