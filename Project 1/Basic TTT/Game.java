import java.util.Scanner;
public class Game {
    public int size = 3; // the length of board
    public int [][] board = new int[size][size]; // the game board which is also the state of search
    boolean result =true; // as a mark to judge if the game ends
    private final int firstmove = 1; // the 'X'
    private final int secondmove =-1; // the 'O'
    public int mark; // used for change turn
    int people; // people's turn
    int computer; // computer turn
    int countstep; // count the all steps of game
    String[][] displayboard;

    //init the game
    public void game() {
        countstep = 0;
        mark = 1;
        // used to display the board
        displayboard = new String[][] {
                {" | ","_"," | ","_"," | ","_"," | "},
                {"----------------"},
                {" | ","_"," | ","_"," | ","_"," | "},
                {"----------------"},
                {" | ","_"," | ","_"," | ","_"," | "},
        };
        // the init state place is empty
        for (int i = 0; i < board[1].length; i++) {
            for (int j = 0; j < board[1].length; j++) {
                //state[i][j] = 0;
                board[i][j] = 0;
                //iniboard[i][j] = 0;
            }
        }
    }

    // judge if the game end
    boolean isover(int flag){
        if(flag==0){
            System.err.println("Draw");
            result = false;
        }else if (flag==people){
            System.err.println("People Win");
            result = false;
        }else if (flag==computer) {
            System.err.println("Computer Win");
            result = false;
        }
        return result;
    }

    // people turn and what's people choice
    void People(int flag){
        int x,y; // corresponding of people choice
        int step;

        // recursively judge if the move is legal
        do{
            System.err.println("what's your choice(enter number between 1-9): ");
            Scanner sc = new Scanner(System.in);
            step = sc.nextInt()-1; // get input of choice

            // judge if the move is legal
            if(step>=0&&step<=8) {
                y = step % 3; //record the place of the choice
                x = step / 3;
                if (board[x][y] == 0) {
                    // change the state (transform function)
                    board[x][y] = people;
                }else{
                    retype(flag);
                    return ;
                }
            }else{
                retype(flag);
                return ;
            }
            countstep += 1;

            //create the state node
            GameTree temptree = new GameTree();
            temptree.GameTree(computer,board,step,flag);
            printboard();
            //judge the end
            if(!isover(temptree.flag)){
                return;
            };
            return;
        }while(true);
    }


    void retype(int flag){
        System.err.println("The choice is invaild. Please retype your choice!");
        People(flag);
    }

    // computer turn and choose the best move
    void Computer(int flag){
        int max = -2*computer;// make sure the 'max' value of computer
        int position = -1;

        // if computer is first, just choose the center
        if (countstep ==0){
            board[(size-1)/2][(size-1)/2] = computer;
            System.out.println("Computer action is: "+5);
            printboard();
            countstep += 1;
            return;
        }

        // if computer is not first, create the search tree to make best move
        GameTree temptree = new GameTree();
        temptree.GameTree(computer,board,position,flag);
        temptree.successor(temptree);

        // from the successor of computer to choose the best one
        for (GameTree node:temptree.successors
             ) {
            int value=node.eval(node);// evaluate the goodness of successor
            if (computer == firstmove) {
                if (value > max) {
                    position = node.position;
                    max = value;
                }
            } else{
                if (value < max) {
                    position = node.position;
                    max = value;
                }
            }
        }

        // print the computer action and transform state
        System.out.println("Computer action is: "+(position+1));
        int y = position%3;
        int x = position/3;
        board[x][y] = computer;
        countstep += 1;
        printboard();
        // judge the end
        temptree.GameTree(people,board,position,flag);
        if(!isover(temptree.flag)){
            return;
        }
    }
    void printboard(){
        for(int i=0;i<board.length;i++){
            for(int j=0;j<board.length;j++){
                //System.out.println(board[i][j]);
                if(board[i][j]==firstmove){
                    displayboard[2*i][2*j+1] = "X";
                }else if(board[i][j]==secondmove){
                    displayboard[2*i][2*j+1] = "O";
                }
            }
            //System.out.print("\n");
        }

        for(int i=0;i<displayboard.length;i++){
            for (int j=0;j<displayboard[i].length;j++){
                System.err.print(displayboard[i][j]);
            }
            System.err.print("\n");
        }
        System.err.print("\n");
        System.err.print("\n");
    }

    // the game processor function
    void run(int flag){
        // make sure which is the firstmove
        if (flag == 1) {
            people = firstmove;
            computer = secondmove;
        } else if(flag == 0){
            people = secondmove;
            computer = firstmove;
        }
        // init the game parameter
        game();
        printboard(); // print state of board which is easy to debugger
        // the move process
        while (result) {
            if (mark == people) {
                People(flag);
                mark *= -1;
            } else {
                Computer(flag);
                mark *= -1;
            }
        }
    }
}
