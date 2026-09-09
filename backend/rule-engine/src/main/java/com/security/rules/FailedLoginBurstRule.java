package com.security.rules;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

public class FailedLoginBurstRule {

    private final ArrayList<LogEvent> logEvents;

    public FailedLoginBurstRule(ArrayList<LogEvent> logEvents) {
        this.logEvents = logEvents;
    }

    public List<RuleResult> suspiciousBruteLogin() {
        // Implementation of logic to detect failed login bursts
        List<RuleResult> results = new ArrayList<>();
        int failedAttempts = 0;
        for (LogEvent event : this.logEvents) {
            if (isLoginEndpoint(event) && isFailedLogin(event)) {
                failedAttempts++;
            }
        }
        if (failedAttempts >= 5) {
            results.add(new RuleResult("FailedLoginBurst", null,
                    failedAttempts + " failed login attempts detected."));
        }

        return results;
    }

    public List<RuleResult> suspiciousBruteLoginFromSameIP() {
        // Implementation of logic to detect failed login bursts from the same IP
        HashMap<String, Integer> ipFailedAttempts = new HashMap<>();
        List<RuleResult> results = new ArrayList<>();
        HashSet<String> alreadyFlagged = new HashSet<>();

        for (LogEvent event : this.logEvents) {
            if (isLoginEndpoint(event) && isFailedLogin(event)) {
                String ip = event.getSourceIp();
                int newCount = ipFailedAttempts.getOrDefault(ip, 0) + 1;
                ipFailedAttempts.put(ip, newCount);

                if (newCount >= 5 && alreadyFlagged.add(ip)) {
                    results.add(new RuleResult("SuspiciousBruteLoginFromSameIP", ip,
                            newCount + " failed attempts from this IP."));
                }
            }
        }
        return results;
    }

    public List<RuleResult> suspiciousBruteLoginFromSameIPWithinTimeFrame(int threshold, int timeFrame) {
        HashMap<String, ArrayList<Instant>> ipFailedAttempts = new HashMap<>();
        List<RuleResult> results = new ArrayList<>();
        HashSet<String> alreadyFlagged = new HashSet<>();

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

            if (attempts.size() >= threshold && alreadyFlagged.add(ip)) {
                results.add(new RuleResult("SuspiciousBruteLoginFromSameIPWithinTimeFrame", ip,
                        attempts.size() + " failed attempts from this IP within " + timeFrame + " minutes."));
            }

        }

        return results;
    }

    public List<RuleResult> suspiciousUnusualEndpointAccessByIP(int distinctEndpointThreshold) {
        HashMap<String, HashSet<String>> ipEndpoints = new HashMap<>();
        List<RuleResult> results = new ArrayList<>();
        HashSet<String> alreadyFlagged = new HashSet<>();

        for (LogEvent event : this.logEvents) {
            String ip = event.getSourceIp();
            String endpoint = event.getEndpoint();
            HashSet<String> endpointsForIp = ipEndpoints.getOrDefault(ip, new HashSet<>());
            endpointsForIp.add(endpoint);
            ipEndpoints.put(ip, endpointsForIp);

            if (endpointsForIp.size() >= distinctEndpointThreshold && alreadyFlagged.add(ip)) {
                results.add(new RuleResult("SuspiciousUnusualEndpointAccessByIP", ip,
                        endpointsForIp.size() + " distinct endpoints accessed."));
            }
        }

        return results;
    }

    public List<RuleResult> suspiciousPortScanPattern(int distinctEndpointThreshold, int timeFrameMinutes) {
        HashMap<String, ArrayList<LogEvent>> ipEvents = new HashMap<>();
        List<RuleResult> results = new ArrayList<>();
        HashSet<String> alreadyFlagged = new HashSet<>();

        for (LogEvent event : this.logEvents) {
            String ip = event.getSourceIp();
            Instant eventTime = Instant.parse(event.getTimestamp());

            ArrayList<LogEvent> eventsForIp = ipEvents.getOrDefault(ip, new ArrayList<>());
            eventsForIp.add(event);

            Instant windowStart = eventTime.minus(Duration.ofMinutes(timeFrameMinutes));
            eventsForIp.removeIf(e -> Instant.parse(e.getTimestamp()).isBefore(windowStart));

            ipEvents.put(ip, eventsForIp);

            HashSet<String> distinctEndpoints = new HashSet<>();
            for (LogEvent e : eventsForIp) {
                distinctEndpoints.add(e.getEndpoint());
            }

            if (distinctEndpoints.size() >= distinctEndpointThreshold && alreadyFlagged.add(ip)) {
                results.add(new RuleResult("SuspiciousPortScanPattern", ip,
                        distinctEndpoints.size() + " distinct endpoints accessed within " + timeFrameMinutes + " minutes."));
            }
        }
        return results;
    }

    public List<RuleResult> suspiciousCredentialStuffingByIP(int distinctUserThreshold, int timeFrameMinutes) {
        HashMap<String, ArrayList<LogEvent>> ipEvents = new HashMap<>();
        List<RuleResult> results = new ArrayList<>();
        HashSet<String> alreadyFlagged = new HashSet<>();

        for (LogEvent event : this.logEvents) {
            if (!isLoginEndpoint(event) || !isFailedLogin(event)) {
                continue;
            }
            String userId = event.getUserId();
            if (userId == null) {
                continue;
            }

            String ip = event.getSourceIp();
            Instant eventTime = Instant.parse(event.getTimestamp());

            ArrayList<LogEvent> eventsForIp = ipEvents.getOrDefault(ip, new ArrayList<>());
            eventsForIp.add(event);

            Instant windowStart = eventTime.minus(Duration.ofMinutes(timeFrameMinutes));
            eventsForIp.removeIf(e -> Instant.parse(e.getTimestamp()).isBefore(windowStart));

            ipEvents.put(ip, eventsForIp);

            HashSet<String> distinctUsers = new HashSet<>();
            for (LogEvent e : eventsForIp) {
                distinctUsers.add(e.getUserId());
            }

            if (distinctUsers.size() >= distinctUserThreshold && alreadyFlagged.add(ip)) {
                results.add(new RuleResult("SuspiciousCredentialStuffingByIP", ip,
                        distinctUsers.size() + " distinct usernames attempted from this IP within " + timeFrameMinutes + " minutes."));
            }
        }
        return results;
    }

    public List<RuleResult> evaluateAllRules() {
        List<RuleResult> allResults = new ArrayList<>();
        allResults.addAll(suspiciousBruteLogin());
        allResults.addAll(suspiciousBruteLoginFromSameIP());
        allResults.addAll(suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
        allResults.addAll(suspiciousUnusualEndpointAccessByIP(5));
        allResults.addAll(suspiciousPortScanPattern(5, 10));
        allResults.addAll(suspiciousCredentialStuffingByIP(5, 10));
        return allResults;
    }

    private boolean isLoginEndpoint(LogEvent event) {
        return event.getEndpoint().equals("/api/login") || event.getEndpoint().equals("/login");
    }

    private boolean isFailedLogin(LogEvent event) {
        return event.getStatusCode() == 401 || event.getStatusCode() == 403;
    }
}
