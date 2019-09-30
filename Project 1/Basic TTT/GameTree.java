import java.util.ArrayList;
import java.util.List;

public class GameTree {
    //int count = 0;
    int flag = -2;// flag is used to judge end
    private final int second = -1;// second means 'O',value is -1
    private int ppchoice;// means people choice about 'X'=1 or 'O'=0
    private final int first = 1;
    public int nextplayer; //means the next player is which
    public int score ; // means the value of the heuristic function,help computer to make move
    List<GameTree> successors = new ArrayList<GameTree>(); // all the possible move of the next
    public int position;  // the position of current move
    public int[][] board,copy ; // board is used to save the state of board, copy is used to handle search tree


    public void GameTree( int player,int[][]board,int position,int flag) {
        //init the whole node
        this.nextplayer = player;
        this.ppchoice = flag;
        this.board = new int[3][3];
        this.copy = new int[3][3];
        // input the board state into the node
        for(int i=0;i<board.length;i++) {
            for (int j = 0; j < board.length; j++) {
                this.board[i][j] = board[i][j];
                this.copy[i][j] = board[i][j];
            }
        }
        this.position = position;
        this.flag = judgeend(this); // use judgeend function to judge if it is terminal node
    }

    // generate the search tree
    List<GameTree> successor(GameTree tttNode){
        if(tttNode.flag!=2){
            return tttNode.successors;
        }else {
            for(int i=0;i<tttNode.board.length;i++){
                for (int j=0;j<tttNode.board.length;j++){
                    if(tttNode.board[i][j]==0){
                        tttNode.copy[i][j] = tttNode.nextplayer;
                        GameTree suc = new GameTree();
                        suc.GameTree(-tttNode.nextplayer,tttNode.copy,3*i+j,tttNode.ppchoice);
                        suc.successor(suc);
                        tttNode.successors.add(suc);
                        tttNode.copy[i][j] = 0;
                    }
                }
            }
            return tttNode.successors;
        }
    }


    int judgeend(GameTree node){
        // judge the win state in row
        for(int i = 0;i < node.board[0].length; i++) {
            if (node.board[i][1] == node.board[i][2]&&node.board[i][2]==node.board[i][0]) {
                if (node.board[i][1] == first) {
                    return 1;
                }else if(node.board[i][1] == second){
                    return -1;
                }
            }
        }
        // check lines
        for(int i = 0;i < node.board[0].length; i++){
            if(node.board[1][i]==node.board[2][i]&&node.board[2][i]==node.board[0][i]){
                if(node.board[0][i] == first){
                    return 1;
            }else if(node.board[0][i] == second) {
                    return -1;
                }
            }
        }
        // check the diagonal
        if(node.board[0][0]==node.board[1][1]&&node.board[1][1]==node.board[2][2]){
            if(node.board[1][1]==first) {
                return 1;
            }else if(node.board[1][1]==second){
                return -1;
            }
        }else if(node.board[2][0]==node.board[1][1]&&node.board[1][1]==node.board[0][2]){
            if(node.board[1][1]==first) {
                return 1;
            }else if (this.board[1][1]==second){
                return -1;
            }
        }

        // check if it is the draw state
        for (int i = 0; i < node.board.length; i++) {
            for (int j = 0; j < node.board[1].length; j++) {
                if (node.board[i][j] == 0) {
                    return 2;
                }
            }
        }
        return 0;
    }

    // heuristic function
    int eval(GameTree node) {
        // terminal state directly get score
        if (node.flag == -1) {
            node.score = -1;
            return -1;
        }
        if (node.flag == 1) {
            node.score = 1;
            return 1;
        }
        if (node.flag == 0) {
            node.score = 0;
            return 0;
        }

        //minmax function to get best move
        if (node.nextplayer == 1) {
            int count = -2;
            for (GameTree s : node.successors
            ) {
                eval(s); // recursively deepen into the terminal node
                //minmax algorithm
                if (s.score > count) {
                    count = s.score;
                }
            }
            node.score = count;
        } else {
            int count = 2;
            for (GameTree s : node.successors
            ) {
                eval(s); // recursively deepen into the terminal node
                //minmax algorithm
                if (s.score < count) {
                    count = s.score;
                }
            }
            node.score = count;
        }
        return node.score;
    }
}
