import pygame
from constants import *
from game import Game


pygame.init()
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))
#prendre à partir des lexèmes

def model_game_instructions(lexems):
    index_1, index_2 = 0, 0
    partie = []
    coups = []
    for i in range(len(lexems[:-2])):
        if lexems[i].tag =="semicolon":
            index_2 = i
            if index_1 == 0: 
                coup = lexems[index_1:index_2] #parceque pas de point-virgule avant le premier coup
            else:
                coup = lexems[index_1+1:index_2]
            coups.append(coup)
            index_1 = index_2
    
    for coup in coups:
        dict_coup = {
            "couleur":"",
            "piece":"",
            "position": "",
            "objectif": "",
            "actions": []
        }
        partie.append(dict_coup)
        partie[-1]["couleur"] = coup[0].value
        for index, char in enumerate(coup[1].value):
            if char == "-":
                partie[-1]["piece"] =  coup[1].value[0:index]
                partie[-1]["position"] = coup[1].value[index+1:]
                break
        partie[-1]["objectif"] = coup[2].value
        for event in coup[3:]:
            partie[-1]["actions"].append(event.tag)

    for coup in partie:
        pos = coup["position"]
        y,x = 0,0
        y = 8-int(pos[1])
        x = (     0 if pos[0] == 'a'
                else 1 if pos[0] == 'b'
                else 2 if pos[0] == 'c'
                else 3 if pos[0] == 'd'
                else 4 if pos[0] == 'e'
                else 5 if pos[0] == 'f'
                else 6 if pos[0] == 'g'
                else 7)
        coup["position"] = (y,x)

        pos = coup["objectif"]
        y = 8-int(pos[1])
        x = (     0 if pos[0] == 'a'
                else 1 if pos[0] == 'b'
                else 2 if pos[0] == 'c'
                else 3 if pos[0] == 'd'
                else 4 if pos[0] == 'e'
                else 5 if pos[0] == 'f'
                else 6 if pos[0] == 'g'
                else 7)
        coup["objectif"] = (y,x)
    return partie


def main(lexems):
    partie = model_game_instructions(lexems)
    run = True
    game_over = False
    turn = White
    FPS = 60
    game = Game(Width,Height,Rows,Cols,Square,Win)

    clics = 0
    index = 0
    try:
        while run:

            clock.tick(FPS)
            game.update_window()
            if game.check_game():
                game_over = True
            if clics == 2:
                index +=1
                clics = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

                if event.type == pygame.KEYDOWN and game_over:
                    if event.key == pygame.K_SPACE and game_over:
                        game.reset()


                if event.type == pygame.KEYDOWN and not game_over or event.type == pygame.MOUSEBUTTONDOWN and not game_over:  #remplacer par un autre bouton

                    if pygame.mouse.get_pressed()[0] or event.type == pygame.KEYDOWN:
                        if "p_reine" in partie[index]["actions"] or "p_tour" in partie[index]["actions"] or "p_cavalier" in partie[index]["actions"] or "p_fou" in partie[index]["actions"]:
                            try:
                                index_pr = partie[index]["actions"].index("p_fou")
                            except ValueError:
                                try:
                                    index_pr = partie[index]["actions"].index("p_cavalier")
                                except ValueError:
                                    try:
                                        index_pr = partie[index]["actions"].index("p_reine")
                                    except ValueError:
                                        index_pr = partie[index]["actions"].index("p_tour")
                            if clics == 0:
                                row,col = partie[index]["position"]
                                #selection pièce
                                print("pièce sélectionnée:",partie[index]["piece"])
                                game.select(row,col)
                                clics +=1
                            elif clics == 1:
                                row, col = partie[index]["objectif"]
                                #selection case
                                game.select(row,col)
                                game.promotion(row,col,partie[index]["actions"][index_pr][2:])
                                game.change_turn()
                                clics +=1
                        elif "petit_roque" not in partie[index]["actions"] and "grand_roque" not in partie[index]["actions"]:
                            if clics == 0:
                                row,col = partie[index]["position"]
                                #selection pièce
                                game.select(row,col)
                                clics +=1
                            elif clics == 1:
                                row, col = partie[index]["objectif"]
                                #selection case
                                print("pièce sélectionnée:",partie[index]["piece"])
                                game.select(row,col)
                                clics +=1
                        elif "petit_roque" in partie[index]["actions"]:
                            game.roque = True
                            if clics == 0:
                                row,col = partie[index]["position"]
                                #selection pièce
                                print("pièce sélectionnée:",partie[index]["piece"])
                                game.select(row,col)
                                clics +=1
                            elif clics == 1:
                                row, col = partie[index]["objectif"]
                                #selection case
                                game.select(row,col)
                                #déplacement tour
                                game.select(row,7)
                                game.select(row,5)
                                game.change_turn()
                                clics +=1
                        elif "grand_roque" in partie[index]["actions"]:
                            game.roque = True #flag raise pour que la fonction _move ne change pas la couleur
                            if clics == 0:
                                row,col = partie[index]["position"]
                                #selection pièce
                                print("pièce sélectionnée:",partie[index]["piece"])
                                game.select(row,col)
                                clics +=1
                            elif clics == 1:
                                row, col = partie[index]["objectif"]
                                #selection case
                                game.select(row,col)
                                #déplacement tour
                                game.select(row,0)
                                game.select(row,3)
                                game.change_turn()
                                clics +=1
                        
                        if "checkmate" in partie[index]["actions"]:
                            pass
                        elif "nul" in partie[index]["actions"]:
                            pass
    except IndexError:
        if index == len(partie):
            print("===================================================")
            print(lexems[-2].value, ": La partie s'est terminée sur un",lexems[-4].tag)
            print("===================================================")
            quit()
        quit()
