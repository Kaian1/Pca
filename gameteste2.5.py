import pygame
import requests
from io import BytesIO
import random
import sys

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corrida Matemática")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Defina as variáveis globais
correct_answers_limit = 5

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

# Classe para representar o bot
class Bot:
    def __init__(self):
        self.vidas = 3

    def reset(self):
        self.vidas = 3

    def get_answer(self):
        # Lógica para gerar uma resposta do bot
        return random.randint(1, 9)

# Classe para representar o jogo de perguntas matemáticas
class MathGame:
    def __init__(self):
        self.player = Player()
        self.bot = Bot()
        self.font = pygame.font.Font(None, 36)
        self.pergunta, self.resposta_correta = ("", None)
        self.correct_answers = 0
        self.correct_answers_bot = 0
        self.car_x_initial = 100
        self.car_x_player = self.car_x_initial
        self.car_x_bot = self.car_x_initial
        self.car_y = 300
        self.last_bot_move_time = pygame.time.get_ticks()

    def start_new_game(self, operation):
        self.pergunta, self.resposta_correta = generate_math_question(operation)
        self.player.resposta_do_jogador = ""
        self.bot.reset()

    def reset(self):
        self.player.reset()
        self.bot.reset()
        self.correct_answers = 0
        self.correct_answers_bot = 0
        self.car_x_player = self.car_x_initial
        self.car_x_bot = self.car_x_initial
        self.last_bot_move_time = pygame.time.get_ticks()

    def check_answer(self, is_player=True):
        try:
            resposta = int(self.player.resposta_do_jogador) if is_player else self.bot.get_answer()
            if resposta == self.resposta_correta:
                if is_player:
                    self.correct_answers += 1
                    if self.correct_answers >= correct_answers_limit:
                        print("Você alcançou o limite de respostas corretas. Voltando ao menu.")
                        self.reset()
                        return True
                else:
                    if self.car_x_bot >= 200:
                        print("O bot atingiu 5 casas. Você perdeu! Voltando ao menu.")
                        self.reset()
                        return True
                    self.correct_answers_bot += 1
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

    # Baixar a imagem da URL para o carro do jogador
    url_player = "https://github.com/Kaian1/Pca/raw/master/Carro%20vermelho.png"
    response_player = requests.get(url_player)

    # Verificar se o download foi bem-sucedido
    if response_player.status_code == 200:
        # Carregar a imagem do carro do jogador a partir dos dados baixados
        carro_player = pygame.image.load(BytesIO(response_player.content))
        car_rect_player = carro_player.get_rect()
        car_rect_player.topleft = (car_x, car_y)
    else:
        print("Erro ao baixar a imagem do carro do jogador")

    # Baixar a imagem da URL para o carro do bot
    url_bot = "https://github.com/Kaian1/Pca/blob/master/Carro%20ciano.png?raw=true"
    response_bot = requests.get(url_bot)

    # Verificar se o download foi bem-sucedido
    if response_bot.status_code == 200:
        # Carregar a imagem do carro do bot a partir dos dados baixados
        carro_bot = pygame.image.load(BytesIO(response_bot.content))
        car_rect_bot = carro_bot.get_rect()
        car_rect_bot.topleft = (car_x, car_y)
    else:
        print("Erro ao baixar a imagem do carro do bot")

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
                                game.reset()
                                car_x = game.car_x_initial
                                correct_answers = 0
                            if game.car_x_player < 740:
                                game.car_x_player += 40
                            else:
                                game.car_x_player = 100
                            car_rect_player.topleft = (game.car_x_player, car_y)
                        else:
                            print(f"ERROU!!! A resposta correta é: {game.resposta_correta}.")
                            game.player.vidas -= 1
                            if game.player.vidas == 0:
                                print("Você perdeu todas as vidas. Voltando ao menu.")
                                game_state = MENU
                                game.reset()
                                car_x = game.car_x_initial
                    elif event.key == pygame.K_BACKSPACE:
                        game.player.resposta_do_jogador = game.player.resposta_do_jogador[:-1]
                    else:
                        game.player.resposta_do_jogador += event.unicode

        # Limpa a tela
        screen.fill(WHITE)

        if game_state == MENU:
            show_menu()
        elif game_state == GAME:
            # Exibe as vidas do jogador na tela
            text = game.font.render(f"Vidas do jogador: {game.player.vidas}", True, BLACK)
            screen.blit(text, (10, 10))

            # Exibe a pergunta na tela
            text = game.font.render(game.pergunta, True, BLACK)
            screen.blit(text, (100, 100))

            # Exibe a entrada do jogador na tela
            text = game.font.render(f"Sua resposta: {game.player.resposta_do_jogador}", True, BLACK)
            screen.blit(text, (100, 150))

            # Desenha o carro do jogador na tela
            screen.blit(carro_player, car_rect_player)

            # Movimenta o carro do bot a cada 7 segundos
            current_time = pygame.time.get_ticks()
            if current_time - game.last_bot_move_time >= 7000:
                game.last_bot_move_time = current_time
                if game.car_x_bot < 740:
                    game.car_x_bot += 40
                else:
                    game.car_x_bot = 100
                car_rect_bot.topleft = (game.car_x_bot, car_y)

            # Desenha o carro do bot na tela
            screen.blit(carro_bot, car_rect_bot)

        # Atualiza a tela
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
