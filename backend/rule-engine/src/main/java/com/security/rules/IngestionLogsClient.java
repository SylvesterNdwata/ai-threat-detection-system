package com.security.rules;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class IngestionLogsClient {

    private final ObjectMapper mapper;

    public IngestionLogsClient() {
        this.mapper = new ObjectMapper();
    }

    public ArrayList<LogEvent> getLogs() {
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest httpRequest = HttpRequest.newBuilder()
                .GET()
                .uri(URI.create("http://localhost:8001/logs"))
                .build();

        try {
            HttpResponse<String> httpResponse = httpClient.send(httpRequest, HttpResponse.BodyHandlers.ofString());
            
            if (httpResponse.statusCode() != 200) {
                throw new RuntimeException("Failed to fetch logs: ingestion service returned status code " + httpResponse.statusCode());
            }

            return parseLogs(httpResponse.body());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Thread was interrupted while fetching logs", e);
        }
        catch (IOException e) {
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

}
