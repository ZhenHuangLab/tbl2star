# tbl2star


[![PyPI version](https://badge.fury.io/py/tbl2star.svg)](https://pypi.org/project/tbl2star/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/tbl2star.svg)](https://pypi.org/project/tbl2star/)


A tool converting DYNAMO table files(.tbl) to RELION star files(.star)



Can be used together with [Membrane_Associated_Picking](https://github.com/EuanPyle/Membrane_Associated_Picking) by [EuanPyle](https://github.com/EuanPyle), which helps to pick membrane associated particles in cryo-ET.



Based on [dynamotable](https://github.com/teamtomo/dynamotable), [starfile](https://github.com/teamtomo/starfile), [eulerangles](https://github.com/alisterburt/eulerangles) by [alisterburt](https://github.com/alisterburt).



## Features



- Convert one or more dynamo tables to one relion star file
- Transfer all particle information including position, angle, related object and tomogram and so on
- Strictly follow the relion format for coordinates importing
- Recognize the personalized naming pattern of tomograms flexibly and precisely



## Installation



You can install this package by:

```
pip install tbl2star
```



## Usage



You can refer to the instructions via:

```
tbl2star --help
```



### Preparation

The dictionary containing tilt series and dynamo tables must look like this:

```
.
├── tomograms
│   └──***[pattern]_[number1]***
│      └──***[pattern]_[number1]***.st
│      └──etc...
│   └──***[pattern]_[number2]***
│      └──***[pattern]_[number2]***.st
│      └──etc...
│   └──***[pattern]_[number3]***
│      └──***[pattern]_[number3]***.st
│      └──etc...
│   └──etc...
├── dynamotables
│   └──***.tbl
│   └──etc...
```

Pay attention to the following points:

1. The file dictionary for storing tilt series is consistent with the rules of RELION software.
2. Tomogram is distinguished by numbers in DYNAMO tables, so please ensure that the number1, number2, number3, etc. in this naming pattern are different.
3. This tool will determine the number corresponding to each tomogram based on a specific pattern defined by you, and will look up the coordinates information for each tomogram in the DYNAMO tables based on this number. Therefore, please strictly follow the naming conventions mentioned above. `***` represents any symbol, and you can input your customized pattern `[pattern]`, so that the tool can read the subsequent number `[number]`.
4. You also need to place the `.tbl` file that stores all coordinates information in the same folder. After specifying the target directory, this tool will read all `.tbl` files in the directory, so please pay attention to the correspondence with tomograms, especially the numbers corresponding to the tomogram names.



### Parameters

- `tiltseries_path`: `-ts`. Path to dictionary containing tiltseries/tomograms in RELION pattern. For example, `path/to/your/tomograms`.
- `dynamotable_path`: `-tbl`. Path to dictionary containing all of your dynamotables. Default is to use the current folder. All of these coordinates will be used, so please ensure that they correspond to the tomograms.
- `binning`: `-b`. Binning in DYNAMO table. Default is 1.
- `pattern`: `-p`. Pattern to recognize tomogram names. Default is `TS/ts`.You can input a string so that the first set of numbers after the string is recognized and used as a criterion to distinguish the tomogram. For instance, if your tomogram folder names are `Rubisco_30_A_001_XX`, `Rubisco_30_A_002_XX`..., you can set the pattern to A so the program can recognize them as 1,2,...Note that strings and numbers must be separated by `_`.
- `relionstarfile_name`: `-s`. Name of relion star file. Default is `AllCoordinates.star`. For example, you can input `GCBcoordinates.star`. Do not forget the file suffix `.star`.
- `relionstarfile_path`: `-sp`. Path of relion star file. Default is the current folder. For example, `Path/to/your/save/dictionary`.




### Example

You can just simply using:

```
tbl2star
```

```
Please enter your path to dictionary containing tiltseries/tomograms: /Users/hzvictor/tomograms
Please enter your path to dictionary containing all dynamo tables. [.]: /Users/hzvictor
Binning in DYNAMO table [1]: 6
Pattern to recognize tomogram names: ts
Please enter the name of relion star file: Allcoordinates.star
Please enter the save path of relion star file: /Users/hzvictor/test
/Users/hzvictor/GCB_004_object_1.tbl has been read
/Users/hzvictor/GCB_003_object_2.tbl has been read
     rlnTomoName  rlnTomoParticleId  rlnTomoManifoldIndex  ...  rlnAnglePsi  rlnClassNumber  rlnRandomSubset
0     GCB_ts_003                  1                     2  ...     -135.000               1                1
1     GCB_ts_003                  2                     2  ...      153.435               1                1
2     GCB_ts_003                  3                     2  ...      135.000               1                2
3     GCB_ts_003                  4                     2  ...      141.340               1                2
4     GCB_ts_003                  5                     2  ...      -90.000               1                2
...          ...                ...                   ...  ...          ...             ...              ...
5826  GCB_ts_004              11658                     1  ...      168.690               1                1
5827  GCB_ts_004              11659                     1  ...       45.000               1                1
5828  GCB_ts_004              11660                     1  ...        0.000               1                1
5829  GCB_ts_004              11661                     1  ...      161.570               1                2
5830  GCB_ts_004              11662                     1  ...      -26.565               1                2

[11662 rows x 14 columns]
Saving relion .star file Allcoordinates.star to /Users/hzvictor/test/ ...
```

Or you can input:

```
tbl2star -ts /Users/hzvictor/tomograms -tbl /Users/hzvictor -b 6 -p ts -s Allcoordinates.star -sp /Users/hzvictor/test
```



## License

The project is released under the BSD 3-Clause License


