package com.security.rules;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class IngestionLogsClient {

    private final ObjectMapper mapper;
    private final HttpClient httpClient;

    public IngestionLogsClient() {
        this.mapper = new ObjectMapper();
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .build();
    }

    public ArrayList<LogEvent> getLogs(int sinceMinutes) {
        HttpRequest httpRequest = HttpRequest.newBuilder()
                .GET()
                .uri(URI.create("http://localhost:8001/logs?since_minutes=" + sinceMinutes))
                .build();

        try {
            HttpResponse<String> httpResponse = this.httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());

            if (httpResponse.statusCode() != 200) {
                throw new RuntimeException("Failed to fetch logs: ingestion service returned status code " + httpResponse.statusCode());
            }

            return parseLogs(httpResponse.body());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Thread was interrupted while fetching logs", e);
        } catch (IOException e) {
            throw new RuntimeException("Failed to fetch logs", e);
        }
    }

    public ArrayList<LogEvent> parseLogs(String jsonBody) {
        ArrayList<LogEvent> logEvents = new ArrayList<>();
        try {
            JsonNode rootNode = mapper.readTree(jsonBody);

            if (!rootNode.isArray()) {
                throw new RuntimeException("Expected JSON array of log events");
            }

            for (JsonNode item : rootNode) {
                long id = item.path("id").asLong();
                String timestamp = item.path("timestamp").asText();
                String sourceIp = item.path("source_ip").asText();
                String userId = item.path("user_id").isNull() ? null : item.path("user_id").asText();
                String endpoint = item.path("endpoint").asText();
                int statusCode = item.path("status_code").asInt();
                String userAgent = item.path("user_agent").isNull() ? null : item.path("user_agent").asText();
                String message = item.path("message").asText();

                LogEvent event = new LogEvent(id, timestamp, sourceIp, userId, endpoint, statusCode, userAgent, message);
                logEvents.add(event);
            }
        } catch (IOException e) {
            throw new RuntimeException("Failed to parse logs", e);
        }
        return logEvents;
    }

    public void postAlert(RuleResult result) {
        ObjectNode payload = this.mapper.createObjectNode();
        payload.put("rule_name", result.getRuleName());
        payload.put("source_ip", result.getSourceIp());
        payload.put("detail", result.getDetail());

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:8001/alerts"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                .build();

        try {
            HttpResponse<String> response = this.httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != 200) {
                throw new RuntimeException("Failed to post alert: status code " + response.statusCode());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Interrupted while posting alert", e);
        } catch (IOException e) {
            throw new RuntimeException("Failed to post alert", e);
        }
    }

}
