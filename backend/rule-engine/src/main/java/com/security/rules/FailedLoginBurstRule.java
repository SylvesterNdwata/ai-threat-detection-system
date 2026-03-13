package com.security.rules;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

public class FailedLoginBurstRule {

    private final ArrayList<LogEvent> logEvents;

    public FailedLoginBurstRule(ArrayList<LogEvent> logEvents) {
        this.logEvents = logEvents;
    }

    public boolean suspiciousBruteLogin() {
        // Implementation of logic to detect failed login bursts
        int failedAttempts = 0;
        for (LogEvent event : this.logEvents) {
            if (isLoginEndpoint(event) && isFailedLogin(event)) {
                failedAttempts++;
            }
        }
        if (failedAttempts >= 5) {
            System.out.println("Suspicious activity detected: " + failedAttempts + " failed login attempts.");
            return true;
        }

        return false;
    }

    public boolean suspiciousBruteLoginFromSameIP() {
        // Implementation of logic to detect failed login bursts from the same IP
        HashMap<String, Integer> ipFailedAttempts = new HashMap<>();
        for (LogEvent event : this.logEvents) {
            if (isLoginEndpoint(event) && isFailedLogin(event)) {
                String ip = event.getSourceIp();
                int newCount = ipFailedAttempts.getOrDefault(ip, 0) + 1;
                ipFailedAttempts.put(ip, newCount);

                if (newCount >= 5) {
                    System.out.println("Suspicious activity detected from IP: " + ip + " with " + newCount + " failed attempts.");
                    return true;
                }
            }
        }
        return false;
    }

    public boolean suspiciousBruteLoginFromSameIPWithinTimeFrame(int threshold, int timeFrame) {
        HashMap<String, ArrayList<Instant>> ipFailedAttempts = new HashMap<>();

        for (LogEvent event : this.logEvents) {
            boolean isFailedLogin = isLoginEndpoint(event) && isFailedLogin(event);

            if (!isFailedLogin) {
                continue;
            }

            String ip = event.getSourceIp();
            Instant eventTime = Instant.parse(event.getTimestamp());

            ArrayList<Instant> attempts = ipFailedAttempts.getOrDefault(ip, new ArrayList<>());
            attempts.add(eventTime);

            Instant windowStart = eventTime.minus(Duration.ofMinutes(timeFrame));
            attempts.removeIf(attemptTime -> attemptTime.isBefore(windowStart));

            ipFailedAttempts.put(ip, attempts);

            if (attempts.size() >= threshold) {
                System.out.println("Suspicious activity detected from IP: " + ip + " with " + attempts.size() + " failed attempts within " + timeFrame + " minutes.");
                return true;
            }

        }

        return false;
    }

    public boolean suspiciousUnusualEndpointAccessByIP(int distinctEndpointThreshold) {
        HashMap<String, HashSet<String>> ipEndpoints = new HashMap<>();

        for (LogEvent event: this.logEvents) {
            String ip = event.getSourceIp();
            String endpoint = event.getEndpoint();
            HashSet<String> endpointsForIp = ipEndpoints.getOrDefault(ip, new HashSet<>());
            endpointsForIp.add(endpoint);
            ipEndpoints.put(ip, endpointsForIp);

            if (endpointsForIp.size() >= distinctEndpointThreshold) {
                System.out.println("Suspicious activity detected from IP: " + ip + " accessing " + endpointsForIp.size() + " distinct endpoints.");
                return true;
            }
        }

        return false;
    }

    // Incomplete method for detecting port scan patterns based on distinct endpoints accessed from the same IP within a time frame
    public boolean suspiciousPortScanPattern(int distinctEndpointThreshold, int timeFrameMinutes) {
        HashMap<String, ArrayList<LogEvent>> ipEvents = new HashMap<>();

        for (LogEvent event: this.logEvents) {
            String ip = event.getSourceIp();

            ArrayList<LogEvent> eventsForIp = ipEvents.getOrDefault(ip, new ArrayList<>());
            eventsForIp.add(event);
            ipEvents.put(ip, eventsForIp);
        }
        return false;
    }

    private boolean isLoginEndpoint(LogEvent event) {
        return event.getEndpoint().equals("/api/login") || event.getEndpoint().equals("/login");
    }

    private boolean isFailedLogin(LogEvent event) {
        return event.getStatusCode() == 401 || event.getStatusCode() == 403;
    }
}
