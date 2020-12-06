import sys
class Node(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x
    
    def __str__(self):
        return "[%d, %d]"%(y,x)

class NodeAndScore(object):
    def __init__(self, node, score):
        self.node = node
        self.score = score

class Game(object):
    def __init__(self):
        self.nodes = []
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.root_childs_score = []
        self.up_to_depth = -1
    
    def evaluate_board(self):
        score = 0
        for y in xrange(0,3):
            blank_nodes = 0
            x_nodes = 0
            o_nodes = 0
            for x in xrange(0,3):
                if self.board[y][x] == 0:
                    blank_nodes += 1
                elif self.board[y][x] == 1:
                    x_nodes += 1
                else:
                    o_nodes += 1
            score += self.evaluate_score(x_nodes, o_nodes)
        
        for x in xrange(0,3):
            blank_nodes = 0
            x_nodes = 0
            o_nodes = 0
            for y in xrange(0,3):
                if self.board[y][x] == 0:
                    blank_nodes += 1
                elif self.board[y][x] == 1:
                    x_nodes += 1
                else:
                    o_nodes += 1
            score += self.evaluate_score(x_nodes, o_nodes)
        
        for x in xrange(0,3):
            y = x
            blank_nodes = 0
            x_nodes = 0
            o_nodes = 0
            if self.board[y][x] == 0:
                blank_nodes += 1
            elif self.board[y][x] == 1:
                x_nodes += 1
            else:
                o_nodes += 1
            score += self.evaluate_score(x_nodes, o_nodes)
        
        y = 0
        for x in xrange(2,-1,-1):
            blank_nodes = 0
            x_nodes = 0
            o_nodes = 0
            if self.board[y][x] == 0:
                blank_nodes += 1
            elif self.board[y][x] == 1:
                x_nodes += 1
            else:
                o_nodes += 1
            score += self.evaluate_score(x_nodes, o_nodes)
            y+=1
        
        return score
    
    def is_X_won(self):
        if (self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] == 1) or (self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] == 1):
            return True
        for i in xrange(0,3):
            if (self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and self.board[i][0] == 1) or (self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and self.board[0][i] == 1):
                return True
        return False
    
    def is_O_won(self):
        if (self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] == 2) or (self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] == 2):
            return True
        for i in xrange(0,3):
            if (self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and self.board[i][0] == 2) or (self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and self.board[0][i] == 2):
                return True
        return False
    
    def get_avail_states(self):
        avail_nodes = []
        for y in xrange(0,3):
            for x in xrange(0,3):
                if self.board[y][x] == 0:
                    avail_nodes.append(Node(y,x))
        return avail_nodes


    def is_game_over(self):
        return (self.is_X_won() or self.is_O_won() or len(self.get_avail_states())==0)

    def display_board(self):
        for i in xrange(0,25):   
            print("")
        for i in xrange(0,3):
            for j in xrange(0,3):
                if self.board[i][j] == 2:
                    sys.stdout.write("O ")
                elif self.board[i][j] == 1:
                    sys.stdout.write("X ")
                else:
                    sys.stdout.write("_ ")

            print("")
    
    def place_a_piece(self, node, player):
        #1 = X = CPU
        #2 = O = Player
        self.board[node.y][node.x] = player

    
    def take_input(self):
        y = int(raw_input("New Y coord: "))
        x = int(raw_input("New X coord: "))
        n = Node(y,x)
        self.place_a_piece(n,2)
    
    def alpha_beta_pruning(self, alpha, beta, depth, turn):
        if beta<=alpha:
            print("Pruning at depth %d"%(depth))
            if turn == 1:
                return sys.maxint
            else:
                return -(sys.maxint-1)
        
        if depth == self.up_to_depth or self.is_game_over():
            return self.evaluate_board()
        
        nodes_available = self.get_avail_states()
        if len(nodes_available)==0:
            return 0
        if depth==0:
            self.root_childs_score = []
        max_val = -(sys.maxint-1)
        min_val = sys.maxint
        for n in nodes_available:
            current_score = 0
            if turn == 1:
                self.place_a_piece(n, 1)
                current_score = self.alpha_beta_pruning(alpha, beta, depth+1, 2)
                max_val = max(max_val, current_score)

                alpha = max(current_score, alpha)
                if depth == 0:
                    self.root_childs_score.append(NodeAndScore(n, current_score))
            elif turn == 2:
                self.place_a_piece(n, 2)
                current_score = self.alpha_beta_pruning(alpha, beta, depth+1, 1)
                min_val = min(min_val, current_score)

                beta = min(current_score, beta)
            self.board[n.y][n.x] = 0
            if current_score == sys.maxint or current_score == -(sys.maxint-1):
                break
        
        return max_val if turn == 1 else min_val
    
    def generate_move_for_CPU(self):
        MAX = -100000
        best = None
        for n in self.root_childs_score:
            if MAX < n.score:
                MAX = n.score
                best = n
        
        return best.node

    
    def evaluate_score(self, x_nodes, o_nodes):
        score = 0
        if x_nodes == 3:
            score = 100
        elif x_nodes == 2 and o_nodes == 0:
            score = 10
        elif x_nodes == 1 and o_nodes == 0:
            score = 1
        elif o_nodes == 3:
            score = -100
        elif o_nodes == 2 and x_nodes == 0:
            score = -10
        elif o_nodes == 1 and x_nodes == 0:
            score = -1

        return score





if __name__ == "__main__":
    g = Game()
    
    while not g.is_game_over():
        g.display_board()
        g.take_input()
        if g.is_game_over():
            break
        
        g.alpha_beta_pruning(-(sys.maxint-1), sys.maxint, 0, 1)
        g.place_a_piece(g.generate_move_for_CPU(), 1)
        g.display_board()
        if g.is_game_over():
            break
    
    if g.is_O_won():
        print("Congrats")
    elif g.is_X_won():
        print("Sed")
    else:
        print("Tie")

