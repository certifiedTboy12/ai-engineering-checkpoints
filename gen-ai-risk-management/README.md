# GenAI Risk and Mitigation Analysis

## Scenario 1: The Misleading Test Script

### 1. Primary Risk/Vulnerability

**Infrastructure Vulnerability / Unsafe Code Generation**

The GenAI-generated Python script contains code that could establish an unauthorized communication channel with an external IP address. This creates a security risk because AI-generated code can contain unintended, insecure, or malicious functionality even when the code appears correct.

### 2. Best Mitigation Strategy

**Human Review + Secure Code Testing Environment**

All AI-generated code should undergo **human security review before execution or deployment**. A qualified developer or security tester should inspect the generated code for unexpected network connections, file access, credential handling, and other potentially dangerous operations.

The organization should also execute AI-generated scripts in a **sandboxed or isolated environment** with restricted network access. This ensures that even if the generated code contains a malicious or unsafe instruction, it cannot communicate with unauthorized external systems.

#### Recommended Approach

* Review AI-generated code manually.
* Use static code and security analysis tools.
* Run scripts in a sandbox or isolated test environment.
* Restrict outbound network connections.
* Require approval before executing generated code against production systems.

---

## Scenario 2: The Secret Leak

### 1. Primary Risk/Vulnerability

**Data Exfiltration / Sensitive Data Exposure**

The tester has entered customer names and phone numbers into a commercial web-based LLM. The subsequent appearance of this information in another generated response demonstrates the risk of confidential information being exposed through an external AI service.

### 2. Best Mitigation Strategy

**Data Minimization + Anonymization**

The company should apply **data minimization** before sending information to an external LLM. Only the information necessary for the classification task should be included.

Customer names and phone numbers should be **removed, masked, or anonymized** before the bug report is submitted.

For example:

```text
Original:
Customer John Smith, phone: +234-801-123-4567, reported that the login page crashes.

Anonymized:
Customer [REDACTED], phone: [REDACTED], reported that the login page crashes.
```

The organization should also establish policies preventing employees from entering personally identifiable information (PII) into public or commercial AI services unless the service has been explicitly approved for such data.

#### Recommended Approach

* Remove unnecessary PII.
* Anonymize or pseudonymize sensitive information.
* Use an approved enterprise/private AI environment for confidential data.
* Apply data-loss-prevention controls where possible.
* Train employees on what information may be submitted to AI systems.

---

## Scenario 3: The Corrupted Feedback Loop

### 1. Primary Risk/Vulnerability

**Data Poisoning / Feedback Loop Manipulation**

Developers are intentionally providing false positive feedback to the AI-generated test cases. This contaminates the feedback data used to improve the system. Over time, the AI learns from inaccurate feedback and begins producing lower-quality test cases.

This is an example of **data poisoning**, specifically poisoning of a feedback or evaluation dataset.

### 2. Best Mitigation Strategy

**Human Review + Trusted Evaluation Data**

The organization should prevent a single group of users from being able to freely manipulate the data used to evaluate or improve the AI system.

A **human review process** should be introduced for important evaluation results. Quality scores should be independently verified using predefined criteria rather than being accepted automatically.

The organization can also maintain a **trusted validation dataset** containing professionally reviewed test descriptions. The AI's performance can periodically be compared against this dataset to detect degradation.

#### Recommended Approach

* Require independent human verification of quality scores.
* Use objective scoring criteria and validation rules.
* Maintain a trusted, independently reviewed evaluation dataset.
* Monitor for unusual patterns in feedback.
* Audit who submitted evaluation scores.
* Periodically test whether model quality is improving or deteriorating.

---

## Summary Table

| Scenario                       | Primary Risk/Vulnerability                            | Best Mitigation                                 |
| ------------------------------ | ----------------------------------------------------- | ----------------------------------------------- |
| **1. Misleading Test Script**  | Infrastructure Vulnerability / Unsafe Code Generation | **Human Review + Secure/Sandboxed Environment** |
| **2. Secret Leak**             | Data Exfiltration / Sensitive Data Exposure           | **Data Minimization + Anonymization**           |
| **3. Corrupted Feedback Loop** | Data Poisoning                                        | **Human Review + Trusted Evaluation Dataset**   |

## Key Principle

The three scenarios demonstrate different stages of the GenAI lifecycle:

1. **Generation:** AI-generated code must be reviewed and safely executed.
2. **Input:** Sensitive information should be minimized and anonymized before being provided to an external AI system.
3. **Feedback:** AI evaluation and training data must be protected from manipulation and continuously validated.

Using these controls together helps organizations reduce the risk of **unsafe outputs, confidential-data leakage, and manipulated AI feedback loops**.
