import os
import pygame
import numpy as np
from pygame import mixer

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_image(name, size, color):
    surface = pygame.Surface(size)
    surface.fill(color)
    pygame.image.save(surface, name)

def create_silent_wav(filename, duration=1.0):
    # Create a silent WAV file
    sample_rate = 44100
    samples = np.zeros(int(duration * sample_rate))
    samples = (samples * 32767).astype(np.int16)
    
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write((36 + len(samples) * 2).to_bytes(4, 'little'))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write((16).to_bytes(4, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write((1).to_bytes(2, 'little'))
        f.write(sample_rate.to_bytes(4, 'little'))
        f.write((sample_rate * 2).to_bytes(4, 'little'))
        f.write((2).to_bytes(2, 'little'))
        f.write((16).to_bytes(2, 'little'))
        f.write(b'data')
        f.write((len(samples) * 2).to_bytes(4, 'little'))
        f.write(samples.tobytes())

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, 'assets')
    images_dir = os.path.join(assets_dir, 'images')
    sounds_dir = os.path.join(assets_dir, 'sounds')
    fonts_dir = os.path.join(assets_dir, 'fonts')
    
    for directory in [assets_dir, images_dir, sounds_dir, fonts_dir]:
        create_directory(directory)
    
    # Create images
    create_image(os.path.join(images_dir, 'background.png'), (800, 600), (0, 0, 0))
    create_image(os.path.join(images_dir, 'player.png'), (64, 64), (0, 255, 0))
    create_image(os.path.join(images_dir, 'enemy.png'), (64, 64), (255, 0, 0))
    create_image(os.path.join(images_dir, 'bullet.png'), (32, 32), (255, 255, 0))
    create_image(os.path.join(images_dir, 'ufo.png'), (64, 64), (0, 0, 255))
    
    # Create sound files
    create_silent_wav(os.path.join(sounds_dir, 'background.wav'), 1.0)
    create_silent_wav(os.path.join(sounds_dir, 'laser.wav'), 0.5)
    create_silent_wav(os.path.join(sounds_dir, 'explosion.wav'), 0.5)
    
    # Copy system font
    system_font = pygame.font.get_default_font()
    if os.path.exists(system_font):
        import shutil
        shutil.copy(system_font, os.path.join(fonts_dir, 'freesansbold.ttf'))
    
    print("Placeholder assets created successfully!")

if __name__ == "__main__":
    main() 