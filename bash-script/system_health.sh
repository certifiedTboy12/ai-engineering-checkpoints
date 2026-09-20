#!/bin/bash

# ==========================================
# System Health Monitoring Script
# ==========================================

LOG_FILE="/var/log/system_health.log"
TEMP_FILE="/tmp/system_health_report.txt"

# Create a timestamp
timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Add timestamp and message to report
log_section() {
    echo ""
    echo "[$(timestamp)] =========================================="
    echo "[$(timestamp)] $1"
    echo "[$(timestamp)] =========================================="
}

# Start a new report
{
    echo "=========================================================="
    echo "          SYSTEM HEALTH REPORT"
    echo "=========================================================="
    echo "Report generated: $(timestamp)"
    echo ""

    # ------------------------------------------
    # 1. System Information
    # ------------------------------------------
    log_section "SYSTEM INFORMATION"

    echo "Hostname:"
    hostname

    echo ""
    echo "Operating System:"
    if command -v lsb_release >/dev/null 2>&1; then
        lsb_release -a 2>/dev/null
    else
        cat /etc/os-release
    fi

    echo ""
    echo "Kernel Version:"
    uname -r

    echo ""
    echo "System Uptime:"
    uptime

    # ------------------------------------------
    # 2. CPU and Memory Usage
    # ------------------------------------------
    log_section "CPU AND MEMORY USAGE"

    echo "Top 5 CPU-Consuming Processes:"
    ps aux --sort=-%cpu | head -n 6

    echo ""
    echo "Memory Usage:"
    free -h

    echo ""
    echo "CPU Summary:"
    top -bn1 | head -n 5

    # ------------------------------------------
    # 3. Disk Usage
    # ------------------------------------------
    log_section "DISK USAGE"

    echo "Disk Partitions:"
    df -h

    echo ""
    echo "Disk Usage Warnings:"

    # Check partitions above 80% usage
    df -P -x tmpfs -x devtmpfs | awk '
    NR > 1 {
        usage = $5
        gsub("%", "", usage)

        if (usage > 80) {
            print "WARNING: " $6 " is " usage "% full"
            warning_found=1
        }
    }

    END {
        if (!warning_found)
            print "OK: No partition is above 80% usage."
    }'

    # ------------------------------------------
    # 4. Network Status
    # ------------------------------------------
    log_section "NETWORK STATUS"

    echo "Network Interfaces and IP Addresses:"
    ip a

    echo ""
    echo "Connectivity Test:"
    
    if ping -c 2 -W 2 google.com >/dev/null 2>&1; then
        echo "OK: Internet connectivity is available."
        echo ""
        ping -c 2 google.com
    else
        echo "WARNING: Unable to reach google.com."
    fi

    # ------------------------------------------
    # 5. Running Services
    # ------------------------------------------
    log_section "RUNNING SERVICES"

    echo "Important Services:"

    check_service() {
        SERVICE=$1

        if systemctl list-unit-files | grep -q "^${SERVICE}.service"; then
            echo ""
            echo "Service: $SERVICE"
            systemctl is-active "$SERVICE" 2>/dev/null || true
            systemctl is-enabled "$SERVICE" 2>/dev/null || true
        else
            echo ""
            echo "Service: $SERVICE"
            echo "Not installed or not available."
        fi
    }

    check_service "sshd"
    check_service "apache2"
    check_service "nginx"

    # ------------------------------------------
    # End of Report
    # ------------------------------------------
    echo ""
    log_section "REPORT COMPLETE"
    echo "Report generated at: $(timestamp)"

} | tee "$TEMP_FILE"

# ------------------------------------------
# Save report to /var/log
# ------------------------------------------

if [ "$EUID" -eq 0 ]; then
    cat "$TEMP_FILE" >> "$LOG_FILE"
else
    sudo sh -c "cat '$TEMP_FILE' >> '$LOG_FILE'"
fi

# Remove temporary file
rm -f "$TEMP_FILE"

echo ""
echo "=========================================================="
echo "System health check completed."
echo "Log saved to: $LOG_FILE"
echo "=========================================================="