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
        num2 = random.randint(1, num1)  # Evita divisões por zero e divisões que não resultem em números inteiros
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
        self.pergunta, self.resposta_correta = "", None

    def start_new_game(self, operation):
        self.pergunta, self.resposta_correta = generate_math_question(operation)
        self.player.resposta_do_jogador = ""

    def check_answer(self):
        try:
            resposta = int(self.player.resposta_do_jogador)
            if resposta == self.resposta_correta:
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
# Função para verificar o fim de jogo
def check_game_over(game):
    if game.player.vidas <= 0:
        print("Você perdeu todas as vidas. Voltando ao menu.")
        return True
    return False

# Função para executar o jogo
def run_game():
    game = MathGame()
    clock = pygame.time.Clock()
    menu_shown = True
    car_x = 100  # Posição X inicial do carro
    car_y = 300  # Posição Y inicial do carro
    carro = pygame.image.load("d:\Projeto PCA\Carro vermelho.png")
    tamanho, largura = 5, 1.5
    car_rect = carro.get_rect()
    car_rect.topleft = (car_x, car_y)

    global selected_operation
    correct_answers = 0  # Número de respostas corretas
    correct_answers_limit = 5  # Limite de respostas corretas antes de voltar ao menu

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif menu_shown:
                if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_4:
                    selected_operation = OPERATIONS[event.key - pygame.K_1]
                    game.start_new_game(selected_operation)
                    menu_shown = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if game.check_answer():
                            print("Certa a resposta!")
                            correct_answers += 1  # Incrementa o número de respostas corretas
                            if correct_answers >= correct_answers_limit:
                                print("Você alcançou o limite de respostas corretas. Voltando ao menu.")
                                menu_shown = True
                            if car_x < 740:  # Limite o movimento a 1 casa
                                car_x += 40  # Altere a velocidade do carro conforme necessário
                            else:
                                car_x = 100  # Volte à posição inicial após 4 casas
                            car_rect.topleft = (car_x, car_y)  # Atualize a posição do carro
                        else:
                            print(f"EROU!!! A resposta correta é: {game.resposta_correta}.")
                            game.player.vidas -= 1
                            if game.player.vidas == 0:
                                print("Você perdeu todas as vidas. Fim de jogo.")
                                running = False
                        game.start_new_game(selected_operation)
                    elif event.key == pygame.K_BACKSPACE:
                        game.player.resposta_do_jogador = game.player.resposta_do_jogador[:-1]
                    elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                       pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        game.player.resposta_do_jogador += event.unicode

        # Limpa a tela
        screen.fill(WHITE)

        if menu_shown:
            show_menu()
        else:
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

        clock.tick(60)  # Limita a taxa de quadros a 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
