import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class receiptProcessor{

    public static void main(String[] args) throws IOException{
        ProcessBuilder pb = new ProcessBuilder("python","receipt_reader.py");
        Process p = pb.start();
        System.out.println(pb.command());
        
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(
        p.getInputStream()));

        String s = null;

        while((s = stdInput.readLine()) != null){
            System.out.println(s);
        }
    }
}