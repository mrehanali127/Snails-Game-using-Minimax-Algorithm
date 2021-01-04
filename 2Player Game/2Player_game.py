import arcade
import random
import copy
SCREEN_WIDTH=750
SCREEN_HEIGHT=620
ROWS=10            # No of Rows in Board
COLS=10            #No of columns in Board
WIDTH=60           #Width of each grid cell
HEIGHT=60
MARGIN=2          # Margin Between Grid Cells
TITLE="2 Player Game"

class MyGame(arcade.View):
    
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        self.background = arcade.load_texture("images/bc_image2.jpg")

        # initliaze Board
        self.board=[[0 for i in range(ROWS)]for j in range(COLS)]
        self.board[0][0]=1
        self.board[9][9]=2
        print(self.board)
        #initliazi player_list
        self.player_list=arcade.SpriteList()
        self.bc_sprite=arcade.SpriteList()
        # scores
        self.score1=0
        self.score2=0
        
        # for takin turn
        self.counter=1
        # state of game
        self.state="GameMenu"
        self.win="0"
        
            
    # intilize Grid Cells
    def initializeCells(self):
        for row in range(ROWS):
            for column in range(COLS):
                x = column * (WIDTH + MARGIN) + (WIDTH // 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT // 2 + MARGIN)
                arcade.draw_rectangle_outline(x,y,WIDTH,HEIGHT,arcade.color.WHITE_SMOKE)
        self.setup()

    # place sprites on initial position   
    def setup(self):
        #player 1
        if self.board[0][0]==1:
            self.player_scaling1=0.10
            self.player_sprite1 = arcade.Sprite("images/player1.png",self.player_scaling1 )
            self.player_sprite1.center_x = 30
            self.player_sprite1.center_y = 30
            self.player_list.append(self.player_sprite1)
        # player2
        if self.board[9][9]==2:
            self.player_scaling2=0.10
            self.player_sprite2 = arcade.Sprite("images/player2.png",self.player_scaling2 )
            self.player_sprite2.center_x = 590
            self.player_sprite2.center_y = 590
            self.player_list.append(self.player_sprite2)
        # Side wale sprite
        self.player_scaling1=0.12
        self.player_sprite1 = arcade.Sprite("images/player1.png",self.player_scaling1 )
        self.player_sprite1.center_x = 680
        self.player_sprite1.center_y = 110
        self.player_list.append(self.player_sprite1)
        # side wale sprite
        self.player_scaling2=0.12
        self.player_sprite2 = arcade.Sprite("images/player2.png",self.player_scaling2 )
        self.player_sprite2.center_x = 680
        self.player_sprite2.center_y = 530
        self.player_list.append(self.player_sprite2)

        
    # when first player take turn
    def resync_grid_with_player1(self,x,y,x1,y1):
        for row in range(ROWS):
            for column in range(COLS):
                # Change in Frontend on basis of Backend
                if self.board[row][column]==1:
                    self.player_scale1=0.10
                    self.player1 = arcade.Sprite("images/player1.png",self.player_scale1 )
                    self.player1.center_x = y*62+30       #formula to place sprite in center of grid cell
                    self.player1.center_y = x*62+30
                    self.player_list.append(self.player1)
                if self.board[row][column]==10:
                    self.player_scaling1=0.8
                    self.splash1 = arcade.Sprite("images/player01_splash.png",self.player_scaling1 )
                    self.splash1.center_x = y1*62+30   #Formula to place splash in center
                    self.splash1.center_y = x1*62+30
                    #self.player1.remove_from_sprite_lists()
                    self.player_list.append(self.splash1)
                
    
    # when second player take turn
    def resync_grid_with_player2(self,x,y,x1,y1):
        for row in range(ROWS):
            for column in range(COLS):
                if self.board[row][column]==2:
                    self.player_scale2=0.10
                    self.player2 = arcade.Sprite("images/player2.png",self.player_scale2 )
                    self.player2.center_x = y*62+30
                    self.player2.center_y = x*62+30
                    self.player_list.append(self.player2)

                if self.board[row][column]==20:
                    self.player_scaling2=0.8
                    self.splash2 = arcade.Sprite("images/player2_splash.png",self.player_scaling2 )
                    self.splash2.center_x = y1*62+30
                    self.splash2.center_y = x1*62+30
                    self.player_list.append(self.splash2)
                
    # Evaluate Board on basis of backend stored data
    def EvalBoard(self):
        score1=0
        score2=0
        free_place=0
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j]==10:
                    score1+=1
                elif self.board[i][j]==20:
                    score2+=1
                if self.board[i][j]==0:
                    free_place+=1
                    self.win="0"
        self.score1=score1
        self.score2=score2
        #if score1>score2:
        if score1>score2 and free_place==0:
        #if score1>10:
            self.win="Player1"
        elif score2>score1 and free_place==0:
            self.win="Player2"
        elif score1==score2 and free_place==0:
            self.win="Draw"
        
        
    
        if self.win != "0":
            self.state="GameOver"
          
    # To determin that now where is player1
    def player1_position(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j]==1:
                    return i,j
    
    # To determin That now where is player2
    def player2_position(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j]==2:
                    return i,j   

    
    def on_draw(self):
        
        # This command has to happen before we start drawing
        arcade.start_render()
        if self.state=="GameMenu":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

            arcade.draw_text("Snails Game",365,300,arcade.color.WHITE,font_size=60,anchor_x="center")
            arcade.draw_text("Human VS Bot",365,250,arcade.color.WHITE,font_size=30,anchor_x="center")
            arcade.draw_text("Clik on adjacent boxes to move",365,200,arcade.color.WHITE,font_size=20,anchor_x="center")
            arcade.draw_text("Press S to Start Game",365,100,arcade.color.WHITE,font_size=20,anchor_x="center")

        elif self.state=="GameOn":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)
            output = f"Score: {self.score2}"
            arcade.draw_text("Player 2",650,570,arcade.color.WHITE,font_size=20)
            arcade.draw_text(output, 650, 460, arcade.color.WHITE, 18)
            output = f"Score: {self.score1}"
            arcade.draw_text("Player 1",650,140,arcade.color.WHITE,font_size=20)
            arcade.draw_text(output, 650, 50, arcade.color.WHITE, 18)
            
            arcade.draw_text("S", 680, 400, arcade.color.WHITE, 35)
            arcade.draw_text("N", 680, 360, arcade.color.WHITE, 35)
            arcade.draw_text("A", 680, 320, arcade.color.WHITE, 35)
            arcade.draw_text("I", 680, 280, arcade.color.WHITE, 35)
            arcade.draw_text("L", 680, 240, arcade.color.WHITE, 35)
            arcade.draw_text("S", 680, 200, arcade.color.WHITE, 35)
            self.initializeCells()
            self.player_list.draw()
        
        elif self.state=="GameOver":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

            if self.win=="Player1":
                arcade.draw_text("Player1 Won :)",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=30,anchor_x="center")
            if self.win=="Player2":
                arcade.draw_text("Player2 Won :(",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=30,anchor_x="center")
            if self.win=="Draw":
                arcade.draw_text("It's  draw..",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=30,anchor_x="center")


    def on_key_press(self,key,modifiers):
        if self.state=="GameMenu":
            if key==arcade.key.S:
                self.state="GameOn"


    def on_mouse_press(self, x, y, button, modifiers ):
        if self.state=="GameOn":
            # Change the x/y screen coordinates to grid coordinates
            column = int(x // (WIDTH + MARGIN))
            row = int(y // (HEIGHT + MARGIN))
            print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

            # corner in the margin and go to a grid location that doesn't exist
            if row < ROWS and column < COLS:
                # which turn was it
                #turn=random.randint(1,2)
                if self.counter % 2==0:
                    turn=2
                else:
                    turn=1
                self.counter+=1
                
                self.IsLegalMove(row,column,turn)
        
        elif self.state=="GameOver":
            self.board=[[0 for i in range(ROWS)]for j in range(COLS)]
            self.board[0][0]=1
            self.board[9][9]=2
            self.win="0"
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    self.bc_sprite=arcade.Sprite("images/bc_image.jpg",0.027)
                    self.bc_sprite.center_x = i*62+30   #Formula to place splash in center
                    self.bc_sprite.center_y = j*62+30
                    #self.player1.remove_from_sprite_lists()
                    self.player_list.append(self.bc_sprite)
            self.score1=0
            self.score2=0
            self.state="GameMenu"
            
        
    
    #checking is move is valid
    def IsLegalMove(self,row,column,turn):
        if turn==1:
            #childs=self.ChildBoards(turn)
            #print(childs)
            p_row,p_col=self.player1_position()        # finding current position of player

            # Following If condition is for that player can move only adjacent to it either vertically of horizontally
            if (row==p_row and (column==p_col+1 or column==p_col-1 ) or
            column==p_col and (row==p_row+1 or row==p_row-1) ) and self.board[row][column]==0:
                    
                self.board[row][column]=1
                self.board[p_row][p_col]=10
                # update position in frontend
                self.resync_grid_with_player1(row,column,p_row,p_col)
            # if player click on his slime on same row it can move only horizontally in both direction
            if(row==p_row and (column==p_col-1 or column==p_col+1 )) and self.board[row][column]==10:
                # if player click back in backward (LEFT)
                if column==p_col-1:
                    while(column>0 and self.board[row][column-1]==10):
                        column-=1
                # if player click forward (RIGHT)
                elif column==p_col+1:
                    while (column<COLS-1 and self.board[row][column+1]==10):
                        column+=1
                self.board[row][column]=1
                self.board[p_row][p_col]=10
                #update frontend
                self.resync_grid_with_player1(row,column,p_row,p_col)
            # if player click on his slime in same column it can move only vertically in both direction
            if((row==p_row-1 or row==p_row+1) and column==p_col) and self.board[row][column]==10:
                # if player click downward
                if row==p_row-1:
                    while(row>0 and self.board[row-1][column]==10):
                        row-=1
                # if player click upward
                elif row==p_row+1:
                    while (row<ROWS-1 and self.board[row+1][column]==10):
                        row+=1

                self.board[row][column]=1
                self.board[p_row][p_col]=10
                self.resync_grid_with_player1(row,column,p_row,p_col)

        # if player 2 has turn
        elif turn==2:
            p_row,p_col=self.player2_position()
            if (row==p_row and (column==p_col+1 or column==p_col-1 ) or
            column==p_col and (row==p_row+1 or row==p_row-1) ) and self.board[row][column]==0:
                    
                self.board[row][column]=2

                self.board[p_row][p_col]=20
                self.resync_grid_with_player2(row,column,p_row,p_col)
            # if player click on his slime on same row it can move only horizontally in both direction
            if(row==p_row and (column==p_col-1 or column==p_col+1 )) and self.board[row][column]==20:
                # if player click back in backward (LEFT)
                if column==p_col-1:
                    while(column>=0 and self.board[row][column-1]==20):
                        column-=1
                # if player click forward (RIGHT)
                elif column==p_col+1:
                    while (column<COLS-1 and self.board[row][column+1]==20):
                        column+=1
                self.board[row][column]=2
                self.board[p_row][p_col]=20
                #update frontend
                self.resync_grid_with_player2(row,column,p_row,p_col)
            # if player click on his slime in same column it can move only vertically in both direction
            if((row==p_row-1 or row==p_row+1) and column==p_col) and self.board[row][column]==20:
                # if player click downward
                if row==p_row-1:
                    while(row>=0 and self.board[row-1][column]==20):
                        row-=1
                # if player click upward
                elif row==p_row+1:
                    while (row<ROWS-1 and self.board[row+1][column]==20):
                        row+=1

                self.board[row][column]=2
                self.board[p_row][p_col]=20
                self.resync_grid_with_player2(row,column,p_row,p_col)

            
        print(self.board)                
        self.EvalBoard()           #Evaluate board after every turn


    def ChildBoards(self,turn):
        if turn==1:
            sign=1
            splash=10
            P_row,P_col=self.player1_position()
        else:
            sign=2
            splash=20
            P_row,P_col=self.player2_position()
        temp_board=copy.deepcopy(self.board)
        list_boards=[]
        counter=0
        for i in range(len(temp_board)):
            for j in range(len(temp_board[0])):
                if  temp_board[i][j]==0:
                    counter+=1
                
        for i in range(len(temp_board)):
            for j in range(len(temp_board[0])):
                if (i==P_row and (j==P_col+1 or j==P_col-1 ) or
                j==P_col and (i==P_row+1 or i==P_row-1) ) and temp_board[i][j]==0:
                    temp_board[P_row][P_col]=splash
                    temp_board[i][j]=sign
                    temp=copy.deepcopy(temp_board)
                    temp_board[i][j]=0
                    temp_board[P_row][P_col]=sign
                    list_boards.append(temp)
            
    
        return list_boards


def main():
    window=arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    arcade.run()
    #game_view.setup()
 

if __name__=="__main__":
     main()