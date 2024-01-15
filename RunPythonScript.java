import java.io.IOException;
import java.io.InputStream;

public class RunPythonScript {
    public static void main(String[] args) {
        String pyScriptPath = "launcher.py";

        try {
            ProcessBuilder pb;
            String os = System.getProperty("os.name").toLowerCase();

            if (os.contains("win")) {
                pb = new ProcessBuilder("python", pyScriptPath);
            } else {
                pb = new ProcessBuilder("python3", pyScriptPath);
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

            int exitCode = process.waitFor();
            System.out.println("Python script exited with code: " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
