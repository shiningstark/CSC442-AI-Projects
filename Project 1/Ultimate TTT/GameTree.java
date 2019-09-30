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
    public int[][][] board, copy; // the state space
    private final int maxdepth = 2; // the max depth can search
    public int depth = 1; // mark the current depth
    public float max = 2000;
    public float min = -2000;

    // init the node
    public void GameTree(int player, int[][][] state, int[] position, int flag) {
        this.nextplayer = player;
        this.ppchoice = flag;
        this.board = new int[4][4][4];
        this.copy = new int[4][4][4];
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
    List<GameTree> successor(GameTree tttNode) {
        if (tttNode.flag != 2 || tttNode.depth > tttNode.maxdepth) {
            calUtility(tttNode);
            return tttNode.successors;
        } else {
            createsuc(tttNode);
        }
        eval(tttNode);
        return tttNode.successors;
    }

    //recursively create successors
    void createsuc(GameTree tttNode) {
        for (int k = 0; k < tttNode.board.length; k++) {
            for (int i = 0; i < tttNode.board[1].length; i++) {
                for (int j = 0; j < tttNode.board[1].length; j++) {
                    if (tttNode.board[k][i][j] == 0) {
                        tttNode.copy[k][i][j] = tttNode.nextplayer;
                        GameTree suc = new GameTree();
                        int[] place = new int[2];
                        place[0] = k;
                        place[1] = 4 * i + j;
                        suc.GameTree(-tttNode.nextplayer, tttNode.copy, place, tttNode.ppchoice);
                        suc.depth = tttNode.depth + 1;
                        suc.successor(suc);
                        tttNode.copy[k][i][j] = 0;

                        // ab pruning algorithm
                        if (tttNode.nextplayer == first) {
                            if (tttNode.min < suc.score) {
                                tttNode.min = suc.score;
                            } else {
                                continue;
                            }
                        } else {
                            if (tttNode.max > suc.score) {
                                tttNode.max = suc.score;
                            } else {
                                continue;
                            }
                        }
                        tttNode.successors.add(suc);
                    }
                }
            }
        }
    }

    // judge the terminal state
    int judgeend(GameTree node) {
        // judge the win state
        int value;
        value = check_up_to_down(node);
        if (value != -2) {
            return value;
        }
        value = check_vertic(node);
        if (value != -2) {
            return value;
        }
        value = check_diagonal(node);
        if (value != -2) {
            return value;
        }

        // check the draw state
        for (int k = 0; k < node.board.length; k++) {
            for (int i = 0; i < node.board[1].length; i++) {
                for (int j = 0; j < node.board[1].length; j++) {
                    if (node.board[k][i][j] == 0) {
                        return 2;
                    }
                }
            }
        }
        return 0;
    }

    int check_up_to_down(GameTree node) {
        for (int k = 0; k < node.board.length; k++) {
            for (int i = 0; i < node.board[0].length; i++) {
                if (node.board[k][i][1] == node.board[k][i][2] && node.board[k][i][2] == node.board[k][i][0] && node.board[k][i][1] == node.board[k][i][3]) {
                    if (node.board[k][i][1] == first) {
                        return 1;
                    } else if (node.board[k][i][1] == second) {
                        return -1;
                    }
                }
            }
            // check lines
            for (int i = 0; i < node.board[0].length; i++) {
                if (node.board[k][1][i] == node.board[k][2][i] && node.board[k][2][i] == node.board[k][0][i] && node.board[k][2][i] == node.board[k][3][i]) {
                    if (node.board[k][0][i] == first) {
                        return 1;
                    } else if (node.board[k][0][i] == second) {
                        return -1;
                    }
                }
            }
            // check the diagonal
            if (node.board[k][0][0] == node.board[k][1][1] && node.board[k][1][1] == node.board[k][2][2] && node.board[k][0][0] == node.board[k][3][3]) {
                if (node.board[k][1][1] == first) {
                    return 1;
                } else if (node.board[k][1][1] == second) {
                    return -1;
                }
            }
            if (node.board[k][3][0] == node.board[k][2][1] && node.board[k][1][2] == node.board[k][2][1] && node.board[k][1][2] == node.board[k][0][3]) {
                if (node.board[k][2][1] == first) {
                    return 1;
                } else if (node.board[k][2][1] == second) {
                    return -1;
                }
            }
        }
        return -2;
    }


    int check_vertic(GameTree node) {
        for (int k = 0; k < node.board.length; k++) {
            for (int i = 0; i < node.board[0].length; i++) {
                if (node.board[1][k][i] == node.board[2][k][i] && node.board[2][k][i] == node.board[3][k][i] && node.board[3][k][i] == node.board[0][k][i]) {
                    if (node.board[0][k][i] == first) {
                        return 1;
                    } else if (node.board[0][k][i] == second) {
                        return -1;
                    }
                }
            }
        }
        return -2;
    }

    int check_diagonal(GameTree node) {
        // check the diagonal
        for (int k = 0; k < node.board.length; k++) {
            if (node.board[0][k][0] == node.board[1][k][1] && node.board[2][k][2] == node.board[1][k][1] && node.board[2][k][2] == node.board[3][k][3]) {
                if (node.board[1][k][1] == first) {
                    return 1;
                } else if (node.board[1][k][1] == second) {
                    return -1;
                }
            }
            if (node.board[0][0][k] == node.board[1][1][k] && node.board[1][1][k] == node.board[2][2][k] && node.board[2][2][k] == node.board[3][3][k]) {
                if (node.board[2][2][k] == first) {
                    return 1;
                } else if (node.board[2][2][k] == second) {
                    return -1;
                }
            }
            if (node.board[0][k][3] == node.board[1][k][2] && node.board[2][k][1] == node.board[1][k][2] && node.board[2][k][1] == node.board[3][k][0]) {
                if (node.board[2][k][1] == first) {
                    return 1;
                } else if (node.board[2][k][1] == second) {
                    return -1;
                }
            }
            if (node.board[0][3][k] == node.board[1][2][k] && node.board[1][2][k] == node.board[2][1][k] && node.board[2][1][k] == node.board[3][0][k]) {
                if (node.board[2][1][k] == first) {
                    return 1;
                } else if (node.board[2][1][k] == second) {
                    return -1;
                }
            }
        }
        if (node.board[0][0][0] == node.board[1][1][1] && node.board[2][2][2] == node.board[1][1][1] && node.board[2][2][2] == node.board[3][3][3]) {
            if (node.board[1][1][1] == first) {
                return 1;
            } else if (node.board[1][1][1] == second) {
                return -1;
            }
        }
        if (node.board[3][0][0] == node.board[2][1][1] && node.board[1][2][2] == node.board[2][1][1] && node.board[1][2][2] == node.board[0][3][3]) {
            if (node.board[2][1][1] == first) {
                return 1;
            } else if (node.board[2][1][1] == second) {
                return -1;
            }
        }
        if (node.board[0][0][3] == node.board[1][1][2] && node.board[2][2][1] == node.board[1][1][2] && node.board[2][2][1] == node.board[3][3][0]) {
            if (node.board[1][1][2] == first) {
                return 1;
            } else if (node.board[1][1][2] == second) {
                return -1;
            }
        }
        if (node.board[0][3][0] == node.board[1][2][1] && node.board[1][2][1] == node.board[2][1][2] && node.board[2][1][2] == node.board[3][0][3]) {
            if (node.board[2][1][2] == first) {
                return 1;
            } else if (node.board[2][1][2] == second) {
                return -1;
            }
        }
        return -2;
    }

    // evaluate end node score
    boolean end(GameTree node) {
        if (node.flag == -1) {
            node.score = -1000;
            return true;
        } else if (node.flag == 1) {
            node.score = 1000;
            return true;
        } else if (node.flag == 0) {
            node.score = 0;
            return true;
        }
        return false;
    }

    // recursively score every node in tree
    void eval(GameTree node) {
        if (end(node)) {
            return;
        } else if (node.nextplayer == 1) {
            int count = -1900;
            node.score = max(node, count);
        } else {
            int count = 1900;
            node.score = min(node, count);
        }
        return;
    }

    // minmax algorithm
    float max(GameTree node, float count) {
        if (node.successors.size() == 0) {
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


    float min(GameTree node, float count) {
        if (node.successors.size() == 0) {
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
        if (end(tttNode)) {
            return tttNode.score;
        }
        int count = 0;
        //ArrayList counts = new ArrayList();

        //refill the blanks with next player move
        count += refill(tttNode, tttNode.nextplayer);
        count += refill(tttNode, -tttNode.nextplayer);
        return count;
    }
        //counts.add(count);


        //pick the best move
        /*if (tttNode.nextplayer == first) {
            int max = -2 * 9;
            for (int num : counts
            ) {
                if (num > max) {
                    max = num;
                }
            }
            count = max;
        } else {
            int max = 2 * 9;
            for (int num : counts
            ) {
                if (num < max) {
                    max = num;
                }
            }
            count = max;
        }*/


    int refill(GameTree node, int player) {
        int count = 0;
        int[][][] tempboard = new int[node.board[1].length][node.board[1].length][node.board[1].length];
        for (int k = 0; k < 4; k++) {
            for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                    if (node.board[k][i][j] == 0) {
                        tempboard[k][i][j] = player;
                    } else {
                        tempboard[k][i][j] = node.board[k][i][j];
                    }
                }
            }
        }
        for (int k = 0; k < node.board.length; k++) {
            for (int i = 0; i < node.board[0].length; i++) {

                // add each line in each height
                count += (node.board[k][i][1] + node.board[k][i][2] + node.board[k][i][0] + node.board[k][i][3])/4;
                // add each row in each height
                count += (node.board[k][1][i] + node.board[k][2][i] + node.board[k][0][i] + node.board[k][3][i])/4;
                // from up to down add each pole in each point
                count += (node.board[1][k][i] + node.board[2][k][i] + node.board[3][k][i] + node.board[0][k][i])/4;
            }
            // from each side perpendicular to the ground add their diagonals into count
            count += (node.board[0][k][0] + node.board[1][k][1] + node.board[2][k][2] + node.board[3][k][3])/4;
            count += (node.board[0][0][k] + node.board[1][1][k] + node.board[2][2][k] + node.board[3][3][k])/4;
            count += (node.board[0][k][3] + node.board[1][k][2] + node.board[2][k][1] + node.board[3][k][0])/4;
            count += (node.board[0][3][k] + node.board[1][2][k] +node.board[2][1][k]  + node.board[3][0][k])/4;
            // from sides parallel to the ground and add their diagonal
            count += (node.board[k][0][0] + node.board[k][1][1] + node.board[k][2][2] + node.board[k][3][3])/4;
            count += (node.board[k][3][0] + node.board[k][2][1] + node.board[k][1][2] + node.board[k][0][3])/4;
        }

        // from the special side which is combined by eight vertex
        count += (node.board[0][0][0] + node.board[1][1][1] + node.board[2][2][2] + node.board[3][3][3])/4;
        count += (node.board[3][0][0] + node.board[2][1][1] + node.board[1][2][2] + node.board[0][3][3])/4;
        count += (node.board[0][3][0] + node.board[1][2][1] + node.board[2][1][2] + node.board[3][0][3])/4;
        count += (node.board[0][0][3] + node.board[1][1][2] + node.board[2][2][1] + node.board[3][3][0])/4;
        return count;
    }
}