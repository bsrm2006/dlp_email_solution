-- DLP Database Schema

-- Exceptions Table
CREATE TABLE IF NOT EXISTS exceptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    value TEXT NOT NULL,
    reason TEXT,
    severity TEXT DEFAULT 'low',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiration DATETIME
);

-- Email Scan Logs Table
CREATE TABLE IF NOT EXISTS email_scan_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender TEXT,
    recipient TEXT,
    status TEXT,
    violation_type TEXT,
    details TEXT,
    severity TEXT
);

-- Attachment Scan Logs Table
CREATE TABLE IF NOT EXISTS attachment_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    filename TEXT,
    file_size INTEGER,
    mime_type TEXT,
    scan_result TEXT,
    violation_details TEXT
);

-- User Audit Log
CREATE TABLE IF NOT EXISTS user_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);