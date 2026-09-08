package com.security.rules;

public class RuleResult {
    private final String ruleName;
    private final String sourceIp;
    private final String detail;

    public RuleResult(String ruleName, String sourceIp, String detail) {
        this.ruleName = ruleName;
        this.sourceIp = sourceIp;
        this.detail = detail;
    }

    public String getRuleName() {
        return ruleName;
    }

    public String getSourceIp() {
        return sourceIp;
    }

    public String getDetail() {
        return detail;
    }

    @Override 
    public String toString() {
        return "RuleResult{rule=" + ruleName + ", ip=" + sourceIp + ", detail='" + detail + "'}";
    }
}
