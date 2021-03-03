class Field:
    def __init__(self,isWall):
        #TODO ?: pole FieldType mozna sie niby pobawic np w wode, 
        #przechodzenie przez ktora by spowalnialo, albo jakies rozne kolory plansz?
        self.isWall=isWall
        self.booster=None
        self.player=None
    def isEmpty(self):
        if(not self.isWall and self.booster==None and self.player==None):
            return True
        return False
    def is_wall(self):
        return self.isWall
    def is_booster(self):
        return self.booster==None
    def is_player(self):
        return self.player==None
    #TODO: Stworzenie tekstur, no na pewno zrobiłbym coś na gracza i boostery, może ściany i podłoże