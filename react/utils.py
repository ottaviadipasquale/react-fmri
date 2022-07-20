import logging
import os

import numpy as np

__all__ = ['check_can_write_file', 'normalize_3d_volume', 'volume4d_to_matrix']


def check_can_write_file(fpath: str, force: bool = False):
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
    logging.debug(fpath)

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


def normalize_3d_volume(v: np.ndarray) -> np.ndarray:
    """
    Normalize the positive values of a 3-dimensional numpy array.

    This function shifts the minimum value to zero and rescales the resulting
    values by the span between the minimum and maximum in the array.

    Note:
        The processing clips the values of the input image to the [0, +infty)
        interval.

    Args:
        v: np.ndarray
            three-dimensional array to be normalized

    Returns:
        the normalized version of the input three-dimensional np.ndarray.

    Raises:
        ValueError : if the input volume is not three-dimensional.
    """
    if v.ndim != 3:
        raise ValueError('Input data must be 3-dimensional')
    data = v.copy()
    zeromask = data <= 0
    data[zeromask] = 0.
    a = np.min(data[np.logical_not(zeromask)])
    b = np.max(data[np.logical_not(zeromask)])
    logging.info(f'Minimum: {a}')
    logging.info(f'Maximum: {b}')
    data = data - a  # shift
    data = data / (b - a)  # scale
    data[zeromask] = 0.
    return data


def volume4d_to_matrix(v: np.ndarray) -> np.ndarray:
    """
        This function transforms a 4-dimensional volume in a matrix whose
        columns are the vectorization of the 4th dimension of the input array.

        For fMRI data, where time is the 4th dimension, it gives a matrix with
        a row per voxel and a column per time point.

        Args:
            v: np.ndarray
                four-dimensional array to be transformed into a matrix.

        Returns:
            the matrix version of the input volume.

        Raises:
            ValueError : if the input volume is not 4-dimensional.
    """
    if v.ndim != 4:
        raise ValueError('The passed volume must be 4 dimensional.')
    return np.reshape(v, (np.prod(v.shape[:-1]), v.shape[-1]))
