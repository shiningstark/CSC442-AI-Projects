import java.util.ArrayList;
import java.util.Scanner;
//import java.util.List;
public class Game {
    private final int size = 4; //board length
    private final int number = 4;// the number of board
    public int[][][] state = new int[number][size][size]; // the whole state space
    //public int [][] board = new int[size][size]; // every time processing board
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
            {" | ","_"," | ","_"," | ","_"," | ","_"," | "},
            {"-----------------------"},
            {" | ","_"," | ","_"," | ","_"," | ","_"," | "},
            {"------------------------"},
            {" | ","_"," | ","_"," | ","_"," | ","_"," | "},
            {"------------------------"},
            {" | ","_"," | ","_"," | ","_"," | ","_"," | "},
    };

    // init game parameters
    public void game() {
        countstep = 0;
        place[0] = -1;
        for (int k = 0;k < number; k++) {
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    state[k][i][j] = 0;
                    //board[i][j] = 0;
                    //iniboard[i][j] = 0;
                }
            }
        }
    }

// judge terminal state
    void isover(int flag) {
        if (flag == 0) {
            System.err.println("Draw");
            result = false;
        } else if (flag == people) {
            System.err.println("People Win");
            result = false;
        } else if (flag == computer) {
            System.err.println("Computer Win");
            result = false;
        }
    }

// put the current single board state into the bigger board, transform function
    /*void give(int order){
        for (int i = 0; i < board[1].length; i++) {
            for (int j = 0; j < board[1].length; j++) {
                state[order][i][j] = board[i][j];
                if (!result){
                    board[i][j] = iniboard[i][j];
                }
            }
        }
    }*/

// transform to the new single board
    /*void back(int order){
        for (int i = 0; i < board[1].length; i++) {
            for (int j = 0; j < board[1].length; j++) {
                board[i][j] = state[order][i][j] ;
                if (!result){
                    board[i][j] = iniboard[i][j];
                }
            }
        }
    }*/

// people turn
    void People(int flag){
        int x,y;
        int step;
        int[] position = new int[2];
        do{
            position[0]=inputorder();
            System.err.println("what's your choice about the place(enter number between 1-16): ");
            Scanner sc = new Scanner(System.in);
            step = sc.nextInt()-1;

            // check the legal move
            if(step>=0&&step<=15) {
                y = step % size; //corresponding of choice
                x = step / size;
                /*if (countstep == 0){
                    position[0] = place[0];
                }else{
                    position[0] = place[1];
                }*/
                position[1] = step;
                if (state[position[0]][x][y] == 0) {
                    state[position[0]][x][y] = people;
                }else{
                    retype(flag);
                    return ;
                }
            }else{
                retype(flag);
                return ;
            }

            // change state
            place[0] = position[0];
            place[1] = position[1];
            //give(position[0]);
            countstep += 1;
            GameTree temptree = new GameTree();
            temptree.GameTree(computer,state,place,flag);
            //back(position[1]);
            printboard();
            isover(temptree.flag);
            return;
        }while(true);
    }


    void retype(int flag){
        System.err.println("The choice is wrong. Please retype your choice!");
        People(flag);
    }

//computer turn
    void Computer(int flag) {
        float max = -2 * computer * 10; // sure the max value of computer
        int[] position = new int[2];

        // if computer is first,the move will be random
        if (countstep == 0) {
            //board[1][1] = computer;
            position[1] = 5;
            position[0] = (int) (Math.random() * (number - 1));
            place[0] = position[0];
            place[1] = position[1];
            int y = position[1] % size;
            int x = position[1] / size;
            state[place[0]][x][y] = computer;
            System.out.println("Computer action's height is:"+place[0]);
            System.out.println("Computer action's place is:"+place[1]);
            //give(position[0]);
            countstep += 1;
            //back(position[1]);
            printboard();
            return;
        }

        // choose the best move
        GameTree temptree = new GameTree();
        temptree.GameTree(computer, state, place, flag);
        temptree.successor(temptree); // generate the search tree

        // choose the move
        for (GameTree node : temptree.successors
        ) {
            //node.eval(node);
            if (computer == firstmove) {
                if (node.score > max) {
                    position = node.position;
                    max = node.score;
                }
            } else {
                if (node.score < max) {
                    position = node.position;
                    max = node.score;
                }
            }
        }

        // change state
        int y = position[1] % size;
        int x = position[1] / size;
        place[0] = position[0];
        place[1] = position[1];
        //board[x][y] = computer;
        state[position[0]][x][y] = computer;
        System.out.println("Computer action's height is:"+place[0]);
        System.out.println("Computer action's place is:"+place[1]);
        temptree.GameTree(people, state, place, flag);
        //give(position[0]);
        //back(position[1]);
        printboard();
        isover(temptree.flag);
        countstep += 1;
    }
        //check the next board is full
        /*while (true){
            if (temptree.flag == 0) {
                System.out.println("\nThe next board is full");
                int value = inputorder();
                if (value > 0) {
                    back(value);
                    break;
                }
            }else{
                back(position[1]);
                break;
            }
        }
    }*/


    //display the whole board
    void printboard(){
        for(int k=0;k<number;k++){
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
    int inputorder(){
        int order ;
        do {
            System.err.println("\nWhich board do you want to play?(type 1-4 and use Enter as end)\n");
            Scanner sc1 = new Scanner(System.in);
            order = sc1.nextInt() - 1;
            if (order > 3 || order < 0) {
                System.err.println("\nPlease type valid order\n");
            }else{
                return order;
            }
        }while(true);
    }

    // the game main process
    void run(int flag){
        // make sure which is first move and if the computer first will use the random
        if (flag == 1) {
            people = firstmove;
            computer = secondmove;
            //order = inputorder();
        } else {
            people = secondmove;
            computer = firstmove;
            //order =(int)(Math.random()*3);
        }

        // init game
        game();
        printboard();

        // the game main process
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
