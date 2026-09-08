package com.security.rules;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class RuleEngineMain {

    private static final int ALERT_COOLDOWN_MINUTES = 20;

    /**
     * @param args
     * @throws InterruptedException
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Rule engine started...");
        IngestionLogsClient client = new IngestionLogsClient();
        Map<String, Instant> lastAlertedAt = new HashMap<>();

        while (true) {
            try {
                ArrayList<LogEvent> logsFromClient = client.getLogs(20);

                System.out.println("Logs fetched from ingestion service:");
                for (LogEvent event : logsFromClient) {
                    System.out.println(event);
                }

                FailedLoginBurstRule rule = new FailedLoginBurstRule(logsFromClient);

                System.out.println("Evaluating rules on fetched logs...");
                List<RuleResult> allResults = new ArrayList<>();
                allResults.addAll(rule.suspiciousBruteLogin());
                allResults.addAll(rule.suspiciousBruteLoginFromSameIP());
                allResults.addAll(rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
                allResults.addAll(rule.suspiciousUnusualEndpointAccessByIP(5));
                allResults.addAll(rule.suspiciousPortScanPattern(5, 10));

                Instant now = Instant.now();
                for (RuleResult result : allResults) {
                    String key = result.getRuleName() + "|" + (result.getSourceIp() == null ? "GLOBAL" : result.getSourceIp());
                    Instant lastAlert = lastAlertedAt.get(key);

                    if (lastAlert != null && Duration.between(lastAlert, now).toMinutes() < ALERT_COOLDOWN_MINUTES) {
                        System.out.println("SUPPRESSED (cooldown): " + result);
                        continue;
                    }

                    System.out.println("ALERT: " + result);
                    client.postAlert(result);
                    lastAlertedAt.put(key, now);
                }
            } catch (RuntimeException e) {
                System.err.println("Rule engine iteration failed: " + e.getMessage());
                e.printStackTrace();
            }

            Thread.sleep(5000);
        }
    }
}
