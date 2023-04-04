# tbl2star



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



