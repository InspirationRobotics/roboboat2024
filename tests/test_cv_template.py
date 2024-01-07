"""
Test template for unit testing with pytest
"""

# import what you need from within the package
import pytest

import numpy as np

from asv.cv import template_cv


def test_cv_function():
    """
    Test a cv function withing the cv template file
    """

    # creates a cv template object to test the function
    cv = template_cv.CV()
    result, img_viz = cv.run(np.float32(5.1), None, None)
    assert isinstance(result, dict) and img_viz == np.float32(5.1)
