# camera_vision/reference_detection.py
import cv2
import numpy as np
from typing import Optional, Tuple

class ReferenceDetector:
    def __init__(self):
        # Predefined reference objects (A4 paper, credit card)
        self.reference_objects = {
            'a4': {
                'width': 21.0,  # cm (short edge)
                'height': 29.7, # cm (long edge)
                'ar': 29.7/21.0, # Aspect ratio
                'color_range': {
                    'lower': np.array([0, 0, 200]),
                    'upper': np.array([180, 30, 255])
                }
            },
            'credit_card': {
                'width': 8.56,  # cm
                'height': 5.398, # cm
                'ar': 5.398/8.56,
                'color_range': {
                    'lower': np.array([0, 0, 150]),
                    'upper': np.array([180, 80, 255])
                }
            }
        }
        
    def detect_reference(self,
                        frame: np.ndarray,
                        reference_type: str = 'a4') -> Optional[Tuple[float, float, np.ndarray]]:
        """
        Detect reference object in frame
        Args:
            frame: Input image (BGR)
            reference_type: Type of reference object ('a4' or 'credit_card')
        Returns:
            Tuple of (pixel_width, pixel_height, contour) or None
        """
        if reference_type not in self.reference_objects:
            raise ValueError(f"Unknown reference type: {reference_type}. Choose 'a4' or 'credit_card'")
            
        ref_obj = self.reference_objects[reference_type]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask based on color range
        mask = cv2.inRange(hsv, 
                          ref_obj['color_range']['lower'],
                          ref_obj['color_range']['upper'])
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            # Check if quadrilateral
            if len(approx) == 4:
                # Calculate aspect ratio
                rect = cv2.minAreaRect(cnt)
                width, height = rect[1]
                if width > height:
                    width, height = height, width
                ar = height / width
                
                # Check if aspect ratio matches reference
                if abs(ar - ref_obj['ar']) < 0.1:  # 10% tolerance
                    # Return dimensions in pixels and contour
                    return width, height, cnt
                    
        return None
        
    def draw_reference(self,
                      frame: np.ndarray,
                      contour: np.ndarray) -> np.ndarray:
        """
        Draw reference object contour on frame
        Args:
            frame: Input image (BGR)
            contour: Detected contour
        Returns:
            Image with drawn contour
        """
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
        return frame