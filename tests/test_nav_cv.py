"""
Test template for unit testing with pytest
"""

# import what you need from within the package
import pytest

from asv.cv import nav_cv


def test_find_red_green():
    """
    Test the find red & green function
    """
    cv = nav_cv.CV()
    result = cv.find_red_and_green("this is some data")

def test_cv_function():
    """
    Test a cv function withing the cv template file
    """

    # creates a cv template object to test the function
    cv = nav_cv.CV()
    result, img_viz = cv.run("this_is_some_data", None, None)
    assert isinstance(result, dict) and img_viz == "this_is_some_data" 