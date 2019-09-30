import java.util.ArrayList;
import java.util.List;

public class GameTree {
    public int flag = -2; // remark of state
    private final int second = -1; //'O'
    public int ppchoice; // people choice about first or second
    private final int first = 1; //'X'
    public int nextplayer; // the next turn
    public float score; // evaluate the state
    public List<GameTree> successors = new ArrayList<GameTree>(); // the tree successors
    public int[] position = new int[2]; // position of current move
    public int[] status = new int[9]; // mark which single board is full
    public int[][][] board, copy; // the state space
    private final int maxdepth = 3; // the max depth can search
    public int depth = 1; // mark the current depth
    public float max = 20;
    public float min = -20;

    // init the node
    public void GameTree(int player, int[][][] state, int[] position, int flag) {
        this.nextplayer = player;
        this.ppchoice = flag;
        this.board = new int[9][3][3];
        this.copy = new int[9][3][3];
        for (int k = 0; k < board.length; k++) {
            for (int i = 0; i < board[1].length; i++) {
                for (int j = 0; j < board[1].length; j++) {
                    this.board[k][i][j] = state[k][i][j];
                    this.copy[k][i][j] = state[k][i][j];
                }
            }
        }
        this.position[0] = position[0];
        this.position[1] = position[1];
        this.flag = judgeend(this);
    }

    //generate the successors process
    List<GameTree> successor(GameTree tttNode ) {
        if (tttNode.flag == 0){
            for (int i = 0; i < tttNode.board.length; i++) {
                createsuc(tttNode, i);
            }
        } else if (tttNode.flag != 2 || tttNode.depth > tttNode.maxdepth) {
            calUtility(tttNode);
            return tttNode.successors;
        } else {
            createsuc(tttNode,tttNode.position[1]);
        }
        eval(tttNode);
        return tttNode.successors;
    }

    //recursively create successors
    void createsuc(GameTree tttNode,int index){
        for (int i = 0; i < tttNode.board[1].length; i++) {
            for (int j = 0; j < tttNode.board[1].length; j++) {
                if (tttNode.board[index][i][j] == 0) {
                    tttNode.copy[index][i][j] = tttNode.nextplayer;
                    GameTree suc = new GameTree();
                    int[] place = new int[2];
                    place[0] = index;
                    place[1] = 3 * i + j;
                    suc.GameTree(-tttNode.nextplayer, tttNode.copy, place, tttNode.ppchoice);
                    suc.depth = tttNode.depth + 1;
                    suc.successor(suc);
                    tttNode.copy[index][i][j] = 0;

                    // ab pruning algorithm
                    if (tttNode.nextplayer == first){
                        if (tttNode.min<suc.score) {
                            tttNode.min = suc.score;
                        } else{
                            continue;
                        }
                    }else{
                        if (tttNode.max>suc.score) {
                            tttNode.max = suc.score;
                        } else{
                            continue;
                        }
                    }
                    tttNode.successors.add(suc);
                }
            }
        }
    }

    // judge the terminal state
    int judgeend(GameTree node) {
        // judge the win state in row
        for (int i = 0; i < node.board[0].length; i++) {
            if (node.board[node.position[0]][i][1] == node.board[node.position[0]][i][2] && node.board[node.position[0]][i][2] == node.board[node.position[0]][i][0]) {
                if (node.board[node.position[0]][i][1] == first) {
                    return 1;
                } else if (node.board[node.position[0]][i][1] == second) {
                    return -1;
                }
            }
        }
        // check lines
        for (int i = 0; i < node.board[0].length; i++) {
            if (node.board[node.position[0]][1][i] == node.board[node.position[0]][2][i] && node.board[node.position[0]][2][i] == node.board[node.position[0]][0][i]) {
                if (node.board[node.position[0]][0][i] == first) {
                    return 1;
                } else if (node.board[node.position[0]][0][i] == second) {
                    return -1;
                }
            }
        }
        // check the diagonal
        if (node.board[node.position[0]][0][0] == node.board[node.position[0]][1][1] && node.board[node.position[0]][1][1] == node.board[node.position[0]][2][2]) {
            if (node.board[node.position[0]][1][1] == first) {
                return 1;
            } else if (node.board[node.position[0]][1][1] == second) {
                return -1;
            }
        }
        if (node.board[node.position[0]][2][0] == node.board[node.position[0]][1][1] && node.board[node.position[0]][1][1] == node.board[node.position[0]][0][2]) {
            if (node.board[node.position[0]][1][1] == first) {
                return 1;
            } else if (node.board[node.position[0]][1][1] == second) {
                return -1;
            }
        }

        // check the draw state
        for (int i = 0; i < node.board[node.position[0]][1].length; i++) {
            for (int j = 0; j < node.board[node.position[0]][1].length; j++) {
                if (node.board[node.position[1]][i][j] == 0) {
                    return 2;
                }
            }
        }
        node.status[node.position[1]] = 1;

        // check is it draw state
        for (int l = 0; l < 9; l++) {
            if (node.status[l] == 0) {
                return 3;
            }
        }
        return 0;
    }

    // evaluate end node score
    boolean end(GameTree node){
        if (node.flag == -1) {
            node.score = -9;
            return true;
        } else if (node.flag == 1) {
            node.score = 9;
            return true;
        } else if (node.flag == 0) {
            node.score = 0;
            return true;
        }
        return false;
    }

    // recursively score every node in tree
    void eval(GameTree node) {
        if (end(node)){
            return;
        } else if (node.nextplayer == 1) {
            float count = -2*9;
            node.score = max(node,count);
        } else {
            float count = 2*9;
            node.score = min(node,count);
        }
        return;
    }

    // minmax algorithm
    float max(GameTree node,float count){
        if (node.successors.size() == 0){
            node.score = calUtility(node);
            return node.score;
        }
        for (GameTree s : node.successors
        ) {
            /*if (s.successors.size() != 0) {
                eval(s);
                //int value = calUtility(node);
                //sum += temp;
            } else {
                s.score = calUtility(s);
            }*/
            if (s.score > count) {
                count = s.score;
            }
        }
        return count;
    }


    float min(GameTree node,float count){
        if (node.successors.size() == 0){
            node.score = calUtility(node);
            return node.score;
        }
        for (GameTree s : node.successors
        ) {
            /*if (s.successors.size() != 0) {
                eval(s);
            } else {
                s.score = calUtility(s);
            }*/
            if (s.score < count) {
                count = s.score;
                //sum += temp;
            }
        }
        return count;
    }

    // evaluate node which is not terminal
    float calUtility(GameTree tttNode) {
        if (end(tttNode)){
            return tttNode.score;
        }
        float count = 0;
        float[] counts = new float[9];
        int[][] tempboard = new int[tttNode.board[1].length][tttNode.board[1].length];

        //refill the blanks with next player move
        for (int k = 0; k < tttNode.board.length; k++) {
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (tttNode.board[k][i][j] == 0) {
                        tempboard[i][j] = tttNode.nextplayer;
                    } else {
                        tempboard[i][j] = tttNode.board[k][i][j];
                    }
                }
            }

            for (int i = 0; i < 3; i++) {
                count += (tempboard[i][0] + tempboard[i][1] + tempboard[i][2]) / 3;
            }
            //calculate the rows value
            for (int i = 0; i < 3; i++) {
                count += (tempboard[0][i] + tempboard[1][i] + tempboard[2][i]) / 3;
            }
            //calculate the lines value
            count += (tempboard[0][0] + tempboard[1][1] + tempboard[2][2]) / 3;
            count += (tempboard[2][0] + tempboard[1][1] + tempboard[0][2]) / 3;

            //refill the blanks with own move
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (tttNode.board[k][i][j] == 0) {
                        tempboard[i][j] = -tttNode.nextplayer;
                    } else {
                        tempboard[i][j] = tttNode.board[k][i][j];
                    }
                }
            }

            //the same count process as above
            for (int i = 0; i < 3; i++) {
                count += (tempboard[i][0] + tempboard[i][1] + tempboard[i][2]) / 3;
            }
            for (int i = 0; i < 3; i++) {
                count += (tempboard[0][i] + tempboard[1][i] + tempboard[2][i]) / 3;
            }

            count += (tempboard[0][0] + tempboard[1][1] + tempboard[2][2]) / 3;
            count += (tempboard[2][0] + tempboard[1][1] + tempboard[0][2]) / 3;
            counts[k] = count;
        }

        //pick the best move
        if (tttNode.nextplayer == first){
            float max = -2*9;
            for (float num:counts
            ) {
                if (num>max){
                    max = num;
                }
            }
            count = max;
        }else{
            float max = 2*9;
            for (float num:counts
            ) {
                if (num<max){
                    max = num;
                }
            }
            count = max;
        }
        return count;
    }
}
