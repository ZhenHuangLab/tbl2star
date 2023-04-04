import typer
from eulerangles import convert_eulers
import pandas as pd
import numpy as np
from ._tools import read_dynamo_tbl, get_tomo_name, save_dynamo_star

app = typer.Typer(add_completion=False)
@app.command(name='tbl2star')
def tbl2star_app(
    tiltseries_path: str = typer.Option(..., '-ts', '--tiltseries_path', prompt='Please enter your path to dictionary containing tiltseries/tomograms', help='Path to dictionary containing tiltseries/tomograms in RELION pattern'),
    dynamotable_path: str = typer.Option('.', '-tbl', '--dynamotable_path', prompt='Please enter your path to dictionary containing all dynamo tables.', help='Path to dictionary containing all of your dynamotables. Default is to use the current folder. All of these coordinates will be used, so please ensure that they correspond to the tomograms.'),
    binning: float = typer.Option(1, '-b', '--binning', prompt='Binning in DYNAMO table', help='Binning in DYNAMO table. Default is 1.'),
    pattern: str = typer.Option(None, '-p', '--pattern', prompt='Pattern to recognize tomogram names', help='Pattern to recognize tomogram names. Default is TS/ts. Explained in detail in README.md.'), 
    relionstarfile_name: str = typer.Option(None, '-s', '--relionstarfile_name', prompt='Please enter the name of relion star file', help='Name of relion star file. Default is "AllCoordinates.star". For example, you can input GCBcoordinates.star'),
    relionstarfile_path: str = typer.Option(None, '-sp', '--relionstarfile_path', prompt='Please enter the save path of relion star file', help='Path of relion star file. Default is the current folder. For example, you can input Path/to/your/save/dictionary')
):
    """
    A tool converting DYNAMO table files(.tbl) to RELION star files(.star).

    ======
    param:

    -------------------

    tiltseries_path: str

        Path to dictionary containing tiltseries/tomograms in RELION pattern. 
        
        For example, path/to/your/tomograms

    -------------------

    dynamotable_path: optional, str

        Path to dictionary containing all of your dynamotables. 
        
        Default is to use the current folder.

        All of these coordinates will be used, so please ensure that they correspond to the tomograms.

    -------------------

    binning: optional, str

        Binning in DYNAMO table. Default is 1.

    -------------------

    pattern: optional, str

        Pattern to recognize tomogram names. Default is TS/ts. Explained in detail in README.md.

        You can input a string so that the first set of numbers after the string is recognized and used as a criterion to distinguish the tomogram.
        
        For instance, if your tomogram folder names are 'Rubisco_30_A_001_XX', 'Rubisco_30_A_002_XX'..., you can set the pattern to A so the program can recognize them as 1,2,...
        
        Note that strings and numbers must be separated by "_".

    -------------------

    relionstarfile_name: optional, str
        
        Name of relion star file. Default is "AllCoordinates.star". 
        
        For example, you can input 'GCBcoordinates.star'.
        
        Do not forget the file suffix .star.

    -------------------

    relionstarfile_path: optional, str
        
        Path of relion star file. Default is the current folder. 
        
        For example, you can input 'Path/to/your/save/dictionary'.


    """
    # table = read_dynamo_tbl(folder_path='/Users/hzvictor/Desktop/Membrane_Associated_Picking-main')

    table = read_dynamo_tbl(folder_path=dynamotable_path)
    star_data = {}

    # _rlnTomoName #1

    tomo_num = table['tomo'].to_numpy()
    # star_data['rlnTomoName'] = get_tomo_name(ts_path='/Users/hzvictor/Desktop/Membrane_Associated_Picking-main/tomograms', tomo_num_arr=tomo_num, pattern=pattern)
    star_data['rlnTomoName'] = get_tomo_name(ts_path=tiltseries_path, tomo_num_arr=tomo_num, pattern=pattern)

    # _rlnTomoParticleId #2

    n_id = range(1, table.shape[0]+1)
    star_data['rlnTomoParticleId'] = n_id

    # _rlnTomoManifoldIndex #3

    star_data['rlnTomoManifoldIndex'] = table['reg']

    # _rlnCoordinateX #4 / _rlnCoordinateY #5 / _rlnCoordinateZ #6

    for axis in ('x', 'y', 'z'):
        head = f'rlnCoordinate{axis.upper()}'
        shift_axis = f'd{axis}'
        star_data[head] = (table[axis] + table[shift_axis]) * float(binning)

    # _rlnOriginXAngst #7 / _rlnOriginYAngst #8 / _rlnOriginZAngst #9

    for axis in ('X', 'Y', 'Z'):
        head = f'rlnOrigin{axis}Angst'
        star_data[head] = [0] * len(star_data['rlnTomoName'])

    # _rlnAngleRot #10 / _rlnAngleTilt #11 / _rlnAnglePsi #12

    eulers_dynamo = table[['tdrot', 'tilt', 'narot']].to_numpy()
    eulers_relion = convert_eulers(eulers_dynamo,
                                    source_meta='dynamo',
                                    target_meta='relion')
    star_data['rlnAngleRot'] = eulers_relion[:, 0]
    star_data['rlnAngleTilt'] = eulers_relion[:, 1]
    star_data['rlnAnglePsi'] = eulers_relion[:, 2]

    # _rlnClassNumber #13

    star_data['rlnClassNumber'] = [1] * len(star_data['rlnTomoName'])

    # _rlnRandomSubset #14

    star_data['rlnRandomSubset'] = np.random.choice([1, 2], size=len(star_data['rlnTomoName']), p=[0.5, 0.5])

    ######### SAVE THE STAR FILE ##########
    df = pd.DataFrame.from_dict(star_data)
    print(df)
    save_dynamo_star(dataframe=df, filename=relionstarfile_name, filepath=relionstarfile_path)
