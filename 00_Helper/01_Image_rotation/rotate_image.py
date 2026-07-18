from PIL import Image

input_file = "H-Tronic_Solarladeregler.png"
output_file = "rotated.png"

angle = 0.3   # fractional degree rotation

img = Image.open(input_file)
rotated = img.rotate(angle, expand=True, resample=Image.BICUBIC)
rotated.save(output_file)
