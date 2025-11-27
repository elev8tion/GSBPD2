from setuptools import setup, find_packages

setup(
    name="kre8vidmems",
    version="0.1.0",
    description="Video-based AI memory using QR codes and semantic search",
    author="Kre8VidMems Team",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "qrcode[pil]",
        "sentence-transformers",
        "annoy",
        "tqdm",
        "Pillow",
        "pyzbar",
    ],
    python_requires=">=3.8",
)
