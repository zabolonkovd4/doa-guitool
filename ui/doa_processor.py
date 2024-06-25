from enum import Enum
import doatools.model as model


class DoAMethod(str, Enum):
    MUSIC = 'MUSIC' 
    ROOT_MUSIC = 'ROOT_MUSIC'

    def __str__(self) -> str:
        return self.value


def set_array(size=8, wavelen=51.6, arr_type='ULA'):
    # Parameters
    d0 = wavelen / 2
    # Create an array
    arr = None
    if arr_type == 'ULA':
        arr = model.UniformLinearArray(size, d0)
    if arr_type == 'UCA':
        arr = model.UniformCircularArray(size, d0)
    return arr


