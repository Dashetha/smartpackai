# camera_vision/objectron_infer.py
import cv2
import numpy as np
from typing import Optional, Tuple
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

class ObjectronDetector:
    def __init__(self, model_name: str = 'Shoe'):
        """
        Initialize MediaPipe Objectron detector
        Args:
            model_name: Pre-trained model name ('Shoe', 'Chair', 'Cup', 'Camera')
        """
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe not installed. Run: pip install mediapipe")
            
        self.model_name = model_name
        self.detector = mp.solutions.objectron.Objectron(
            static_image_mode=False,
            max_num_objects=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.8,
            model_name=model_name
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_object(self,
                     frame: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Detect 3D object in frame
        Args:
            frame: Input image (BGR)
        Returns:
            Tuple of (landmarks, bounding_box) or None
        """
        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Process image
        results = self.detector.process(image)
        
        if results.detected_objects:
            # Get first detected object
            detected_object = results.detected_objects[0]
            
            # Extract landmarks and bounding box
            landmarks = detected_object.landmarks_2d
            bounding_box = detected_object.rect
            
            return landmarks, bounding_box
            
        return None
        
    def draw_detection(self,
                       frame: np.ndarray,
                       landmarks: np.ndarray,
                       bounding_box: np.ndarray) -> np.ndarray:
        """
        Draw detection results on frame
        Args:
            frame: Input image (BGR)
            landmarks: Detected landmarks
            bounding_box: Detected bounding box
        Returns:
            Image with drawn detection
        """
        # Convert back to BGR for drawing
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Draw landmarks and bounding box
        self.mp_drawing.draw_landmarks(
            image, landmarks, mp.solutions.objectron.BOX_CONNECTIONS)
        self.mp_drawing.draw_axis(image, landmarks)
        
        return image
        
    def estimate_dimensions(self,
                          landmarks: np.ndarray,
                          reference_length: float) -> Tuple[float, float, float]:
        """
        Estimate object dimensions using landmarks
        Args:
            landmarks: Detected 3D landmarks
            reference_length: Known length of reference object
        Returns:
            Tuple of (length, width, height) in cm
        """
        # Calculate pixel dimensions from landmarks
        x_coords = [lm.x for lm in landmarks.landmark]
        y_coords = [lm.y for lm in landmarks.landmark]
        z_coords = [lm.z for lm in landmarks.landmark]
        
        pixel_length = max(x_coords) - min(x_coords)
        pixel_width = max(y_coords) - min(y_coords)
        pixel_height = max(z_coords) - min(z_coords)
        
        # Simple proportional estimation
        length = reference_length * pixel_length
        width = reference_length * pixel_width
        height = reference_length * pixel_height
        
        return round(length, 2), round(width, 2), round(height, 2)