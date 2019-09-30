import java.util.Scanner;

public class tictactoe {
    public static void main(String[] arg){

        // init game
        Game game = new Game();
        while(true) {
            System.err.println("\nYou want to player X or O?(type 1 or 0 and use Enter as end)\n");// 1 represent X,0 represent O;
            Scanner preference = new Scanner(System.in);
            int flag = preference.nextInt();

            // check if the input is legal
            if (flag != 1 && flag != 0) {
                System.err.println("\nPlease type valid number\n");
            }else {
                //the game main function
                game.run(flag);
                System.err.println("\n\nGame Over!!!\n\n");
                game.result = true;
                game.mark = 1;
            }
        }
    }
}
