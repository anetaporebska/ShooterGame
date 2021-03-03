from Field import Field


class Board:
    def __init__(self,width:int,height:int,mapVersion:int):
        self.height=height
        self.width=width
        self.board=[]
        for i in range(width):
            self.board.append([])
#        TODO: wygenerowanie najlepiej paru plansz, w sensie wstawienie scian
        if(mapVersion == 1):
            for row in self.board:
                for j in range(height):
                    row.append(Field(False))
        elif(mapVersion==2):
            pass
