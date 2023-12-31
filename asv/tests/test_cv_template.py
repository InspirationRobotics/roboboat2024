"""
Test template for unit testing with pytest
"""

# import what you need from within the package
import pytest

from asv.cv import template_cv


def test_cv_function():
    """
    Test a cv function withing the cv template file
    """

    # creates a cv template object to test the function
    cv = template_cv.CV()
    result, img_viz = cv.run(frame="this_is_some_data", target=None, oakd_data=None)
    assert isinstance(result, dict) and img_viz == "this_is_some_data" 