import java.util.*;

public class NegativeNumberExceptionDriver {

    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);
        int firstNumber = 0;
        int secondNumber = 0;

        try {

           
            try {
                System.out.print("Enter first non-negative number: ");
                firstNumber = input.nextInt();

                if (firstNumber < 0) {
                    throw new NegativeNumberException();
                }
            }
            catch (NegativeNumberException e) {
                System.out.println("First number error: " + e.getMessage());
            }
            catch (InputMismatchException e) {
                System.out.println("Invalid input!");
                input.next(); 
            }

            try {
                System.out.print("Enter second non-negative number: ");
                secondNumber = input.nextInt();

                if (secondNumber < 0) {
                    throw new NegativeNumberException();
                }
            }
            catch (NegativeNumberException e) {
                System.out.println("Second number error: " + e.getMessage());
            }
            catch (InputMismatchException e) {
                System.out.println("Invalid input!");
                input.next();
            }

        }
        finally {
            System.out.println("Numbers entered: " + firstNumber + " and " + secondNumber);
            System.out.println("Program finished.");
            input.close();
        }
    }
}