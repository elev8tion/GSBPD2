"""
QR Code generation and decoding
"""
import qrcode
import cv2
import numpy as np
import gzip
import base64
from PIL import Image
from typing import Optional, Tuple
from kre8vidmems.config import (
    QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, 
    QR_BORDER, QR_FILL_COLOR, QR_BACK_COLOR
)

def encode_to_qr(data: str) -> Image.Image:
    """Encode string to QR code image"""
    
    # Compress if large
    if len(data) > 100:
        compressed = gzip.compress(data.encode('utf-8'))
        b64 = base64.b64encode(compressed).decode('ascii')
        data = f"GZ:{b64}"
        
    qr = qrcode.QRCode(
        version=QR_VERSION,
        error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{QR_ERROR_CORRECTION}"),
        box_size=QR_BOX_SIZE,
        border=QR_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    return qr.make_image(fill_color=QR_FILL_COLOR, back_color=QR_BACK_COLOR)

def qr_to_numpy(qr_image: Image.Image, target_size: Tuple[int, int]) -> np.ndarray:
    """Convert PIL QR image to OpenCV numpy array (BGR)"""
    # Resize
    qr_image = qr_image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to RGB
    if qr_image.mode != 'RGB':
        qr_image = qr_image.convert('RGB')
        
    # Convert to numpy
    arr = np.array(qr_image)
    
    # Convert RGB to BGR (OpenCV standard)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def decode_qr(image: np.ndarray) -> Optional[str]:
    """Decode QR code from OpenCV image"""
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)
    
    if data:
        if data.startswith("GZ:"):
            try:
                b64 = data[3:]
                compressed = base64.b64decode(b64)
                data = gzip.decompress(compressed).decode('utf-8')
            except Exception:
                return None # Decompression failed
        return data
    return None
