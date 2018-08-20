from pathlib import Path
# import os
import zipfile


try:
    import zlib
    cp = zipfile.ZIP_DEFLATED
    # compresslevel = 9 - being introduced in 3.7
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


def _generate_filelist(_dir):
    i = Path(_dir)  # ensure a Path-object
    # return [path for path in i.rglob('*.*') if i.is_file]
    return [path for path in i.rglob('*.*')]

    # NOTE: Maybe os.walk is faster...
    # for root, folders, files in os.walk(path):
    #     for filestring in files:
    #         out.append(os.path.join(root, filestring))
    # return out


def decompress(path, target=None, overwrite=False):
    in_path = Path(path)
    invalid = _invalid_zipfile(in_path)
    if not invalid:

        zip = zipfile.ZipFile(in_path)
        tg = Path(target) if target else in_path.with_name(in_path.stem)
        zip.extractall(tg)
        zip.close()


def compress(path, target=None, name=None, overwrite=False):
    '''
    Takes a string or Path-object representing a file or directory
    Compresses into zipfile in target_dir or same directory as path
    Gives it target_name if set or original name with 'zip'-extension.
    '''
    try:
        in_path = Path(path)  # ensure a Path-object
    except Exception as e:
        raise e
    
    # If no target_dir is set, choose parent-directory of the in_path,
    # whether current in_path is a file or a directory.
    out_dir = Path(target) if target else Path.joinpath(*in_path.parts[:-1])
    
    # If no name is set, use the path.stem, whether file or directory.
    fn = name if name else in_path.with_name(in_path.stem + '.zip')

    # If overwrite and save-path exists, save as _copy    
    if (not overwrite) and Path(out_dir, fn).exists():
        fn = fn.rsplit('.zip', 1)[0] + '_copy.zip'

    # Construct a list of Paths to iterate, whether file or directory.
    pathlist = [in_path] if in_path.is_file else _generate_filelist(in_path)

    with zipfile.ZipFile(out_dir / fn, mode='w', compression=cp) as arc:
        for path in pathlist:
            if in_path.is_file:
                arc.write(path)
            else:
                arc.write(path.relative_to(in_path))
                # archive.write(path, os.path.relpath(path, path.parents))

