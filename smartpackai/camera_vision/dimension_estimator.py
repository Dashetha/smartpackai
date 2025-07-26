# camera_vision/dimension_estimator.py
import cv2
import numpy as np
from typing import Tuple, Optional

class DimensionEstimator:
    def __init__(self, reference_length: float, reference_width: float):
        """
        Initialize with known reference object dimensions (in cm)
        Args:
            reference_length: Real-world length of reference object
            reference_width: Real-world width of reference object
        """
        self.reference_length = reference_length
        self.reference_width = reference_width
        self.focal_length = None
        
    def calculate_focal_length(self, 
                             reference_pixel_length: float, 
                             reference_pixel_width: float,
                             distance_to_reference: float) -> float:
        """
        Calculate focal length using reference object
        Args:
            reference_pixel_length: Length in pixels
            reference_pixel_width: Width in pixels
            distance_to_reference: Distance from camera to object (cm)
        Returns:
            Calculated focal length
        """
        focal_length_length = (reference_pixel_length * distance_to_reference) / self.reference_length
        focal_length_width = (reference_pixel_width * distance_to_reference) / self.reference_width
        self.focal_length = (focal_length_length + focal_length_width) / 2
        return self.focal_length
        
    def estimate_dimensions(self, 
                          object_pixel_length: float,
                          object_pixel_width: float,
                          object_pixel_height: float,
                          distance_to_object: float) -> Tuple[float, float, float]:
        """
        Estimate real-world dimensions using focal length
        Args:
            object_pixel_length: Detected length in pixels
            object_pixel_width: Detected width in pixels
            object_pixel_height: Detected height in pixels
            distance_to_object: Distance from camera to object (cm)
        Returns:
            Tuple of (length, width, height) in cm
        """
        if self.focal_length is None:
            raise ValueError("Focal length not calculated. Call calculate_focal_length() first.")
            
        length_cm = (object_pixel_length * distance_to_object) / self.focal_length
        width_cm = (object_pixel_width * distance_to_object) / self.focal_length
        height_cm = (object_pixel_height * distance_to_object) / self.focal_length
        
        return round(length_cm, 2), round(width_cm, 2), round(height_cm, 2)
        
    def estimate_distance(self,
                        object_pixel_length: float,
                        known_object_length: float) -> float:
        """
        Estimate distance to object using known dimension
        Args:
            object_pixel_length: Detected length in pixels
            known_object_length: Real-world length of object (cm)
        Returns:
            Distance in cm
        """
        if self.focal_length is None:
            raise ValueError("Focal length not calculated. Call calculate_focal_length() first.")
            
        return (known_object_length * self.focal_length) / object_pixel_length