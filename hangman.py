import pygame, math, random

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Hangman Game')

RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS*2 + GAP)*13)/2)
starty = 400

A = 65
for i in range(26): # appends the letters list [x, y, capital_letters A to Z, True boolean]
    x = startx + GAP*2 + ((RADIUS*2 + GAP)*(i%13))
    y = starty + ((i//13)*(GAP + RADIUS*2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

images = []
for i in range(7):
    image = pygame.image.load(r"C:\Users\Amundeep\Pictures\Camera Roll\hangman"+ str(i)+".png")
    images.append(image)

# game variable
hangman_status = 0
words = ['HARDEEP', 'MOHINDER', 'JAVASCRIPT', 'DHALIWAL', 'PUNJABI']
word = random.choice(words)
guessed = [] 

#colours 
WHITE = (255,255,255)
BLACK = (0,0,0)

def draw():
    screen.fill(WHITE)

    text = TITLE_FONT.render('DEVELOPER HANGMAN', 1, BLACK)
    screen.blit(text, ((WIDTH - text.get_width())/2, 20))

    #draw word
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += ' '
    text = WORD_FONT.render(display_word, 1 ,BLACK)
    screen.blit(text, (400, 200))

    # draw buttons 
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen,BLACK, (x,y), RADIUS, (3))
            text = LETTER_FONT.render(ltr, 1, BLACK)
            screen.blit(text, (x- text.get_width()/2,y - text.get_height()/2))
    
    screen.blit(images[hangman_status], (150,100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    screen.fill(WHITE)
    text = WORD_FONT.render(message, 1 ,BLACK)
    screen.blit(text, ((WIDTH- text.get_width())/2, (HEIGHT- text.get_height())/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible =letter
                    if visible:
                        dis = ((x-m_x)**2 + (y - m_y)**2)**0.5
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            display_message('You won!')
            break

        if hangman_status == 6:
            display_message('You lost!')
            break

while True:
    main()
    if input('Do you want to play again?').lower().startswith('n'):
        break
pygame.quit()


