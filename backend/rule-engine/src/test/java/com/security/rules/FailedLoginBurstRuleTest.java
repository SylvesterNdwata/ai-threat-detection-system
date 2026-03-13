package com.security.rules;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

public class FailedLoginBurstRuleTest {

    private LogEvent makeEvent(String ip, String endpoint, int status, String timestamp) {
        return new LogEvent(1, timestamp, ip, "user1", endpoint, status, "Mozilla/5.0", "test");
    }

    @Test
    void shouldReturnTrueWhenFiveOrMoreTotalFailedLogins() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            events.add(makeEvent("1.1.1." + i, "/api/login", 401, "2026-03-12T10:00:00Z"));
        }
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertTrue(rule.suspiciousBruteLogin());
    }

    @Test
    void shouldReturnFalseWhenFewerThanFiveTotalFailedLogins() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            events.add(makeEvent("1.1.1." + i, "/api/login", 401, "2026-03-12T10:00:00Z"));
        }
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLogin());
    }

    @Test
    void shouldNotCountSuccessfulLoginsAsFailed() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            events.add(makeEvent("1.1.1.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        }
        events.add(makeEvent("1.1.1.1", "/api/login", 200, "2026-03-12T10:00:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLogin());
    }

    @Test
    void shouldCountBothSlashLoginEndpoints() {
        ArrayList<LogEvent> events = new ArrayList<>();
        events.add(makeEvent("1.1.1.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("1.1.1.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("1.1.1.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("1.1.1.1", "/login", 403, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("1.1.1.1", "/login", 403, "2026-03-12T10:00:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertTrue(rule.suspiciousBruteLogin());
    }

    @Test
    void shouldReturnTrueWhenFiveFailuresFromSameIP() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            events.add(makeEvent("192.168.1.10", "/api/login", 401, "2026-03-12T10:00:00Z"));
        }
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertTrue(rule.suspiciousBruteLoginFromSameIP());
    }

    @Test
    void shouldReturnFalseWhenFailuresSpreadAcrossDifferentIPs() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            events.add(makeEvent("10.0.0.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
            events.add(makeEvent("10.0.0.2", "/api/login", 401, "2026-03-12T10:00:00Z"));
            events.add(makeEvent("10.0.0.3", "/api/login", 401, "2026-03-12T10:00:00Z"));
        }
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLoginFromSameIP());
    }

    @Test
    void shouldTriggerOnlyOnIPThatReachesThreshold() {
        ArrayList<LogEvent> events = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            events.add(makeEvent("10.0.0.1", "/api/login", 403, "2026-03-12T10:00:00Z"));
        }
        for (int i = 0; i < 5; i++) {
            events.add(makeEvent("10.0.0.2", "/api/login", 403, "2026-03-12T10:00:00Z"));
        }
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertTrue(rule.suspiciousBruteLoginFromSameIP());
    }

    @Test
    void shouldReturnTrueWhenFiveAttemptsFromSameIPWithinTimeFrame() {
        ArrayList<LogEvent> events = new ArrayList<>();
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:03:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:04:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertTrue(rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
    }

    @Test
    void shouldReturnFalseWhenAttemptsSpreadOutBeyondTimeFrame() {
        ArrayList<LogEvent> events = new ArrayList<>();
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T11:00:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T12:00:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T13:00:00Z"));
        events.add(makeEvent("172.16.0.1", "/api/login", 401, "2026-03-12T14:00:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
    }

    @Test
    void shouldReturnFalseWhenBurstSpreadAcrossDifferentIPsWithinTimeFrame() {
        ArrayList<LogEvent> events = new ArrayList<>();
        events.add(makeEvent("192.168.1.1", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.1", "/api/login", 401, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("192.168.1.1", "/api/login", 401, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.1", "/api/login", 401, "2026-03-12T10:03:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:03:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
    }

    @Test
    void shouldReturnFalseWhenFourFailedAttemptsOccurwithinTenMinutes() {
        ArrayList<LogEvent> events = new ArrayList<>();
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:04:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/login", 401, "2026-03-12T10:10:00Z"));
        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);
        assertFalse(rule.suspiciousBruteLoginFromSameIPWithinTimeFrame(5, 10));
    }

    @Test
    void shouldDetectUnusualEndpointAccessByIP() {
        ArrayList<LogEvent> events = new ArrayList<>();

        events.add(makeEvent("192.168.1.2", "/api/data", 200, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/admin", 200, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/internal", 200, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.2", "/health", 200, "2026-03-12T10:03:00Z"));
        events.add(makeEvent("192.168.1.2", "/metrics", 200, "2026-03-12T10:04:00Z"));
        events.add(makeEvent("192.168.1.2", "/config", 200, "2026-03-12T10:05:00Z"));

        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);

        assertTrue(rule.suspiciousUnusualEndpointAccessByIP(6));
    }

    @Test
    void shouldReturnFalseWhenUnusualEndpointAccessByIPIsLessThanThreshold() {
        ArrayList<LogEvent> events = new ArrayList<>();

        events.add(makeEvent("192.168.1.2", "/api/data", 200, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/admin", 200, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/internal", 200, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.2", "/health", 200, "2026-03-12T10:03:00Z"));
        events.add(makeEvent("192.168.1.2", "/metrics", 200, "2026-03-12T10:04:00Z"));

        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);

        assertFalse(rule.suspiciousUnusualEndpointAccessByIP(6));
    }

    @Test
    void shouldDetectPortScanPatternWhenManyDistinctEndpointsHitQuickly() {
        ArrayList<LogEvent> events = new ArrayList<>();

        events.add(makeEvent("192.168.1.2", "/api/data", 200, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/admin", 200, "2026-03-12T10:01:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/internal", 200, "2026-03-12T10:02:00Z"));
        events.add(makeEvent("192.168.1.2", "/health", 200, "2026-03-12T10:03:00Z"));
        events.add(makeEvent("192.168.1.2", "/metrics", 200, "2026-03-12T10:04:00Z"));

        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);

        assertTrue(rule.suspiciousPortScanPattern(5, 10));
    }

    @Test
    void shouldNotDetectPortScanWhenActivityIsOutsideTimeWindow() {
        ArrayList<LogEvent> events = new ArrayList<>();

        events.add(makeEvent("192.168.1.2", "/api/data", 200, "2026-03-12T10:00:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/admin", 200, "2026-03-12T10:11:00Z"));
        events.add(makeEvent("192.168.1.2", "/api/internal", 200, "2026-03-12T10:22:00Z"));
        events.add(makeEvent("192.168.1.2", "/health", 200, "2026-03-12T10:33:00Z"));
        events.add(makeEvent("192.168.1.2", "/metrics", 200, "2026-03-12T10:44:00Z"));

        FailedLoginBurstRule rule = new FailedLoginBurstRule(events);

        assertFalse(rule.suspiciousPortScanPattern(5, 10));
    }
}
