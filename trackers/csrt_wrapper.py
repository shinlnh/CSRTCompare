"""
CSRT Tracker Wrapper - OpenCV implementation
Channel and Spatial Reliability Tracker
"""
import cv2
import numpy as np

class CSRTWrapper:
    """Wrapper for OpenCV CSRT tracker"""
    
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.initialized = False
        self.bbox = None
        
    def init(self, frame, bbox):
        """
        Initialize CSRT tracker
        Args:
            frame: numpy array (H, W, 3)
            bbox: tuple (x, y, w, h)
        """
        self.bbox = bbox
        success = self.tracker.init(frame, bbox)
        self.initialized = success
        return success
    
    def update(self, frame):
        """
        Track object in new frame
        Args:
            frame: numpy array (H, W, 3)
        Returns:
            success (bool), bbox (x, y, w, h)
        """
        if not self.initialized:
            return False, self.bbox
            
        success, bbox = self.tracker.update(frame)
        if success:
            self.bbox = bbox
        return success, self.bbox
    
    def get_name(self):
        return "CSRT"
