package com.security.rules;

import java.util.HashMap;
import java.util.List;

public class FailedLoginBurstRule {

    private final List<LogEvent> logEvents;

    public FailedLoginBurstRule(List<LogEvent> logEvents) {
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
}