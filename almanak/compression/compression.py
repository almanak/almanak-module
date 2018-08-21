from pathlib import Path
import zipfile
import os


try:
    import zlib
    cp = zipfile.ZIP_DEFLATED
    # compresslevel = 0-9 - being introduced in 3.7
except:
    cp = zipfile.ZIP_STORED
    # compresslevel = None - being introduced in 3.7


def _invalid_zipfile(filepath):
    '''
    Checks both the zip-container and the files within.
    Returns None if valid, else some error-string
    '''
    if Path(filepath).exists():
        # Test if the filepath points to a .zip-file with a valid container
        try:
            zfile = zipfile.ZipFile(filepath, 'r')
        except zipfile.BadZipfile:
            return "%s not a valid zip-container" % filepath

        # Test the content of each file in the zip-archive
        return zfile.testzip()
    else:
        return "%s not a valid filepath" % filepath


def decompress(path, target=None, overwrite: bool = False) -> str:
    in_path = Path(path)
    invalid = _invalid_zipfile(in_path)
    if not invalid:

        zip = zipfile.ZipFile(in_path)
        tg = Path(target) if target else in_path.with_name(in_path.stem)
        zip.extractall(tg)
        zip.close()
    else:
        return 
    return 

def compress(path, target=None, name: str = None, overwrite: bool = False) -> str:
    '''
    Takes a string or Path-object representing a file or directory
    Compresses into zipfile in target_dir or same directory as path
    Gives it target_name if set or original name with 'zip'-extension.
    '''
    try:
        # ensure Path-objects
        in_path = Path(path)
        out_dir = Path(target) if target else in_path.parent
    except Exception as e:
        raise e
    
    # Determine filename
    if name:
        out_name = name if name.endswith('.zip') else name + '.zip'
    else:
        out_name = in_path.stem + '.zip'

    if (not overwrite) and Path(out_dir, out_name).exists():
        out_name = out_name.rsplit('.zip', 1)[0] + '_copy.zip'

    out_path = out_dir / out_name

    try:
        with zipfile.ZipFile(out_path, mode='w', compression=cp) as arc:
            if in_path.is_file():
                arc.write(in_path, in_path.relative_to(in_path.parent))
            else:
                for path in in_path.rglob('*.*'):
                    arc.write(path, path.relative_to(in_path))
                    # arc.write(path, os.path.relpath(path, path.parents))
        return str(out_path)
    except Exception as e:
        raise e
