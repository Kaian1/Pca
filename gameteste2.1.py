import pygame
import random
import sys

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Perguntas Matemáticas")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Operações matemáticas disponíveis
OPERATIONS = ["1-Adição (+)", "2-Subtração (-)", "3-Multiplicação (*)", "4-Divisão (÷)"]

# Variável para armazenar a operação selecionada
selected_operation = None

# Defina os estados do jogo
MENU = 0
GAME = 1

# Inicialize o estado do jogo como MENU
game_state = MENU

# Função para gerar uma pergunta matemática com base na operação selecionada
def generate_math_question(operation, valor_min=1, valor_max=9):
    num1 = random.randint(valor_min, valor_max)
    num2 = random.randint(valor_min, valor_max)

    if operation == "1-Adição (+)":
        pergunta = f"Quanto é {num1} + {num2}?"
        resposta = num1 + num2
    elif operation == "2-Subtração (-)":
        pergunta = f"Quanto é {num1} - {num2}?"
        resposta = num1 - num2
    elif operation == "3-Multiplicação (*)":
        pergunta = f"Quanto é {num1} x {num2}?"
        resposta = num1 * num2
    elif operation == "4-Divisão (÷)":
        num2 = random.randint(1, num1)
        pergunta = f"Quanto é {num1} ÷ {num2}?"
        resposta = num1 // num2

    return pergunta, resposta

# Classe para representar o jogador
class Player:
    def __init__(self):
        self.vidas = 3
        self.resposta_do_jogador = ""

    def reset(self):
        self.vidas = 3
        self.resposta_do_jogador = ""

# Classe para representar o jogo de perguntas matemáticas
class MathGame:
    def __init__(self):
        self.player = Player()
        self.font = pygame.font.Font(None, 36)
        self.pergunta, self.resposta_correta = ("", None)

    def start_new_game(self, operation):
        self.pergunta, self.resposta_correta = generate_math_question(operation)
        self.player.resposta_do_jogador = ""

    def check_answer(self):
        try:
            resposta = int(self.player.resposta_do_jogador)
            if resposta == self.resposta_correta:
                self.start_new_game(selected_operation)  # Mude a pergunta quando acertar
                return True
            else:
                return False
        except ValueError:
            return False

# Função para exibir o menu na tela
def show_menu():
    font = pygame.font.Font(None, 48)
    text = font.render("Escolha uma operação matemática:", True, BLACK)
    screen.blit(text, (150, 200))

    y = 250
    for i, operation in enumerate(OPERATIONS):
        text = font.render(operation, True, BLACK)
        screen.blit(text, (200, y))
        y += 50

# Função para executar o jogo
def run_game():
    global game_state
    game_state = MENU

    game = MathGame()

    clock = pygame.time.Clock()
    car_x = 100
    car_y = 300
    carro = pygame.image.load("C:\Projeto PCA\Carro vermelho.png")
    tamanho, largura = 5, 1.5
    car_rect = carro.get_rect()
    car_rect.topleft = (car_x, car_y)

    global selected_operation
    correct_answers = 0
    correct_answers_limit = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == MENU:
                if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_4:
                    selected_operation = OPERATIONS[event.key - pygame.K_1]
                    game_state = GAME
                    game.start_new_game(selected_operation)
            elif game_state == GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game.check_answer():
                            print("Certa a resposta!")
                            correct_answers += 1
                            if correct_answers >= correct_answers_limit:
                                print("Você alcançou o limite de respostas corretas. Voltando ao menu.")
                                game_state = MENU
                            if car_x < 740:
                                car_x += 40
                            else:
                                car_x = 100
                            car_rect.topleft = (car_x, car_y)
                        else:
                            print(f"ERROU!!! A resposta correta é: {game.resposta_correta}.")
                            game.player.vidas -= 1
                            if game.player.vidas == 0:
                                print("Você perdeu todas as vidas. Voltando ao menu.")
                                game_state = MENU
                    elif event.key == pygame.K_BACKSPACE:
                        game.player.resposta_do_jogador = game.player.resposta_do_jogador[:-1]
                    else:
                        game.player.resposta_do_jogador += event.unicode

        # Limpa a tela
        screen.fill(WHITE)

        if game_state == MENU:
            show_menu()
        elif game_state == GAME:
            # Exibe as vidas na tela
            text = game.font.render(f"Vidas: {game.player.vidas}", True, BLACK)
            screen.blit(text, (10, 10))

            # Exibe a pergunta na tela
            text = game.font.render(game.pergunta, True, BLACK)
            screen.blit(text, (100, 100))

            # Exibe a entrada do jogador na tela
            text = game.font.render(f"Sua resposta: {game.player.resposta_do_jogador}", True, BLACK)
            screen.blit(text, (100, 150))

            # Desenhe o carro na tela
            screen.blit(carro, car_rect)

        # Atualiza a tela
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
