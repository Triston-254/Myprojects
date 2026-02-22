import java.util.Scanner;
import java.util.Random;

public class DiskDriveTest {
    
    
    private static boolean isDiskDriveReady() {
        Random random = new Random();
        
        return random.nextInt(10) < 7;
    }
    
    
    public static String readFromDiskDrive(String driveName) 
            throws DiskDriveNotReadyException {
        
        System.out.println("Attempting to read from " + driveName + "...");
        
        if (!isDiskDriveReady()) {
            
            throw new DiskDriveNotReadyException();
        }
        
        return "Data read successfully from " + driveName;
    }
    
    
    public static void writeToDiskDrive(String driveName, String data) 
            throws DiskDriveNotReadyException {
        
        System.out.println("Attempting to write to " + driveName + "...");
        
        if (!isDiskDriveReady()) {
            
            throw new DiskDriveNotReadyException("Cannot write to " + driveName + " - Drive not ready!");
        }
        
        System.out.println("Data '" + data + "' written successfully to " + driveName);
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== Disk Drive Operation Simulator ===");
        System.out.println("This program simulates disk drive operations with random failures.\n");
        
        
        try {
            System.out.println("Test 1: Read operation");
            String result = readFromDiskDrive("C:");
            System.out.println("Result: " + result);
        } catch (DiskDriveNotReadyException e) {
            System.out.println("Exception caught: " + e.getMessage());
        }
        
        System.out.println(); 
        
        
        try {
            System.out.println("Test 2: Write operation");
            writeToDiskDrive("D:", "Important data");
        } catch (DiskDriveNotReadyException e) {
            System.out.println("Exception caught: " + e.getMessage());
        }
        
        System.out.println(); 
        
        
        System.out.println("Test 3: Manual drive check");
        System.out.print("Enter drive name (e.g., E:, F:, etc.): ");
        String driveName = scanner.nextLine();
        
        try {
            checkDriveStatus(driveName);
        } catch (DiskDriveNotReadyException e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        System.out.println("\n=== Program Complete ===");
        scanner.close();
    }
    
    
    public static void checkDriveStatus(String driveName) 
            throws DiskDriveNotReadyException {
        
        System.out.println("Checking status of drive " + driveName + "...");
        
        
        if (driveName.equals("A:") || driveName.equals("B:")) {
            
            throw new DiskDriveNotReadyException("Legacy drive " + driveName + " not detected!");
        } else if (driveName.equals("Z:")) {
            
            throw new DiskDriveNotReadyException("Network drive " + driveName + " is disconnected!");
        } else {
            
            if (!isDiskDriveReady()) {
                throw new DiskDriveNotReadyException();
            }
            System.out.println("Drive " + driveName + " is ready and accessible");
        }
    }
}