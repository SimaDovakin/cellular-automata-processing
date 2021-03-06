
STOP = False

DEAD_CELL_COLOR = (243, 243, 197)
ALIVE_CELL_COLOR = (79, 189, 112)
DEAD_CELL_HOVER_COLOR = (227, 227, 118)
ALIVE_CELL_HOVER_COLOR = (0, 144, 46)

class Cell:
    
    def __init__(self, pos, size_, is_alive, generation, alive_neighbs=0):
        self.pos = pos
        self.size_ = size_
        self.alive_neighbs = alive_neighbs
        self.is_alive = is_alive
        self.generation = generation
        
    def count_neighbors(self, cell_list):
        
        rows = len(cell_list)
        cols = len(cell_list[0])
        
        rows_range = (self.pos[0] - 1, self.pos[0], self.pos[0] + 1)
        cols_range = (self.pos[1] - 1, self.pos[1], self.pos[1] + 1)
        
        for i in rows_range:
            for j in cols_range:
                if i == self.pos[0] and j == self.pos[1]:
                    continue
                if cell_list[i % rows][j % cols].is_alive:
                    self.alive_neighbs += 1
                    
                    
    def update(self):
        
        if self.is_alive:
            if self.alive_neighbs < 2 or self.alive_neighbs > 3:
                self.is_alive = False
                self.generation = 0
            else:
                self.generation += 1
        else:
            if self.alive_neighbs == 3:
                self.is_alive = True
                self.generation = 1
            
    def show(self):
        
        if self.is_alive:
            fill(*ALIVE_CELL_COLOR)
        else:
            fill(*DEAD_CELL_COLOR)
            
        if int(mouseX / CELL_SIZE) == self.pos[0] and int(mouseY / CELL_SIZE) == self.pos[1]:
            if self.is_alive:
                fill(*ALIVE_CELL_HOVER_COLOR)
            else:
                fill(*DEAD_CELL_HOVER_COLOR)
                       
        rect(self.pos[0] * self.size_, self.pos[1] * self.size_, self.size_, self.size_)    
        noStroke()
        
        

def setup():
    
    global CELL_LIST, NEW_CELL_LIST, CELL_SIZE
    
    CELL_LIST = []
    NEW_CELL_LIST = []
    
    CELL_SIZE = 10
    
    size(1000, 1000)
    noStroke()
    
    for i in range(height/CELL_SIZE):
        tmp_list = []
        for j in range(width/CELL_SIZE):
            is_alive=True if random(0, 1) > 0.9 else False
            generation = 1 if is_alive else 0
            cell = Cell((i, j), CELL_SIZE, is_alive, generation, alive_neighbs=0)
            tmp_list.append(cell)
            
        CELL_LIST.append(tmp_list)
        
    background(*DEAD_CELL_COLOR)
    
    for i in CELL_LIST:
        for cell in i:
            cell.show()
            

def draw():
    
    global CELL_LIST, NEW_CELL_LIST, STOP
    
    background(*DEAD_CELL_COLOR)
    
    frameRate(10)
    
    if not STOP:
    
        for lst in CELL_LIST:
            tmp_lst = []
            for cell in lst:
                new_cell = Cell(cell.pos, cell.size_, cell.is_alive, cell.generation, 0)
                new_cell.count_neighbors(CELL_LIST)
                new_cell.update()
                tmp_lst.append(new_cell)
                
            NEW_CELL_LIST.append(tmp_lst)
            
        CELL_LIST, NEW_CELL_LIST = NEW_CELL_LIST, []
    
    for lst in CELL_LIST:
        for cell in lst:
            cell.show()
            

def keyReleased():

    global STOP, CELL_LIST
    
    if keyCode == 32: # space
        STOP = True if not STOP else False
    elif keyCode == 8: # backspace
        # kill all cells
        for row in CELL_LIST:
            for cell in row:
                cell.is_alive = False
    
def mousePressed():
    global CELL_LIST, CELL_SIZE
    
    if mouseButton == LEFT:
        
        j = mouseY // CELL_SIZE
        i = mouseX // CELL_SIZE
        
        CELL_LIST[i][j].is_alive = True if not CELL_LIST[i][j].is_alive else False
                                            
    
