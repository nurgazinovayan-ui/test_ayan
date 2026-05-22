from pathlib import Path
from PIL import Image, ImageDraw


def generate_image(prompt: str, output_dir: str = 'generated') -> str:
    Path(output_dir).mkdir(exist_ok=True)
    path = Path(output_dir) / 'draft.png'
    img = Image.new('RGB', (1080, 1350), color=(245, 245, 255))
    d = ImageDraw.Draw(img)
    d.text((40, 40), f'AI Draft\n{prompt[:150]}', fill=(20, 20, 20))
    img.save(path)
    return str(path)
