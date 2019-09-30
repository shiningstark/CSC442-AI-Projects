import java.util.ArrayList;
import java.util.Scanner;
//import java.util.List;
public class Game {
    private final int size = 3; //board length
    private final int number = 9;// the number of board
    public int[][][] state = new int[number][size][size]; // the whole state space
    public int [][] board = new int[size][size]; // every time processing board
    //public int [][] iniboard = new int[size][size]; // initial board
    public boolean result =true; // remark of end
    private final int firstmove = 1; // 'X'
    private final int secondmove =-1;// 'O'
    public int mark = 1; // remark of turn
    public int[] place = new int[2]; //position of every move and changed according to move
    public int people; // people turn
    public int computer;// computer turn
    public int countstep;// number of whole move
    // every single board to display
    private final String[][] oneboard = new String[][] {
            {" | ","_"," | ","_"," | ","_"," | "},
            {"----------------"},
            {" | ","_"," | ","_"," | ","_"," | "},
            {"----------------"},
            {" | ","_"," | ","_"," | ","_"," | "},
    };

    // init game parameters
    public void game( int order) {
        countstep = 0;
        place[0] = order;
        for (int k = 0;k < size*size; k++) {
            for (int i = 0; i < board.length; i++) {
                for (int j = 0; j < board[i].length; j++) {
                    state[k][i][j] = 0;
                    board[i][j] = 0;
                    //iniboard[i][j] = 0;
                }
            }
        }
    }

// judge terminal state
    void isover(int flag) {
        if (flag == 3) {
            System.out.println("Draw");
            result = false;
        } else if (flag == people) {
            System.out.println("People Win");
            result = false;
        } else if (flag == computer) {
            System.out.println("Computer Win");
            result = false;
        }
    }

// put the current single board state into the bigger board, transform function
    void give(int order){
        for (int i = 0; i < board[1].length; i++) {
            for (int j = 0; j < board[1].length; j++) {
                state[order][i][j] = board[i][j];
            }
        }
    }

// transform to the new single board
    void back(int order){
        for (int i = 0; i < board[1].length; i++) {
            for (int j = 0; j < board[1].length; j++) {
                board[i][j] = state[order][i][j] ;
            }
        }
    }

// people turn
    void People(int flag,int order){
        int x,y;
        int step;
        int[] position = new int[2];
        do{
            System.out.println("what's your choice(enter number between 1-9): ");
            Scanner sc = new Scanner(System.in);
            step = sc.nextInt()-1;

            // check the legal move
            if(step>=0&&step<=8) {
                y = step % 3; //corresponding of choice
                x = step / 3;
                if (countstep == 0){
                    position[0] = place[0];
                }else {
                    position[0] = place[1];
                }
                position[1] = step;
                if (board[x][y] == 0) {
                    board[x][y] = people;
                }else{
                    retype(flag,order);
                    return ;
                }
            }else{
                retype(flag,order);
                return ;
            }

            // change state
            place[0] = position[0];
            place[1] = position[1];
            give(position[0]);
            countstep += 1;
            GameTree temptree = new GameTree();
            temptree.GameTree(computer,state,place,flag);
            back(position[1]);
            printboard();
            isover(temptree.flag);
            return;
        }while(true);
    }


    void retype(int flag,int order){
        System.err.println("The choice is wrong. Please retype your choice!");
        People(flag,order);
    }

//computer turn
    void Computer(int flag){
        float max = -2*computer*10; // sure the max value of computer
        int[] position = new int[2];

        // if computer is first,the move will be random
        if(countstep ==0) {
            board[(size - 1) / 2][(size - 1) / 2] = computer;
            position[1] = (size * size - 1) / 2;
            position[0] = (int) (Math.random() * (number -1));
            place[0] = position[0];
            place[1] = position[1];
            System.err.println("Computer action's height is:"+place[0]);
            System.err.println("Computer action's place is:"+place[1]);
            give(position[0]);
            countstep += 1;
            back(position[1]);
            printboard();
            return;
        }

        // choose the best move
        GameTree temptree = new GameTree();
        temptree.GameTree(computer,state,place,flag);
        temptree.successor(temptree); // generate the search tree

        // choose the move
        for (GameTree node:temptree.successors
             ) {
            //node.eval(node);
            if (computer == firstmove) {
                if (node.score > max) {
                    position = node.position;
                    max = node.score;
                }
            } else{
                if (node.score < max) {
                    position = node.position;
                    max = node.score;
                }
            }
        }

        // change state
        int y = position[1]%size;
        int x = position[1]/size;
        place[0] = position[0];
        place[1] = position[1];
        board[x][y] = computer;
        System.err.println("Computer action's height is:"+place[0]);
        System.err.println("Computer action's place is:"+place[1]);
        temptree.GameTree(people,state,place,flag);
        isover(temptree.flag);
        give(position[0]);

        //check the next board is full
        while (true){
            if (temptree.flag == 0) {
                System.err.println("\nThe next board is full");
                int value = inputorder(temptree.status);
                if (value > 0) {
                    back(value);
                    break;
                }
            }else{
                back(position[1]);
                break;
            }
        }
        printboard();
        countstep += 1;
    }


    //display the whole board
    void printboard(){
        for(int k=0;k<size*size;k++){
            for(int i=0;i<size;i++) {
                for (int j = 0; j < size; j++) {
                    //System.out.println(board[i][j]);
                    if (state[k][i][j] == firstmove) {
                        oneboard[2 * i][2 * j + 1] = "X";
                    } else if (state[k][i][j] == secondmove) {
                        oneboard[2 * i][2 * j + 1] = "O";
                    }else if (state[k][i][j] == 0) {
                        oneboard[2 * i][2 * j + 1] = "_";
                    }
                }
            }
            System.err.print("This board's number is: "+(k+1)+"\n");
            for (int i = 0; i < oneboard.length; i++) {
                for (int j = 0; j < oneboard[i].length; j++) {
                    System.err.print(oneboard[i][j]);
                }
                System.err.print("\n");
            }
            System.err.print("\n");
        }
        System.err.print("-------------------------------");
        System.err.print("\n");
    }

// help if the next board is full, change the board
    int inputorder(int[] status){
        int order ;
        do {
            System.out.println("\nWhich board do you want to play?(type 1-9 and use Enter as end)\n");
            Scanner sc1 = new Scanner(System.in);
            order = sc1.nextInt() - 1;
            if (order > 8 || order < 0) {
                System.err.println("\nPlease type valid order\n");
            }else if (status[order] !=0){
                return -1;
            }else{
                return order;
            }
        }while(true);
    }

    // the game main process
    void run(int flag){
        int order;
        // make sure which is first move and if the computer first will use the random
        if (flag == 1) {
            people = firstmove;
            computer = secondmove;
            order = inputorder(new int[number]);
        } else {
            people = secondmove;
            computer = firstmove;
            order =(int)(Math.random()*8);
        }

        // init game
        game(order);
        printboard();

        // the game main process
        while (result) {
            if (mark == people) {
                People(flag,order);
                mark *= -1;
            } else {
                Computer(flag);
                mark *= -1;
            }
        }
    }
}
