//import java.io.IOException;
import java.util.Scanner;

public class tictactoe {
    public static void main(String[] arg){
        //init the game
        Game game = new Game();
        do {
            // get opponent choice
            System.err.println("\nYou want to player X or O?(type 1 or 0 and use Enter as end)\n");// 1 represent X,0 represent O;
            //int flag = -1;
            Scanner sc= new Scanner(System.in);
            //String c = sc.nextLine();
            //char c = (char)System.in.read();
            int flag = sc.nextInt();
            //check if the choice is legal
            if (flag != 1 && flag != 0) {
                System.err.println("\nPlease type valid number\n");
            } else {
                // recursively run the game
                while(true) {
                    game.run(flag);
                    System.err.println("\nGame Over!!!\n");
                    game.result = true;
                    game.mark = 1;
                    break;
                }
            }
        }while (true);
    }
}
