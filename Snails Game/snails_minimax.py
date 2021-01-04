#######################################################################
# Import Libraries
import arcade
import random
import copy
SCREEN_WIDTH=750
SCREEN_HEIGHT=620
ROWS=10              # No of Rows in Board
COLS=10              #No of columns in Board
WIDTH=60              #Width of each grid cell
HEIGHT=60
MARGIN=2               # Margin Between Grid Cells
MAX_LEVEL=7
PREVIOUS=0
TITLE="Snails Game"
#############################################################################
class MyGame(arcade.View):
    
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        self.background = arcade.load_texture("images/bc_image2.jpg")
        
        # initliaze Board
        self.board=[[0 for i in range(ROWS)]for j in range(COLS)]
        self.best_child=[[0 for i in range(ROWS)]for j in range(COLS)]
        # some initialization about coordinates list
        self.board[0][0]=1
        self.board[ROWS-1][COLS-1]=2
        self.slimes=[]
        self.slimes.append(0)
        self.coordinates=[]
        self.coordinates.append([0,0])
        self.coordinates.append([0,0])
        self.coordinates.append([0,0])

       # initialize Player List
        self.player_list=arcade.SpriteList()
        # state of game
        self.state="GameMenu"
        self.win="0"
        #initialzie scores 
        self.score1=0
        self.score2=0
        self.stuck_score1=0
        self.stuck_score2=0
    ##########################################################
    # intilize Grid Cells
    def initializeGrid(self):
        for row in range(ROWS):
            for column in range(COLS):
                x = column * (WIDTH + MARGIN) + (WIDTH // 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT // 2 + MARGIN)
                arcade.draw_rectangle_outline(x,y,WIDTH,HEIGHT,arcade.color.WHITE_SMOKE)
        self.setup()
    ###########################################################
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
        if self.board[ROWS-1][COLS-1]==2:
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

    ###########################################################################    
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
                    """
                    self.white=arcade.Sprite("images/bc_image.jpg",0.027)
                    self.white.center_x=y1*62+30
                    self.white.center_y=x1*62+30
                    self.player_list.append(self.white)
                    """
                    self.player_scaling1=0.7
                    self.splash1 = arcade.Sprite("images/player01_splash.png",self.player_scaling1 )
                    self.splash1.center_x = y1*62+30   #Formula to place splash in center
                    self.splash1.center_y = x1*62+30
                    #self.player1.remove_from_sprite_lists()
                    self.player_list.append(self.splash1)
                
    #############################################################################
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
                    self.player_scaling2=0.7
                    self.splash2 = arcade.Sprite("images/player2_splash.png",self.player_scaling2 )
                    self.splash2.center_x = y1*62+30
                    self.splash2.center_y = x1*62+30
                    self.player_list.append(self.splash2)

    ##############################################################
    # Evaluate Board on basis of backend stored data
    def Evaluate(self,board):
        score=0
        score1=0
        score2=0
        #score2=0
        free_place=0
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==20:
                    score2+=1
                elif board[i][j]==10:
                    score1+=1
                elif board[i][j]==0:
                    free_place+=1
                    #self.win="0"
        self.score2=score2
        self.score1=score1
        # if BOT wins
        if score2>score1 and free_place==0:
        #if score2>=10:
            score=100
            self.win="BOT"
        # if Human Wins
        elif score2<score1 and free_place==0:
            score=-100
            self.win="Player"
        elif score2==score1 and free_place==0:
            score=0
            self.win="Draw"
        #if opponent will cover all free place still he can't win
        elif score2>free_place+score1 and free_place!=0:
            score=100
            self.win="BOT"
        elif score1>free_place+score2 and free_place!=0:
            score=-100
            self.win="Player"
        # If game over
        if self.win != "0":
            self.state="GameOver"
        
        return score
    #########################################################     
    # To determin that now where is player1
    def player1_position(self,board):
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==1:
                    return i,j
    #########################################################
    # To determin That now where is player2
    def player2_position(self,board):
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==2:
                    return i,j   
    ########################################################
    # To Check Wheter Cel is empty
    def IsMoveLeft(self,board):
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j]==0:
                    return True
        return False

    #####################################################################
    def on_draw(self):
        
        # This command has to happen before we start drawing
        arcade.start_render()
        if self.state=="GameMenu":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

            arcade.draw_text("Snails Game",365,350,arcade.color.WHITE,font_size=60,anchor_x="center")
            arcade.draw_text("Human VS Bot",365,300,arcade.color.WHITE,font_size=30,anchor_x="center")
            arcade.draw_text("Press S to Start Game",365,250,arcade.color.WHITE,font_size=20,anchor_x="center")

        elif self.state=="GameOn":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)
            # Put the text on the screen.
            output = f"Score: {self.score2}"
            arcade.draw_text("BOT",650,570,arcade.color.WHITE,font_size=20)
            arcade.draw_text(output, 650, 460, arcade.color.WHITE, 18)
            output = f"Score: {self.score1}"
            arcade.draw_text("HUMAN",650,140,arcade.color.WHITE,font_size=20)
            arcade.draw_text(output, 650, 50, arcade.color.WHITE, 18)
            
            arcade.draw_text("S", 680, 400, arcade.color.WHITE, 35)
            arcade.draw_text("N", 680, 360, arcade.color.WHITE, 35)
            arcade.draw_text("A", 680, 320, arcade.color.WHITE, 35)
            arcade.draw_text("I", 680, 280, arcade.color.WHITE, 35)
            arcade.draw_text("L", 680, 240, arcade.color.WHITE, 35)
            arcade.draw_text("S", 680, 200, arcade.color.WHITE, 35)

            self.initializeGrid()
            self.player_list.draw()
        
        elif self.state=="GameOver":
            arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

            if self.win=="Player":
                arcade.draw_text("Congratulation You Won :)",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=20,anchor_x="center")
            if self.win=="BOT":
                arcade.draw_text("Bot wins :(",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=20,anchor_x="center")
            if self.win=="Draw":
                arcade.draw_text("It's  draw..",365,300,arcade.color.WHITE,font_size=50,anchor_x="center")
                arcade.draw_text("Click to Start Again",365,250,arcade.color.WHITE,font_size=20,anchor_x="center")

    ##############################################################
    def on_key_press(self,key,modifiers):
        if self.state=="GameMenu":
            if key==arcade.key.S:
                self.state="GameOn"

    ##############################################################
    def on_mouse_press(self, x, y, button, modifiers ):
        if self.state=="GameOn":
        
            # Change the x/y screen coordinates to grid coordinates
            column = int(x // (WIDTH + MARGIN))
            row = int(y // (HEIGHT + MARGIN))
            print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

            # corner in the margin and go to a grid location that doesn't exist
            if row < ROWS and column < COLS:
                self.IsLegalMove(row,column)
            res=self.Evaluate(self.board)          #Evaluate board after every turn
            self.BotMove()
            result=self.Evaluate(self.board)
            #self.EvalBoard()           #Evaluate board after every turn
            # if Game over empty the Grid
        elif self.state=="GameOver":
            self.board=[[0 for i in range(ROWS)]for j in range(COLS)]
            self.board[0][0]=1
            self.board[9][9]=2
            
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    self.bc_sprite=arcade.Sprite("images/bc_image.jpg",0.027)
                    self.bc_sprite.center_x = i*62+30   #Formula to place splash in center
                    self.bc_sprite.center_y = j*62+30
                    #self.player1.remove_from_sprite_lists()
                    self.player_list.append(self.bc_sprite)
            
            self.win="0"
            self.score1=0
            self.score2=0
            self.state="GameMenu"

    #############################################################
    #checking is move is valid
    def IsLegalMove(self,row,column):
        
        p_row,p_col=self.player1_position(self.board)        # finding current position of player

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

        #print(self.board)                

    ###############################################################
    # BOT Moves
    def BotMove(self):
        board2=copy.deepcopy(self.board)                 #make copy of original board
        p_row,p_col=self.player2_position(board2)       # find current position of Bot
        temp_row=copy.deepcopy(p_row)
        temp_col=copy.deepcopy(p_col)
        self.coordinates.append([temp_row,temp_col])
        if self.coordinates[-1]==self.coordinates[-3] :
            self.stuck_score1+=1
            self.stuck_score2+=1
        bestVal=-1000
        player=2
        splash=20
        if self.IsMoveLeft(board2):
            ######################
            # hard code some value  #
            if self.score2==1:
                board2[8][8]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            elif self.score2==2:
                board2[7][8]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            elif self.score2==3:
                board2[7][7]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            elif self.score2==4:
                board2[6][7]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            elif self.score2==5:
                board2[6][6]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            elif self.score2==6:
                board2[5][6]=2
                board2[p_row][p_col]=20
                self.best_child=copy.deepcopy(board2)
            # if player stuck in between two postions
            elif self.stuck_score1>0 and ( p_row-1>=0 and p_col-1>=0 and p_row+1<ROWS and p_col+1<COLS) and (board2[p_row-1][p_col]==0 or board2[p_row+1][p_col]==0 or board2[p_row][p_col-1]==0 or board2[p_row][p_col+1]==0):
                #if p_row-1>=0 and p_col-1>=0 and p_row+1<ROWS and p_col+1<COLS:
                #print("stucked")
                if board2[p_row-1][p_col]==0:
                    board2[p_row-1][p_col]=2
                    board2[p_row][p_col]=20
                    #print("bottom")
                    self.best_child=copy.deepcopy(board2)
                    #self.stuck_score=0
                elif board2[p_row+1][p_col]==0:
                    board2[p_row+1][p_col]=2
                    board2[p_row][p_col]=20
                    #print("Top")
                    self.best_child=copy.deepcopy(board2)
                    #self.stuck_score=0
                elif board2[p_row][p_col-1]==0 :
                    board2[p_row][p_col-1]=2
                    board2[p_row][p_col]=20
                    #print("left")
                    self.best_child=copy.deepcopy(board2)
                    #self.stuck_score=0
                elif board2[p_row][p_col+1]==0 :
                    board2[p_row][p_col+1]=2
                    board2[p_row][p_col]=20
                    #print("right")
                    self.best_child=copy.deepcopy(board2)
                self.stuck_score1=0
            # if slimes place arround it and it still stuck
            elif self.stuck_score2>0  and (p_row-1>=0 and p_col-1>=0 and p_row+1<ROWS and p_col+1<COLS) and (board2[p_row-1][p_col]==20 or board2[p_row+1][p_col]==20 or board2[p_row][p_col-1]==20 or board2[p_row][p_col+1]==20):
                #print("STUCK2")
                # if in left are its own slimes
                if board2[p_row][p_col-1]==20:
                    #print("LEFT")
                    column=copy.deepcopy(p_col-1)
                    while(column>0 and board2[p_row][column-1]==20):
                        column-=1
                    board2[p_row][column]=player
                    board2[p_row][p_col]=splash
                    self.best_child=copy.deepcopy(board2)
                # if in right are its own slimes
                if board2[p_row][p_col+1]==20:
                    #print("RIGHT2")
                    column=copy.deepcopy(p_col+1)
                    while(column<COLS-1 and board2[p_row][column+1]==20):
                        column+=1
                    board2[p_row][column]=player
                    board2[p_row][p_col]=splash
                    self.best_child=copy.deepcopy(board2)
                # if in bottom are its own slimes
                if board2[p_row-1][p_col]==20:
                    #print("BOTTOM2")
                    row=copy.deepcopy(p_row-1)
                    while row>0 and board2[row-1][p_col]==splash:
                        row-=1
                    board2[row][p_col]=player
                    board2[p_row][p_col]=splash
                    self.best_child=copy.deepcopy(board2)
                # if in top are its own slimes
                elif board2[p_row+1][p_col]==20:
                    #print("TOP2")
                    row=copy.deepcopy(p_row+1)
                    while row<ROWS-1 and board2[row+1][p_col]==splash:
                        row+=1
                    board2[row][p_col]=player
                    board2[p_row][p_col]=splash
                    self.best_child=copy.deepcopy(board2)
                self.stuck_score2=0
                


            else:

                # Which moves are possible 
                childs=self.ChildBoards(board2,player)
                for i in childs:
                    beta=1000
                    alpha=-1000
                    moveVal=self.MiniMAx(i,0,False,alpha,beta,0)
                    print("Value----->")
                    print(moveVal)
                    # if best value found then previous
                    if moveVal>bestVal:
                        self.best_child=copy.deepcopy(i)
                        bestVal=moveVal
        print("Best value ---->")
        print(bestVal)
        self.board=copy.deepcopy(self.best_child)
        row,col=self.player2_position(self.board)
        self.resync_grid_with_player2(row,col,p_row,p_col)
        #print(self.board)
    

     #####################################################################
    # Minimax
    def MiniMAx(self,board,depth,IsMaxPlayer,alpha,beta,max_level):
        # Evaluate Board
        scores=self.Evaluate(board)
    
        # if Max Level Reached
        if max_level==MAX_LEVEL and self.win=="0":
            return self.Hueristics(board)
        # if Bot Wins
        elif scores==100:
            return scores-depth
        elif scores==-100:
            return scores+depth
        # if Board is Full
        elif self.IsMoveLeft(board)==False:
            return 0
        
        # if Agent Turn
        if IsMaxPlayer :
            player=2
            bestVal=-1000
            if self.IsMoveLeft(board):
                childs=self.ChildBoards(board,player)
                for i in childs:
                    if max_level>MAX_LEVEL:
                        print("Working")
                        break
                    value=self.MiniMAx(i,depth+1,False,alpha,beta,max_level+1)
                    bestVal=max(bestVal,value)
                    
                    alpha=max(alpha,bestVal)
                    if beta<=alpha:
                        break
            return bestVal

        # If Human Turn
        else:
            player=1
            bestVal=1000
            if self.IsMoveLeft(board):
                childs=self.ChildBoards(board,player)
                for i in childs:
                    if max_level>MAX_LEVEL:
                        print("Working2")
                        break
                    value=self.MiniMAx(i,depth+1,True,alpha,beta,max_level+1)
                    bestVal=min(bestVal,value)
                    
                    beta=min(beta,bestVal)
                    if beta<=alpha:
                        break
            return bestVal
    
    #########################################################################
    # Generate Chids
    def ChildBoards(self,temp_board,player):
        #temp_board=copy.deepcopy(board)
        list_boards=[]       # store childs
        if player== 1:
            splash=10
            p_row,p_col=self.player1_position(temp_board)
        elif player==2:
            splash=20
            p_row,p_col=self.player2_position(temp_board)
        
        for i in range(len(temp_board)):
            for j in range(len(temp_board[0])):
                #if empty places found in neighbour 
                if (i==p_row and (j==p_col+1 or j==p_col-1 ) or
                j==p_col and (i==p_row+1 or i==p_row-1) ) and temp_board[i][j]==0:
                    temp_board[i][j]=player
                    temp_board[p_row][p_col]=splash
                    temp=copy.deepcopy(temp_board)
                    temp_board[i][j]=0
                    temp_board[p_row][p_col]=player
                    #print(temp)
                    list_boards.append(temp)
                
                # if Bot move back on its own slime on same row it can move only horizontally in both direction
                if(i==p_row and (j==p_col-1)) and temp_board[i][j]==splash:
                    # if bot moves back in backward (LEFT)
                    column=copy.deepcopy(p_col-1)
                    while(column>0 and temp_board[i][column-1]==splash):
                        column-=1
                    temp_board[i][column]=player
                    temp_board[p_row][p_col]=splash
                    temp=copy.deepcopy(temp_board)
                    temp_board[i][column]=splash
                    temp_board[p_row][p_col]=player
                    list_boards.append(temp)
                    
                    # if bot moves  forward (RIGHT)
                if (i==p_row and j==p_col+1) and temp_board[i][j]==splash:
                    column=copy.deepcopy(p_col+1)
                    while (column<COLS-1 and temp_board[i][column+1]==splash):
                        column+=1
                    temp_board[i][column]=player
                    temp_board[p_row][p_col]=splash
                    temp=copy.deepcopy(temp_board)
                    temp_board[i][column]=splash
                    temp_board[p_row][p_col]=player
                    #print(temp)
                    list_boards.append(temp)
                # if bot moves on its own  slime on same row it can move only vertically in both direction
                if(j==p_col and (i==p_row-1)) and temp_board[i][j]==splash:
                    # if move  back in bottom
                    row=copy.deepcopy(p_row-1)
                    while(row>0 and temp_board[row-1][j]==splash):
                        row-=1
                    temp_board[row][j]=player
                    temp_board[p_row][p_col]=splash
                    temp=copy.deepcopy(temp_board)
                    temp_board[row][j]=splash
                    temp_board[p_row][p_col]=player
                    #print(temp)
                    list_boards.append(temp)
                    
                # if bot move back in Top
                if (j==p_col and i==p_row+1) and temp_board[i][j]==splash:
                    row=copy.deepcopy(p_row+1)
                    while (row<ROWS-1 and temp_board[row+1][j]==splash):
                        row+=1
                    temp_board[row][j]=player
                    temp_board[p_row][p_col]=splash
                    temp=copy.deepcopy(temp_board)
                    temp_board[row][j]=splash
                    temp_board[p_row][p_col]=player
                    #print(temp)
                    list_boards.append(temp)
                
                
        return list_boards     # return Childs
    ######################################################################
    # Count Visited box by agents
    def AI_visited(self,board,splash):
        counter=0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j]==splash:
                    counter=counter+1
        return counter+1

    ######################################################################
    ####  Heuristic Function     #######################################
    def Hueristics(self,board):
        winning_chances=0
        previous=self.slimes.pop()   # previously visited slimes
        # count no of visited slimes
        agent_slimes=self.AI_visited(board,20)    # now slimes
        # If snails move back on its slimes
        if agent_slimes<=previous:      # if no slime increased
            winning_chances+=agent_slimes

        
        self.slimes.append(agent_slimes)    #append updated slimes
        if agent_slimes>previous:
            winning_chances+=agent_slimes+10  # if slimes are more than previous
            
        #current postion of both player
        p_row,p_col=self.player2_position(board)
        p1_row,p1_col=self.player1_position(board)

        """
        # Check no of empty boxes arroud agent
        if p_row+1<ROWS and board[p_row+1][p_col]==0:
            winning_chances+=1
        if p_row-1>=0 and board[p_row-1][p_col]==0:
            winning_chances+=1
        if p_col+1<COLS and board[p_row][p_col+1]==0:
            winning_chances+=1
        if p_col-1>=0 and board[p_row][p_col-1]==0:
            winning_chances+=1
        """
        

        #################################################################
        #First Technique
        #Count No of Empty boxes in all directions
        # empty boxes in left
        if(p_col-1>=0) and board[p_row][p_col-1]==0:
           
            #column=copy.deepcopy(p_col-1)
            column=p_col-1
            #print(f"BEFORE col-1:{p_col-1}")
            while(column>=0 and board[p_row][column]==0):
                column-=1
                winning_chances+=1
            #print(f"AFTER: {p_col-1}")
        # empty boxes in right      
        if p_col+1<COLS and board[p_row][p_col+1]==0:
            # if player click forward (RIGHT)
            #column=copy.deepcopy(p_col+1)
            column=p_col+1
            
            while (column<COLS and board[p_row][column]==0):
                column+=1
                winning_chances+=1
        #empty boxes in Bottom   
        if (p_row-1>=0) and board[p_row-1][p_col]==0:
            #row=copy.deepcopy(p_row-1)
            row=p_row-1
            while(row>=0 and board[row][p_col]==0):
                row-=1
                winning_chances+=1
        if p_row+1<COLS and board[p_row+1][p_col]==0:
            #row=copy.deepcopy(p_row+1)
            row=p_row+1
            while(row<COLS and board[row][p_col]==0):
                row+=1
                winning_chances+=1
        
        ###################################################
        # If bot covered three sides of Player
        if p1_col+1<len(board) and p1_col-1>=0 and p1_row+1<len(board) and p1_row-1>=0 :
            if (board[p1_row][p1_col-1]==20 or board[p1_row][p1_col-1]==2) and (board[p1_row][p1_col+1]==20 or board[p1_row][p1_col+1]==2) and (board[p1_row+1][p1_col]==20 or board[p1_row+1][p1_col]==2):
                winning_chances+=10
                #return 80

       
        ##################################################
        # close to opponent
        if p_row+1<ROWS and board[p_row+1][p_col]==1:
            winning_chances+=5
        if p_row-1>=0 and board[p_row-1][p_col]==1:
            winning_chances+=5
        if p_col+1<COLS and board[p_row][p_col+1]==1:
            winning_chances+=5
        if p_col-1>=0 and board[p_row][p_col-1]==1:
            winning_chances+=5
        
       
        """
        #Count No of Empty boxes in all directions
        if(p_col-1>=0) and board[p_row][p_col-1]==0:
            # if player click back in backward (LEFT)
            column=copy.deepcopy(p_col-1)
            while(column>=0 and board[p_row][column]==0):
                column-=1
                lefts+=1
        directions.append(lefts)
        if p_col+1<COLS and board[p_row][p_col+1]==0:
            # if player click forward (RIGHT)
            column=copy.deepcopy(p_col+1)
            while (column<COLS and board[p_row][column]==0):
                column+=1
                rights+=1
        directions.append(rights)
        if (p_row-1>=0) and board[p_row-1][p_col]==0:
            row=copy.deepcopy(p_row-1)
            while(row>=0 and board[row][p_col]==0):
                row-=1
                bottoms+=1
        directions.append(bottoms)
        if p_row+1<COLS and board[p_row+1][p_col]==0:
            row=copy.deepcopy(p_row+1)
            while(row<COLS and board[row][p_col]==0):
                row+=1
                tops+=1
        directions.append(tops)
        #print("Dirctions")
        #print(directions)
        max_direction=max(directions)
        print("Max")
        print(max_direction)
        winning_chances+=max_direction
        """

        ############################################
        # 3rd Techniques
        range_min=(len(board)/2)-1
        range_max=(len(board)/2)+1
        if range_min<=p_row<=range_max:
            if range_min<=p_col<=range_max:
                #print("********* Centeral Region*************")
                winning_chances+=10
        
        #4th Condition
        #player_slimes=self.AI_visited(board,10)
        #winning_chances-=player_slimes
        
        return winning_chances
        



        


########################################################
#######################################################3
def main():
    window=arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    arcade.run()
    #game_view.setup()
 

if __name__=="__main__":
     main()