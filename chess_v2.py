import pygame
import sys

pygame.init()

display_width = 1280
display_height = 900

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("chess")
clock = pygame.time.Clock()

black = (0, 0, 0) 
white = (255, 255, 255) 
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark = (209,139,71)
light = (255,206,158)

smallfont = pygame.font.SysFont('Corbel',35)
largefont = pygame.font.SysFont('Corbel',155)  

text = smallfont.render('Start' , True , black)
title = largefont.render('CHESS' , True , black)

class Board():
    def __init__(self):
        self.width = 8
        self.height = 8
        self.data = []
        self.size = 96
        self.x_offset = 224
        self.y_offset = 64
        self.move_options_image = pygame.image.load("move_options.png")
        self.move_options = []
        self.danger_zone = []
        self.future_danger_zone = []
        self.active_piece = None
        self.king_danger = False
        self.king_black_danger = False
        self.end = False
        self.king_enemy_moves = None
        self.turn = "white"
        self.menu = True
    

    def pieces(self):

        self.data[0][7] = Rook(0,7,"white")
        self.data[1][7] = Knight(1,7,"white")
        self.data[2][7] = Bishop(2,7,"white")
        self.data[3][7] = Queen(3,7,"white")
        self.data[4][7] = King(4,7,"white")
        self.data[5][7] = Bishop(5,7,"white")
        self.data[6][7] = Knight(6,7,"white")
        self.data[7][7] = Rook(7,7,"white")
        for i in range(8):
            self.data[i][6] = Pawn(i,6,"white")

        self.data[0][0] = Rook(0,0,"black")
        self.data[1][0] = Knight(1,0,"black")
        self.data[2][0] = Bishop(2,0,"black")
        self.data[3][0] = Queen(3,0,"black")
        self.data[4][0] = King(4,0,"black")
        self.data[5][0] = Bishop(5,0,"black")
        self.data[6][0] = Knight(6,0,"black")
        self.data[7][0] = Rook(7,0,"black")
        for i in range(8):
            self.data[i][1] = Pawn(i,1,"black")    
            

    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        
        
    def setup(self):
        for i in range(self.width):
            self.data.append([])
            for j in range(self.height):
                self.data[i].append(0)

    def print(self):
        for i in range(self.height):
            #print (self.data[i])
            pass

    def draw_board(self):
         if (self.menu):
             pygame.draw.rect(gameDisplay,black,[display_width/2-45,display_height/2-5,150,50])
             pygame.draw.rect(gameDisplay,white,[display_width/2-40,display_height/2,140,40])
             image1 = pygame.image.load("Rook_black.png")
             image2 = pygame.image.load("Rook_white.png")
             image1 = pygame.transform.scale(image1, (200, 200))
             image2 = pygame.transform.scale(image2, (200, 200)) 
             gameDisplay.blit(image1,(200,110))
             gameDisplay.blit(image2,(900,110))
             gameDisplay.blit(text ,(display_width/2-5,display_height/2+5))
             gameDisplay.blit(title ,( display_width/2 - 210,150))
         else:
            color = light
            for i in range(8):
                if color == dark:
                    color = light
                else:
                    color = dark  
                for j in range(8):
                    if color == dark:
                        color = light
                    else:
                        color = dark
                    pygame.draw.rect(gameDisplay,color,[self.size * i + self.x_offset ,self.size * j + self.y_offset ,self.size,self.size])
                    if self.data[i][j] != 0:
                        gameDisplay.blit(self.data[i][j].image,(self.size * i + self.x_offset,self.size * j + self.y_offset))
            for p in range(len(self.move_options)):
                        for d in range(len(self.move_options[p])):
                            if type(self.move_options[p][d]) == list :
                                gameDisplay.blit(self.move_options_image,(self.size * self.move_options[p][d][0] + self.x_offset,self.size * self.move_options[p][d][1] + self.y_offset))
                            else:
                                break

    def pre_move(self,i,j):
        
        self.move_piece(i,j)
        self.king_danger = False
        self.move_options = []
        if self.active_piece.name == "pawn":
            if self.active_piece.y == 0 or self.active_piece.y == 7:
                p = self.active_piece.change_pieces()
                self.data[self.active_piece.x][self.active_piece.y] = p
            self.active_piece.start = False
        self.active_piece = None
        #self.check_king()
        #self.move_options = []
        self.check_king_danger()
        self.move_options = []
        #self.king_danger = False
        self.check_sah_mat()
        
                        
    def check_mouse_click(self,pos):
        x = pos[0]
        y = pos[1]
        
        for i in range(self.width):
            for j in range(self.width):
                if x > self.size * i + self.x_offset and  x < self.size * (i+1) + self.x_offset:
                    if y > self.size * j + self.y_offset and  y < self.size * (j+1) + self.y_offset: 
                        """if self.king_danger == True:
                            if self.data[i][j] != 0 and self.data[i][j].name == "king" and self.data[i][j].color == self.turn:
                                self.move_king(i,j)"""
                    
                        for p in range(len(self.move_options)):
                            for d in range(len(self.move_options[p])):
                                #print (self.move_options)
                                if type(self.move_options[p][d]) == list:
                                    if self.move_options[p][d][0] == i and self.move_options[p][d][1] == j:
                                        self.pre_move(i,j)
                                        return
                                else:
                                    if self.move_options[p][d].x ==  i and self.move_options[p][d].y == j:
                                        if self.data[i][j] == 0 or self.data[i][j].color != self.turn:
                                            self.pre_move(i,j)
                                            return
                                    break    
                            
                        if self.data[i][j] != 0 and self.data[i][j].color == self.turn:        
                            self.move_options = []
            
                            if self.king_danger == False:
                                self.move_options = self.data[i][j].activate(self.data,False)
                                self.can_move_piece(self.data[i][j])
                            else:
                                if self.find_pieces_def_king(self.data[i][j]):
                                   self.move_options = self.data[i][j].activate(self.data,False)
                                   
                            if self.data[i][j].name == "king":
                                #self.check_king()
                           
                                self.move_king(i,j)
                                #self.king_danger = False
                            self.active_piece = self.data[i][j]
                            return
        self.move_options = []
        self.active_piece = None
        

    def check_king_danger(self):
        self.king_enemy_moves = []
        self.move_options = []
        p = []       
        self.danger_zone = []
        x = 0
        y = 0
        for m in range(8):
            for n in range(8):
                if self.data[m][n] != 0 and self.data[m][n].name != "king" and self.data[m][n].color != self.turn:
                    p = self.data[m][n].activate(self.data,True)
                    for i in range(len(p)):
                        self.move_options.append([])
                        for j in range(len(p[i])):
                            if type(p[i][j]) == list or p[i][j].name == "king":
                                self.move_options[i].append(p[i][j])
                                if type(p[i][j]) != list and p[i][j].name == "king" and p[i][j].color == self.turn:
                                    self.king_danger = True
                                    self.danger_zone.append(p[i])
                                    self.danger_zone.append([self.data[m][n]])
                            else:
                                self.move_options[i].append([p[i][j].x,p[i][j].y])
                                break
                        for j in range(len(p[i])):
                            if type(p[i][j]) != list and p[i][j].name == "king" and p[i][j].color == self.turn:
                                self.future_danger_zone.append(p[i])
                                x = m
                                y = n

        self.future_danger_zone.append([self.data[x][y]])                        
        return  self.move_options                 

    def can_move_piece(self,piece):
        moves = piece.activate(self.data,False)
        #print ("piece" , piece.name)
        a = False
        #print ("self.future_danger_zone" , self.future_danger_zone)
        for i in range(len(self.future_danger_zone)):
            for j in range(len(self.future_danger_zone[i])):
                if self.future_danger_zone[i][j] == piece:
                    self.move_options = []
                    a = True
        if a:
            #print ("moves",moves)
            self.move_options.append([])
            for i in range(len(self.future_danger_zone)):
                for j in range(len(self.future_danger_zone[i])):            
                    for m in range(len(moves)):
                        for n in range(len(moves[m])):
                            if self.future_danger_zone[i][j] == list:
                                if self.future_danger_zone[i][j] == moves[m][n]:
                                    if type(moves[m][n]) == list:
                                        self.move_options[0].append(moves[m][n])
                            else:
                                if j == len(self.future_danger_zone[i])-1:
                                    if [self.future_danger_zone[i][j].x,self.future_danger_zone[i][j].y] == moves[m][n]:
                                        if type(moves[m][n]) == list:
                                            self.move_options[0].append(moves[m][n])
                                    
    def find_pieces_def_king(self,piece):
        moves = piece.activate(self.data,False)
        self.move_options.append([])
        for i in range(len(self.danger_zone)):
            for j in range(len(self.danger_zone[i])):
                for m in range(len(moves)):
                    for n in range(len(moves[m])):
                        if type(self.danger_zone[i][j]) == list:
                            if self.danger_zone[i][j] == moves[m][n]:
                                if type(moves[m][n]) == list:
                                    
                                    self.move_options[0].append(moves[m][n])
                                else:
                                    self.move_options[0].append([moves[m][n].x,moves[m][n].y])
                        else:
                            if [self.danger_zone[i][j].x,self.danger_zone[i][j].y] == moves[m][n]:
                                self.move_options[0].append(moves[m][n])
                                
                                
                            
    def check_king(self):
        self.check_king_danger()
        self.king_enemy_moves = self.move_options
        #self.check_sah_mat(x,y)
        
    def check_sah_mat(self):
        for i in range(8):
            for j in range(8):
                if  self.data[i][j] != 0 and  self.data[i][j].name == "king" and  self.data[i][j].color == self.turn:
                    self.move_king(i,j)
        if self.end:
            
            if self.turn == "white":
                print ("black win")
          
          
            else:
                print ("white win")
    
               
        self.move_options = []    

    def win_mess(self):
        Winfont = pygame.font.SysFont('Corbel',155) 
        if self.end:
            if self.turn == "white":
                pygame.draw.rect(gameDisplay,white,[display_width/2 - 250,150,575,130])
                black_win = Winfont.render('Black win' , True , black)
                gameDisplay.blit(black_win ,(display_width/2 - 250,150))
              
            else:
                pygame.draw.rect(gameDisplay,white,[display_width/2 - 250,150,575,130])
                white_win = Winfont.render('White win' , True , black)
                gameDisplay.blit(white_win ,(display_width/2-5,display_height/2+5))
         
            
        
        
    def move_king(self,x,y):
        self.check_king()
        king = self.data[x][y]
        king_available_moves = king.activate(self.data,False) 
        for i in range(len(self.king_enemy_moves)):
            for j in range(len(self.king_enemy_moves[i])):
                for m in range(len(king_available_moves)):
                    for n in range(len(king_available_moves[m])):
                        if self.king_enemy_moves[i][j] == king_available_moves[m][n]:
                            king_available_moves[m].pop(n)
                            break        
        self.king_enemy_moves = []
        for i in range(8):
            for j in range(len(king_available_moves)):
                if king_available_moves[j] == [] or type(king_available_moves[j][0]) != list:
                    king_available_moves.pop(j)
                    break
        #print (king_available_moves)        
        if len(king_available_moves) == 0:
            if self.king_danger == True:
                #print ("dinajs je moj najbolji prijatelj")
                if not(self.check_mat()):
                    print ("sah mat")
                    
                    
                    self.end = True
            else:
                print ("mat") # moram popraviti ovo tako da 
        self.move_options = king_available_moves

    def check_mat(self):
        
        for x in range(8):
            for y in range(8):
                if self.data[x][y] != 0 and self.data[x][y].color == self.turn :
                    moves = self.data[x][y].activate(self.data,False)
                    #print (moves )
                    for i in range(len(self.danger_zone)):
                            for j in range(len(self.danger_zone[i])):            
                                for m in range(len(moves)):
                                    for n in range(len(moves[m])):
                                        
                                        if type(self.danger_zone[i][j]) == list:
                    
                                            if self.danger_zone[i][j] == moves[m][n]:
                                                if type(moves[m][n]) == list and self.data[x][y].name != "king":
                                                    #print ("dn " , moves)
                                                    return True
                                        else:
                                            if j == len(self.danger_zone[i])-1 :
                                                if [self.danger_zone[i][j].x,self.danger_zone[i][j].y] == moves[m][n]:
                                                    
                                                    if type(moves[m][n]) == list:
                                                                #print ("dn " , moves)
                                                                return True
        return False                                                   

        
                        
    def move_piece(self,x,y):
        self.change_turn()
        self.data[self.active_piece.x][self.active_piece.y] = 0
        if self.data[x][y] != 0:
            print (self.data[x][y].name + ' ' + self.data[x][y].color +' is dead')
        self.data[x][y] = self.active_piece
        self.active_piece.x = x
        self.active_piece.y = y
        self.future_danger_zone = []
        #self.move_options = []
        
# ---------------------------------------------------------------------------------------------------------------------------------------
class Pawn():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "pawn"
        self.color = color
        self.image = pygame.image.load("pawn_" + self.color + ".png")

        self.start = True

    def activate(self,data,king):
        move_options = []
        a = 1
        if self.color == "white":
            a = -1
        for i in range(4):
            move_options.append([])    
        if self.y < 7 and self.y > 0:
            if self.x < 7:
                if data[self.x + 1][self.y + a] != 0 and data[self.x + 1][self.y + a].color != self.color:
                    move_options[0].append([self.x + 1,self.y + a])
            if self.x > 0:
                if data[self.x - 1][self.y + a] != 0 and data[self.x - 1][self.y + a].color != self.color:    
                    move_options[1].append([self.x - 1,self.y + a]) 
        for i in range(1,3):
            b = i
            if self.color == "white":
                b *= -1
            if abs(b) == 2 and self.start == False:
                    return move_options
            if self.y + b < 8 and data[self.x][self.y + b] == 0:
                    move_options[abs(b) + 1].append([self.x ,self.y + b]) 
        return move_options

    def change_pieces(self):
        return Queen(self.x,self.y,self.color)
        
class Rook():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "rook"
        self.color = color
        self.image = pygame.image.load("rook_"+ self.color +".png")
   
        self.start = True

    def activate(self,data,king):
        move_options = []
        pos = -1
        for i in range(4):
            move_options.append([])
        for j in (-1,1):
                pos += 1
                for i in range(1,16):
                    if self.x + i * j <= 7 and self.x + i * j >= 0:
                        if data[self.x + i * j][self.y] != 0:
                            move_options[pos].append(data[self.x + i * j][self.y])
                        else:    
                            move_options[pos].append([self.x + i * j,self.y])
                pos += 1           
                for i in range(1,16):        
                    if self.y + i * j <= 7 and self.y + i * j >= 0:
                        if data[self.x][self.y + i * j] != 0:
                            move_options[pos].append(data[self.x ][self.y+ i * j])
                        else: 
                            move_options[pos].append([self.x ,self.y + i * j])

        return move_options


class Bishop():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "bishop"
        self.color = color
        self.image = pygame.image.load("bishop_"+ self.color +".png")
        self.start = True

    def activate(self,data,king):
        move_options = []
        pos = -1
        for i in range(4):
            move_options.append([])
        for j in (-1,1):
            for k in (-1,1):
                pos += 1
                for i in range(1,16):
                    if self.x + i * j <= 7 and self.x + i * j >= 0 and self.y + i * k >= 0 and self.y + i * k <= 7:
                            if data[self.x + i * j][self.y + i * k] != 0:
                                move_options[pos].append(data[self.x + i * j][self.y + i * k])
                            else:
                                move_options[pos].append([self.x + i * j,self.y + i * k])
        return move_options


class Knight():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "knight"
        self.color = color
        self.image = pygame.image.load("knight_" + self.color +".png")
        self.start = True

    def activate(self,data,king):
        move_options = []
        pos = -1
        for i in range(8):
            move_options.append([])
            
        for i in (-1,1):
            for j in (-2,2):
                pos += 1
                if  self.x + i <= 7 and self.x + i >= 0  and self.y + j >= 0 and self.y + j <= 7:
                    if data[self.x + i][self.y + j] != 0:
                        move_options[pos].append(data[self.x + i][self.y + j])
                    else:
                        move_options[pos].append([self.x + i,self.y + j])        
                pos += 1
                if  self.x + j <= 7 and self.x + j >= 0  and self.y + i >= 0 and self.y + i <= 7:
                    if data[self.x + j][self.y + i] != 0:
                        move_options[pos].append(data[self.x + j][self.y + i])
                    else:
                        move_options[pos].append([self.x + j,self.y + i])
        return move_options       
    

class Queen():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "queen"
        self.color = color
        self.image = pygame.image.load("queen_" + self.color + ".png")
        self.start = True

    def activate(self,data,king):
        move_options = []
        m_pos_d = [1,1,1,1]
        m_pos = [1,1,1,1]
        pos = -1
        for i in range(8):
            move_options.append([])
        for j in (-1,1):
                pos += 1
                for i in range(1,16):
                    if self.x + i * j <= 7 and self.x + i * j >= 0:
                        if data[self.x + i * j][self.y] != 0:
                            move_options[pos].append(data[self.x + i * j][self.y])
                        else:    
                            move_options[pos].append([self.x + i * j,self.y])
                pos += 1           
                for i in range(1,16):        
                    if self.y + i * j <= 7 and self.y + i * j >= 0:
                        if data[self.x][self.y + i * j] != 0:
                            move_options[pos].append(data[self.x ][self.y+ i * j])
                        else: 
                            move_options[pos].append([self.x ,self.y + i * j])
        for j in (-1,1):
            for k in (-1,1):
                pos += 1
                for i in range(1,16):
                    if self.x + i * j <= 7 and self.x + i * j >= 0 and self.y + i * k >= 0 and self.y + i * k <= 7:
                            if data[self.x + i * j][self.y + i * k] != 0:
                                move_options[pos].append(data[self.x + i * j][self.y + i * k])
                            else:
                                move_options[pos].append([self.x + i * j,self.y + i * k])                     
            
        return move_options




class King():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.name = "king"
        self.color = color
        self.image = pygame.image.load("king_"+ self.color +".png")
        self.start = True    
        

    def activate(self,data,king):
        
        move_options = []
        for i in range(8):
            move_options.append([])
        if self.x + 1 <= 7:
            if data[self.x + 1][self.y] != 0:
                move_options[0].append(data[self.x + 1][self.y])
            else:
                move_options[0].append([self.x + 1,self.y])
        if self.x - 1 >= 0:
            if data[self.x - 1][self.y] != 0:
                move_options[1].append(data[self.x - 1][self.y])
            else:
                move_options[1].append([self.x - 1,self.y])
        if self.y + 1 <= 7:
            if data[self.x][self.y + 1] != 0:
                move_options[2].append(data[self.x][self.y + 1])
            else:
                move_options[2].append([self.x,self.y + 1])
        if self.y - 1 >= 0:
            if data[self.x][self.y - 1] != 0:
                move_options[3].append(data[self.x][self.y - 1])
            else:
                move_options[3].append([self.x,self.y - 1])
            
        if self.x + 1 <= 7  and self.y + 1 <= 7:
            if data[self.x + 1][self.y + 1] != 0:
                move_options[4].append(data[self.x + 1][self.y+1])
            else:
                move_options[4].append([self.x + 1,self.y+1])
        if self.x - 1 >= 0  and self.y - 1 >= 0:
            if data[self.x - 1][self.y - 1] != 0:
                move_options[5].append(data[self.x - 1][self.y-1])
            else:
                move_options[5].append([self.x - 1,self.y-1])
        if self.x + 1 <= 7  and self.y - 1 >= 0:
            if data[self.x + 1][self.y - 1] != 0:
                move_options[6].append(data[self.x + 1][self.y - 1])
            else:
                move_options[6].append([self.x + 1,draw_boardself.y - 1])
        if self.x - 1 >= 0  and self.y + 1 <= 7:
            if data[self.x - 1][self.y + 1] != 0:
                move_options[7].append(data[self.x - 1][self.y + 1])
            else:
                move_options[7].append([self.x - 1,self.y + 1])
            
        return move_options
             
board = Board()            
board.setup()
board.pieces()
#pawn.check_active()
board.print()
#print (board.data)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (board.menu):
                pos = pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                #pygame.draw.rect(gameDisplay,white,[display_width/2-40,display_height/2,140,40])
                
                if x > display_width/2-40 and  x < display_width/2-40 + 140:
                    if y > display_height/2 and  y < display_height/2 + 40:
                        board.menu = False
            else:    
                pos = pygame.mouse.get_pos()
                board.check_mouse_click(pos)
         
             
    gameDisplay.fill(white)
    board.draw_board()
    board.win_mess()
    pygame.display.update()
    clock.tick(60)


game_loop()
pygame.quit()
quit()       





