import pygame
import subprocess
from PIL import Image

pygame.init()

# Função para carregar frames do GIF
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    for frame in range(0, gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
        frames.append(pygame.transform.scale(pygame_image, (800, 600)))
    return frames

def main_menu():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Treasure Hunt - Main Menu")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 50)

    # Carregar imagens
    background_image = pygame.image.load('assets/Iscte-Sketch.png')
    background_image = pygame.transform.scale(background_image, (800, 600))

    # Carregar frames do GIF
    gif_frames = load_gif_frames('assets/agent.gif')
    gif_frame_count = len(gif_frames)
    current_frame = 0

    while True:
        screen.fill((255, 255, 255))

        # Desenhar background
        screen.blit(background_image, (0, 0))

        # Desenhar frame atual do GIF
        screen.blit(gif_frames[current_frame], (250, 0))
        current_frame = (current_frame + 1) % gif_frame_count

        title_text = font.render("Treasure Hunt", True,(255,255,255), (0, 0, 0))
        play_qlearning_text = font_small.render("Play with Q-Learning", True, (255,255,255), (0, 0, 0))
        play_sarsa_text = font_small.render("Play with SARSA", True,(255,255,255), (0, 0, 0))
        quit_text = font_small.render("Quit", True,(255,255,255), (0, 0, 0))

        screen.blit(title_text, (150, 150))
        screen.blit(play_qlearning_text, (150, 300))
        screen.blit(play_sarsa_text, (150, 400))
        screen.blit(quit_text, (150, 500))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Coordenadas ajustadas para os botões
        if 150 <= mouse[0] <= 450 and 300 <= mouse[1] <= 350:
            if click[0] == 1:
                subprocess.run(["python", "q_learning_view.py"])
        
        if 150 <= mouse[0] <= 450 and 400 <= mouse[1] <= 450:
            if click[0] == 1:
                subprocess.run(["python", "sarsa_view.py"])

        if 150 <= mouse[0] <= 450 and 500 <= mouse[1] <= 550:
            if click[0] == 1:
                pygame.quit()
                quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
