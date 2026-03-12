package com.security.rules;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;

public class FailedLoginBurstRule {

    private final ArrayList<LogEvent> logEvents;

    public FailedLoginBurstRule(ArrayList<LogEvent> logEvents) {
        this.logEvents = logEvents;
    }

    public boolean suspiciousBruteLogin() {
        // Implementation of logic to detect failed login bursts
        int failedAttempts = 0;
        for (LogEvent event : this.logEvents) {
            if ((event.getEndpoint().equals("/api/login") || event.getEndpoint().equals("/login")) && (event.getStatusCode() == 401 || event.getStatusCode() == 403)) {
                failedAttempts++;
            }
        }
        return failedAttempts >= 5;
    }

    public boolean suspiciousBruteLoginFromSameIP() {
        // Implementation of logic to detect failed login bursts from the same IP
        HashMap<String, Integer> ipFailedAttempts = new HashMap<>();
        for (LogEvent event : this.logEvents) {
            if ((event.getEndpoint().equals("/api/login") || event.getEndpoint().equals("/login")) && (event.getStatusCode() == 401 || event.getStatusCode() == 403)) {
                String ip = event.getSourceIp();
                int newCount = ipFailedAttempts.getOrDefault(ip, 0) + 1;
                ipFailedAttempts.put(ip, newCount);

                if (newCount >= 5) {
                    return true;
                }
            }
        }
        return false;
    }

    public boolean suspiciousBruteLoginFromSameIPWithinTimeFrame(int threshold, int timeFrame) {
        HashMap<String, ArrayList<Instant>> ipFailedAttempts = new HashMap<>();

        for (LogEvent event : this.logEvents) {
            boolean isFailedLogin = (event.getEndpoint().equals("/api/login") || event.getEndpoint().equals("/login")) && 
                                    (event.getStatusCode() == 401 || event.getStatusCode() == 403);

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
                return true;
            }

        }

        return false;
    }
}
