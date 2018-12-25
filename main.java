import java.io.File;
import java.io.FileOutputStream;
import java.sql.*;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

@SuppressWarnings("Duplicates")
public class main {
    public int yeezy;
    public int crocs;

    public static void main(String[] args) {
        int[] prev = new int[2];
        int[] cur = new int[2];

        // Initialize connection variables.
        String host = "mission1.mysql.database.azure.com";
        String database = "votedb";
        String user = "rdwirkala@mission1";
        String password = "30DeanStreet";


        System.out.println("-------mySQL JDBC Connection Testing ---------");
        try {
            Class.forName("com.mysql.jdbc.Driver");

        } catch (ClassNotFoundException e){
            System.out.println("Missing mySQL driver!");
            e.printStackTrace();
            return;
        }

        System.out.println("mySQL Driver Registered!");
        Connection connection = null;

        try {
            String url = String.format("jdbc:mysql://%s/%s", host, database);

            // Set connection properties.
            Properties properties = new Properties();
            properties.setProperty("user", user);
            properties.setProperty("password", password);
            properties.setProperty("useSSL", "true");
            properties.setProperty("verifyServerCertificate", "true");
            properties.setProperty("requireSSL", "false");

            // Get connection
            connection = DriverManager.getConnection(url, properties);
        } catch (SQLException e) {
            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
            return;
        }
        System.out.println("mySQL DB Connected!");

        // Generate query to pull vote counts from db
        prev = pullValues(connection);
        if(prev[0] == -1 || prev[1] == -1) {
            System.out.println("ERROR PULLING DATA, ABORTING");
            try { connection.close();} catch (Exception e) {e.printStackTrace();}
            return;
        }

        // Generate index.html
        if(!(writeFile(prev))) {
            System.out.println("ERROR CREATING INDEX.HTML, ABORTING");
            try { connection.close();} catch (Exception e) {e.printStackTrace();}
            return;
        }

        // Go into loop to constantly check for changes and update index.html accordingly
        while(true) {
            // Delay by a second at the beginning of every loop
            try {
                TimeUnit.SECONDS.sleep(1);
            }
            catch (Exception e) {
                e.printStackTrace();
            }

            // Pull current db values
            cur = pullValues(connection);
            if(cur[0] == -1 || cur[1] == -1) {
                System.out.println("ERROR PULLING DATA, ABORTING");
                try { connection.close();} catch (Exception e) {e.printStackTrace();}
                return;
            }

            // If results are not the same, the db has updated
            if(prev[0] != cur[0] || prev[1] != cur[1]) {
                System.out.println("DB has new vote counts!");
                prev = cur;

                // Generate index.html
                if(!(writeFile(cur))) {
                    System.out.println("ERROR CREATING INDEX.HTML, ABORTING");
                    try { connection.close();} catch (Exception e) {e.printStackTrace();}
                    return;
                }
            }
            else {
                System.out.println("Nothing has updated");
            }
        }
    }

    private static int[] pullValues(Connection connection) {
        int[] retArr = {-1, -1};

        try {
            Statement s = connection.createStatement();
            String query = String.format("SELECT * FROM votes");
            ResultSet result = s.executeQuery(query);

            while(result.next()){
                retArr[0] = result.getInt("yeezy");
                retArr[1] = result.getInt("crocs");
            }

            String out = String.format("Votes for yeezys: %d Votes for crocs: %d", retArr[0], retArr[1]);
            System.out.println(out);

            result.close();
            s.close();
            retArr[0] = retArr[0];
            retArr[1] = retArr[1];
            return retArr;
        } catch (Exception e) {
            e.printStackTrace();
            return retArr;
        }
    }

    private static boolean writeFile(int[] votes) {
        /* Delete and recreate index.html
        File file = new File("C:\\Users\\Roger Wirkala\\Desktop\\index.html");

        if(file.delete())
        {
            System.out.println("index.html deleted successfully");
        }
        else
        {
            System.out.println("index.html was unable to be deleted");
        }*/

        // Create file
        try {
            String fileData = String.format("<!doctype html>\n" +
                    "<html>\n" +
                    "  <head>\n" +
                    "    <title>Election Results</title>\n" +
                    "  </head>\n" +
                    "  <body>\n" +
                    "    <p>\n" +
                    "\tThis is the polling results website for the Shueworld Elections!\n" +
                    "\t<br>\n" +
                    "\tYeezy: %d\n" +
                    "\t<br>\n" +
                    "\tCrocs: %d\n" +
                    "\t<br>\n" +
                    "    </p>\n" +
                    "  </body>\n" +
                    "</html>\n", votes[0], votes[1]);
            FileOutputStream fos = new FileOutputStream("/home/rdwirkala/public_html/index.html");      ///home/rdwirkala/public_html/index.html
            fos.write(fileData.getBytes());
            fos.flush();
            fos.close();
            System.out.println("index.html created successfully");
            return true;
        }
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}