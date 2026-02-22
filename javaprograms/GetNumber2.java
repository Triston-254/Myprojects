import java.util.*;

public class GetNumber2
{
    public static void main(String args[])
    {
        Scanner stdin = new Scanner(System.in);
        int firstNumber = 0;
        int secondNumber = 0;


        try
        {
            System.out.print("Enter the first non-negative number: ");
            firstNumber = stdin.nextInt();

            if (firstNumber < 0)
            {
                throw new InputMismatchException("Enter non-negative number!");
            }
        }
        catch (InputMismatchException e)
        {
            System.out.println("Error: " + e.getMessage());
        }

        
        try
        {
            System.out.print("Enter the second non-negative number: ");
            secondNumber = stdin.nextInt();

            if (secondNumber < 0)
            {
                throw new InputMismatchException("Enter non-negative number only!");
            }
        }
        catch (InputMismatchException e)
        {
            System.out.println("Error: " + e.getMessage());
        }

        System.out.println("\nYour numbers are " + firstNumber + " and " + secondNumber);

        stdin.close();
    }
}