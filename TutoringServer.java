import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Helen's English Studio — Java Standalone HTTP & REST API Server
 * 
 * Compile & run directly with Java 11+:
 *   java TutoringServer.java
 * 
 * Serves the interactive portal on:
 *   http://127.0.0.1:8085/
 */
public class TutoringServer {

    private static final int PORT = 8085;
    private static final String HTML_FILE = "index.html";

    // In-memory JSON stores seeded with default data
    private static String studentsJson = """
    [
      {"id":"s1","name":"Maya Ronen","grade":"9th Grade","rate":45.0,"phone":"Sarah (Mom) 054-234-5678","wa":"972542345678","notes":"Grammar tenses and speaking confidence.","password":"student123"},
      {"id":"s2","name":"Daniel Klein","grade":"11th Grade (5 Units)","rate":50.0,"phone":"David (Dad) 050-987-6543","wa":"972509876543","notes":"Bagrut Module E practice and unseen texts.","password":"student123"},
      {"id":"s3","name":"Liam Shahar","grade":"7th Grade","rate":40.0,"phone":"Rachel 052-333-8899","wa":"972523338899","notes":"Reading comprehension and school homework.","password":"student123"},
      {"id":"s4","name":"Emma Tal","grade":"10th Grade","rate":45.0,"phone":"Noa 053-444-1122","wa":"972534441122","notes":"Essay writing structure and rich vocabulary.","password":"student123"},
      {"id":"s5","name":"Noah Ben-David","grade":"8th Grade","rate":40.0,"phone":"Itai 050-555-7788","wa":"972505557788","notes":"Irregular verbs drill and conversational fluency.","password":"student123"}
    ]
    """;

    private static String lessonsJson = """
    [
      {"id":"l1","studentId":"s1","studentName":"Maya Ronen","weekId":"2026-W41","day":"Sunday","date":"2026-10-04","startTime":"16:00","endTime":"17:00","rate":45.0,"payment":"Paid","method":"Bit","status":"Completed","topic":"Present Perfect & Vocabulary","location":"Studio (In-Person)"},
      {"id":"l2","studentId":"s3","studentName":"Liam Shahar","weekId":"2026-W41","day":"Sunday","date":"2026-10-04","startTime":"17:15","endTime":"18:15","rate":40.0,"payment":"Paid","method":"Cash","status":"Completed","topic":"School Book Chapter 4","location":"Studio (In-Person)"},
      {"id":"l3","studentId":"s2","studentName":"Daniel Klein","weekId":"2026-W41","day":"Monday","date":"2026-10-05","startTime":"16:30","endTime":"17:30","rate":50.0,"payment":"Unpaid","method":"Bank Transfer","status":"Completed","topic":"5-Unit Module E Practice","location":"Online (Zoom / Meet)"},
      {"id":"l4","studentId":"s4","studentName":"Emma Tal","weekId":"2026-W41","day":"Tuesday","date":"2026-10-06","startTime":"15:30","endTime":"16:30","rate":45.0,"payment":"Paid","method":"PayBox","status":"Completed","topic":"Opinion Essay Writing","location":"Studio (In-Person)"},
      {"id":"l5","studentId":"s5","studentName":"Noah Ben-David","weekId":"2026-W41","day":"Wednesday","date":"2026-10-07","startTime":"16:00","endTime":"17:00","rate":40.0,"payment":"Unpaid","method":"Bit","status":"Confirmed","topic":"Irregular Verbs Drill","location":"Studio (In-Person)"},
      {"id":"l6","studentId":"s1","studentName":"Maya Ronen","weekId":"2026-W41","day":"Thursday","date":"2026-10-08","startTime":"16:30","endTime":"17:30","rate":45.0,"payment":"Unpaid","method":"Bit","status":"Confirmed","topic":"Conversation & Speech","location":"Online (Zoom / Meet)"},
      {"id":"l7","studentId":"s2","studentName":"Daniel Klein","weekId":"2026-W41","day":"Friday","date":"2026-10-09","startTime":"11:00","endTime":"12:00","rate":50.0,"payment":"Unpaid","method":"Bank Transfer","status":"Confirmed","topic":"Literature Analysis","location":"Studio (In-Person)"}
    ]
    """;

    private static String requestsJson = """
    [
      {"id":"r1","studentId":"s1","studentName":"Maya Ronen","lessonId":"l6","lessonSummary":"Thursday (Oct 8) @ 16:30","requestType":"Reschedule","message":"Hi Teacher Helen! I have a school biology exam on Thursday afternoon. Could we please move our lesson to Thursday at 18:00 or Friday morning?","dateSubmitted":"2026-10-06T18:30:00Z","status":"Answered","teacherReply":"Hi Maya! Yes, Thursday at 18:00 works well for me. I updated the schedule for you.","teacherReplyDate":"2026-10-06T19:15:00Z"},
      {"id":"r2","studentId":"s5","studentName":"Noah Ben-David","lessonId":"l5","lessonSummary":"Wednesday (Oct 7) @ 16:00","requestType":"Cancel","message":"Hello Helen, Noah is not feeling well with a fever today and cannot attend. Can we make it up next week?","dateSubmitted":"2026-10-07T08:15:00Z","status":"Pending","teacherReply":"","teacherReplyDate":null}
    ]
    """;

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        // Static Frontend
        server.createContext("/", new StaticFileHandler());

        // API Endpoints
        server.createContext("/api/health", exchange -> sendJson(exchange, "{\"status\":\"ok\",\"engine\":\"Java 17 HttpServer\"}"));
        server.createContext("/api/students", exchange -> sendJson(exchange, studentsJson));
        server.createContext("/api/lessons", exchange -> sendJson(exchange, lessonsJson));
        server.createContext("/api/requests", exchange -> sendJson(exchange, requestsJson));
        
        server.createContext("/api/auth/login", exchange -> {
            if ("POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                String body = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
                if (body.contains("\"role\":\"teacher\"")) {
                    sendJson(exchange, "{\"role\":\"teacher\",\"name\":\"Helen\"}");
                } else {
                    sendJson(exchange, "{\"role\":\"student\",\"studentId\":\"s1\",\"name\":\"Maya Ronen\"}");
                }
            } else {
                sendJson(exchange, "{\"status\":\"ready\"}");
            }
        });

        server.setExecutor(null);
        System.out.println("==================================================");
        System.out.println(" Helen's English Studio — Java Server Started!");
        System.out.println(" Open in your browser: http://127.0.0.1:" + PORT);
        System.out.println("==================================================");
        server.start();
    }

    private static void sendJson(HttpExchange exchange, String json) throws IOException {
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
        exchange.sendResponseHeaders(200, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    static class StaticFileHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            Path path = Paths.get(HTML_FILE);
            if (!Files.exists(path)) {
                // Try looking relative to current directory
                path = Paths.get(".", HTML_FILE);
            }

            if (Files.exists(path)) {
                byte[] htmlBytes = Files.readAllBytes(path);
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                exchange.sendResponseHeaders(200, htmlBytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(htmlBytes);
                }
            } else {
                String error = "<h1>Helen's English Studio</h1><p>" + HTML_FILE + " not found.</p>";
                byte[] bytes = error.getBytes(StandardCharsets.UTF_8);
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                exchange.sendResponseHeaders(404, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            }
        }
    }
}
