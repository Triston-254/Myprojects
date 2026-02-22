import java.util.Scanner;

public class BankSystem {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\n1.Create");
            System.out.println("2.Deposit");
            System.out.println("3.Withdraw");
            System.out.println("4.Check Balance");
            System.out.println("5.Exit");

            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.println("Create selected");
                    break;
                case 2:
                    System.out.println("Deposit selected");
                    break;
                case 3:
                    System.out.println("Withdraw selected");
                    break;
                case 4:
                    System.out.println("Check Balance selected");
                    break;
                case 5:
                    System.out.println("Exiting...");
                    return;
                default:
                    System.out.println("Invalid choice");
            }
        }
    }
}