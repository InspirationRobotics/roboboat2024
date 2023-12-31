"""
Test template for unit testing with pytest
"""

# import what you need from within the package
import pytest
import numpy as np

from asv.cv import nav_cv


def test_find_red_green_sanity():
    """
    Sanity check for find red & green function
    """
    cv = nav_cv.CV()
    
    # Create a mock frame (replace this with a more realistic frame)
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    # Call the function
    result_frame = cv.find_red_and_green(mock_frame)

    # Assert that the result is not None
    assert result_frame is not None

    # Assert that the result has the expected shape
    assert result_frame.shape == mock_frame.shape
