import java.io.IOException;
import java.io.InputStream;

public class RunPythonScript {
    public static void main(String[] args) {
        try {
            String usernameArg = "";  // Initialize the username argument

            // Check if there is an argument passed to the Java program
            if (args.length > 0) {
                usernameArg = args[0];  // Set the username argument
            }

            // Step 1: Create and activate the virtual environment
            ProcessBuilder pbCreate;
            if (isWindows()) {
                pbCreate = createProcessBuilder("python", "-m", "venv", "venv");
            } else {
                pbCreate = createProcessBuilder("python3", "-m", "venv", "venv");
            }
            executeCommand(pbCreate, "Create virtual environment");

            ProcessBuilder pbActivate;
            if (isWindows()) {
                pbActivate = createProcessBuilder("cmd", "/c", "venv\\Scripts\\activate");
            } else {
                pbActivate = createProcessBuilder("bash", "-c", "source venv/bin/activate");
            }
            executeCommand(pbActivate, "Activate virtual environment");

            // Step 2: Upgrade pip in the virtual environment
            ProcessBuilder pbUpgrade;
            if (isWindows()) {
                pbUpgrade = createProcessBuilder("venv\\Scripts\\python", "-m", "pip", "install", "--upgrade", "pip");
            } else {
                pbUpgrade = createProcessBuilder("venv/bin/python3", "-m", "pip", "install", "--upgrade", "pip");
            }
            executeCommand(pbUpgrade, "Upgrade pip");

            // Step 3: Install Python dependencies from requirements.txt
            ProcessBuilder pbInstall;
            if (isWindows()) {
                pbInstall = createProcessBuilder("venv\\Scripts\\pip", "install", "-r", "requirements.txt");
            } else {
                pbInstall = createProcessBuilder("venv/bin/pip3", "install", "-r", "requirements.txt");
            }
            executeCommand(pbInstall, "Install Python dependencies");

            // Step 4: Run the launcher.py script within the virtual environment
            ProcessBuilder pbRun;
            if (isWindows()) {
                pbRun = createProcessBuilder("venv\\Scripts\\python", "launcher.py", "--username", usernameArg);
            } else {
                pbRun = createProcessBuilder("venv/bin/python3", "launcher.py", "--username", usernameArg);
            }
            executeCommand(pbRun, "Run launcher.py");

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static ProcessBuilder createProcessBuilder(String... command) {
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.redirectErrorStream(true);
        return pb;
    }

    private static void executeCommand(ProcessBuilder pb, String description) throws IOException, InterruptedException {
        System.out.println("Executing: " + description);
        Process process = pb.start();

        // Capture and print the output
        InputStream inputStream = process.getInputStream();
        byte[] buffer = new byte[1024];
        int bytesRead;

        while ((bytesRead = inputStream.read(buffer)) != -1) {
            System.out.print(new String(buffer, 0, bytesRead));
        }

        // Wait for the command execution process to complete
        int exitCode = process.waitFor();
        System.out.println(description + " exited with code: " + exitCode);

        if (exitCode != 0) {
            System.err.println("Error occurred during: " + description);
        }
    }

    private static boolean isWindows() {
        return System.getProperty("os.name").toLowerCase().contains("win");
    }
}
