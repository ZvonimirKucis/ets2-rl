from skimage.feature import match_template
import numpy as np 

def template_match(needle, haystack):
    result = match_template(haystack, needle)
    ij = np.unravel_index(np.argmax(result), result.shape)
    x, y = ij[1], ij[0]
    score = result[y, x]
    return x, y, score

def clip(value, max=1, min=-1):
    if value > max:
       value = max
    if value < min:
       value = min
    return value