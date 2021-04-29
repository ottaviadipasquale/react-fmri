import os

import numpy as np

__all__ = ['check_can_write_file', 'volume4d_to_matrix']


def check_can_write_file(fpath: str, force: bool = False,
                         verbose: bool = False):
    """
    Check if a file can be written.

    The function checks if the file already exists, the user has the permission
    to write it, overwriting can be forced and, if the file does not exist, if
    the parent directory exists and is writable.

    Args:
        fpath: str
            path of the file to be checked.
        force: bool
            True if the file can be overwritten, False otherwise.

    Raises:
        FileExistsError : if the file exists and can not be overwritten.
        PermissionError :  if the file esists and the user does not have the
            permission to write it.
        PermissionError : if the file does not exist, the parent directory
            exists and the user does not have the permission to write a file in
            it.
        FileNotFoundError : if file does not exist and the parent directory
            does not exist.
    """
    if verbose:
        print(fpath)

    if os.path.exists(fpath) and os.path.isfile(fpath):
        if os.access(fpath, os.W_OK):
            if force:
                return
            else:
                raise FileExistsError(f'Specify `--force` to overwrite '
                                      f'{fpath}')
        else:
            # Tests for this case seem to be platform-dependent, hence have
            # been removed from the testing suite.
            raise PermissionError(f'User does not have permission to write '
                                  f'{fpath}')
    else:
        d = os.path.dirname(os.path.abspath(fpath))
        if os.path.exists(d):
            if os.access(d, os.W_OK):
                return
            else:
                raise PermissionError(f'User does not have permission to '
                                      f'write file in directory {d}')
        else:
            raise FileNotFoundError(f'Directory does not exist: {d}')


def volume4d_to_matrix(v: np.ndarray):
    """
        For fMRI, where time is the 4th dimension, it gives a matrix with
        a row per voxel and a column per time point.
    """
    if not isinstance(v, np.ndarray):
        v = np.asarray(v)
    if v.ndim != 4:
        raise ValueError('The passed volume must be 4 dimensional.')
    return np.reshape(v, (np.prod(v.shape[:-1]), v.shape[-1]))
