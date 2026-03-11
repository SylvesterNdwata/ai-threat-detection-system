package com.security.rules;

public class LogEvent {
    private long id;
    private String timestamp;
    private String sourceIp;
    private String userId;
    private String endpoint;
    private int statusCode;
    private String userAgent;
    private String message;

    public LogEvent(long id, String timestamp, String sourceIp, String userId, String endpoint, int statusCode, String userAgent, String message) {
        this.id = id;
        this.timestamp = timestamp;
        this.sourceIp = sourceIp;
        this.userId = userId;
        this.endpoint = endpoint;
        this.statusCode = statusCode;
        this.userAgent = userAgent;
        this.message = message;
    }

    public long getId() {
        return id;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public String getSourceIp() {
        return sourceIp;
    }

    public String getUserId() {
        return userId;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public int getStatusCode() {
        return statusCode;
    }

    public String getUserAgent() {
        return userAgent;
    }

    public String getMessage() {
        return message;
    }

    @Override
    public String toString() {
        return "LogEvent{" +
                "id=" + id +
                ", timestamp='" + timestamp + '\'' +
                ", sourceIp='" + sourceIp + '\'' +
                ", userId='" + userId + '\'' +
                ", endpoint='" + endpoint + '\'' +
                ", statusCode=" + statusCode +
                ", userAgent='" + userAgent + '\'' +
                ", message='" + message + '\'' +
                '}';
    }
}
