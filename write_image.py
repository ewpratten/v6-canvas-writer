from PIL import Image
from pathlib import Path
from typing import List
import subprocess

DOMAIN_OFFSET = (170, 70-12)
QR_OFFSET = (200, 200)

def make_address(x: int, y: int, r: int, g: int, b: int) -> str:
    return f"2400:8902:e001:233:{x:02x}{y:02x}:{r:02x}:{g:02x}:{b:02x}"

def image_to_addresses(image_path: Path, x_offset: int, y_offset: int) -> List[str]:

    # Load the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Convert to address list
    addresses = []
    for x in range(image.width):
        for y in range(image.height):
            # Get bitmap pixel
            r, g, b = image.getpixel((x, y))
            addresses.append(make_address(x + x_offset, y + y_offset, r, g, b))
            
    return addresses

def ping_address(address: str):
    print(f"Pinging {address}")
    subprocess.Popen(["ping", "-c", "5", address])
    
def main():
    
    addresses = []
    addresses.extend(image_to_addresses(Path(__file__).parent / "image.bmp", *DOMAIN_OFFSET))
    addresses.extend(image_to_addresses(Path(__file__).parent / "qr_code.bmp", *QR_OFFSET))
    
    # Update the display
    for address in addresses:
        ping_address(address)
                     
if __name__ == "__main__":
    main()