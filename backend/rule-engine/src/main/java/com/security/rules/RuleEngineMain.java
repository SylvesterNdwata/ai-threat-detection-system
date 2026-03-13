package com.security.rules;

import java.util.ArrayList;

public class RuleEngineMain {

    public static void main(String[] args) {
        System.out.println("Rule engine started...");

        /*LogEvent log = new LogEvent(1, "2024-06-01T12:00:00Z", "192.168.1.1", "user1", "/api/data", 200, "Mozilla/5.0", "Request successful");
        System.out.println(log);

        ArrayList<LogEvent> logEvents = new ArrayList<>();

        FailedLoginBurstRule rule = new FailedLoginBurstRule(logEvents);

        logEvents.add(new LogEvent(2, "2024-06-01T12:01:00Z", "192.168.1.2", "user2", "/api/login", 401, "Mozilla/5.0", "Unauthorized access"));
        logEvents.add(new LogEvent(3, "2024-06-01T12:02:00Z", "192.168.1.2", "user3", "/api/login", 200, "Mozilla/5.0", "Request successful"));
        logEvents.add(new LogEvent(4, "2024-06-01T12:03:00Z", "192.168.1.2", "user4", "/api/login", 403, "Mozilla/5.0", "Unauthorized access"));
        logEvents.add(new LogEvent(5, "2024-06-01T12:04:00Z", "192.168.1.2", "user5", "/api/login", 401, "Mozilla/5.0", "Unauthorized access"));
        logEvents.add(new LogEvent(6, "2024-06-01T12:05:00Z", "192.168.1.2", "user6", "/api/login", 200, "Mozilla/5.0", "Request successful"));
        logEvents.add(new LogEvent(7, "2024-06-01T12:06:00Z", "192.168.1.2", "user7", "/api/login", 401, "Mozilla/5.0", "Unauthorized access"));
        logEvents.add(new LogEvent(8, "2024-06-01T12:07:00Z", "192.168.1.2", "user8", "/api/login", 401, "Mozilla/5.0", "Unauthorized access"));
        logEvents.add(new LogEvent(9, "2024-06-01T12:08:00Z", "192.168.1.2", "user9", "/api/login", 200, "Mozilla/5.0", "Request successful"));


        boolean isSuspicious = rule.suspiciousBruteLogin();
        System.out.println("Suspicious brute login detected: " + isSuspicious);

        boolean isSuspiciousFromSameIP = rule.suspiciousBruteLoginFromSameIP();
        System.out.println("Suspicious brute login from same IP detected: " + isSuspiciousFromSameIP);

        boolean isSuspiciousFromSameIPWithinTimeFrame = rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10);
        System.out.println("Suspicious brute login from same IP within time frame detected: " + isSuspiciousFromSameIPWithinTimeFrame);*/

        IngestionLogsClient client = new IngestionLogsClient();
        ArrayList<LogEvent> logsFromClient = client.getLogs();

        System.out.println("Logs fetched from ingestion service:");
        for (LogEvent event : logsFromClient) {
            System.out.println(event);
        }

        FailedLoginBurstRule rule = new FailedLoginBurstRule(logsFromClient);

        System.out.println("Evaluating rules on fetched logs...");
        boolean isSuspiciousFromClient = rule.suspiciousBruteLogin();
        System.out.println("Suspicious brute login detected from client logs: " + isSuspiciousFromClient);

        boolean isSuspiciousFromSameIPFromClient = rule.suspiciousBruteLoginFromSameIP();
        System.out.println("Suspicious brute login from same IP detected from client logs: " + isSuspiciousFromSameIPFromClient);

        boolean isSuspiciousFromSameIPWithinTimeFrameFromClient = rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10);
        System.out.println("Suspicious brute login from same IP within time frame detected from client logs: " + isSuspiciousFromSameIPWithinTimeFrameFromClient);

        boolean isSuspiciousUnusualEndpointAccess = rule.suspiciousUnusualEndpointAccessByIP(5);
        System.out.println("Suspicious unusual endpoint access detected from client logs: " + isSuspiciousUnusualEndpointAccess);
    
        System.exit(0);
    }
}