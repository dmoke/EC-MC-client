import java.io.IOException;
import java.io.InputStream;

public class RunPythonScript {
    public static void main(String[] args) {
        try {
            // Step 1: Create and activate the virtual environment
            createAndActivateVirtualEnv();

            // Step 2: Run the launcher.py script within the virtual environment
            runPythonScript("launcher.py");

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static void createAndActivateVirtualEnv() throws IOException, InterruptedException {
        String os = System.getProperty("os.name").toLowerCase();
        ProcessBuilder pb;

        // Choose appropriate Python executable and venv command based on the operating system
        if (os.contains("win")) {
            pb = new ProcessBuilder("python", "-m", "venv", "venv");
        } else {
            pb = new ProcessBuilder("python3", "-m", "venv", "venv");
        }

        Process process = pb.start();

        // Wait for the venv creation process to complete
        int exitCode = process.waitFor();
        System.out.println("Virtual environment created with exit code: " + exitCode);

        // Activate the virtual environment
        if (os.contains("win")) {
        pb = new ProcessBuilder("cmd", "/c", "python", "-m", "venv", "venv");
        } else {
        pb = new ProcessBuilder("python3", "-m", "venv", "venv");
        }

        process = pb.start();
        exitCode = process.waitFor();
        System.out.println("Virtual environment activated with exit code: " + exitCode);
    }

    private static void runPythonScript(String scriptPath) throws IOException, InterruptedException {
        String os = System.getProperty("os.name").toLowerCase();
        ProcessBuilder pb;

        // Choose appropriate Python executable and script path based on the operating system
        if (os.contains("win")) {
            pb = new ProcessBuilder("venv\\Scripts\\python", scriptPath);
        } else {
            pb = new ProcessBuilder("venv/bin/python3", scriptPath);
        }

        pb.redirectErrorStream(true);
        Process process = pb.start();

        // Capture and print the output
        InputStream inputStream = process.getInputStream();
        byte[] buffer = new byte[1024];
        int bytesRead;

        while ((bytesRead = inputStream.read(buffer)) != -1) {
            System.out.print(new String(buffer, 0, bytesRead));
        }

        // Wait for the script execution process to complete
        int exitCode = process.waitFor();
        System.out.println("Python script exited with code: " + exitCode);
    }
}
