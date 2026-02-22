public class DiskDriveNotReadyException extends Exception {
    
    // No-argument constructor
    public DiskDriveNotReadyException() {
        super("Disk Drive Not Ready!");
    }
    
    // Constructor with a String parameter
    public DiskDriveNotReadyException(String message) {
        super(message);
    }
}