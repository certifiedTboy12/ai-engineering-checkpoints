# Basic Prompting Techniques

## What You're Aiming For

**Master Basic Prompting Techniques**

## 1. Zero-Shot Prompt – Email Classification

A **zero-shot prompt** asks the AI to perform a task without providing examples of how the task should be completed.

### Prompt

> Classify the following email as **Work, Personal, or Spam**:
>
> "Don't forget the team meeting at 2 PM. Please bring your project updates."
>
> Output only the category.

### Expected Output

> **Work**

The email is classified as **Work** because it discusses a team meeting and project updates, which are related to workplace activities.

---

## 2. Few-Shot Prompt – Email Classification

A **few-shot prompt** provides the AI with several examples before asking it to classify a new piece of information.

### Prompt

> Classify each email into one of the following categories: **Work, Personal, or Spam**.
>
> **Example 1**  
> Email: "Dinner at 8 tonight? I'll bring the wine."  
> Category: **Personal**
>
> **Example 2**  
> Email: "You have won a free iPhone! Click here to claim your prize."  
> Category: **Spam**
>
> **Example 3**  
> Email: "The Q2 financial report is due by end of day tomorrow."  
> Category: **Work**
>
> **Now classify this email:**  
> Email: "Are you free for lunch this weekend?"  
> Category:

### Expected Output

> **Personal**

The email is classified as **Personal** because it describes a social invitation rather than a work-related message or unsolicited promotional content.

## Conclusion: Why It Works

### Zero-Shot Prompting

Zero-shot prompting is **simple and flexible** because the model receives only the task instructions and the input. It does not require labeled examples, making it useful when there are few or no examples available. However, the model may have difficulty with ambiguous cases because it has less specific guidance about how categories should be interpreted.

### Few-Shot Prompting

Few-shot prompting provides **examples that demonstrate the expected task and classification pattern**. By seeing examples of Work, Personal, and Spam emails, the model can better understand the intended meaning of each category. This can improve consistency, particularly when working with specialized classification tasks.

## Observations

- **Zero-shot prompting** is quick and flexible but may struggle with ambiguous or unusual inputs.
- **Few-shot prompting** provides additional context and demonstrates the expected output.
- Examples should be **short, relevant, and diverse**.
- The examples should clearly represent the categories being classified.
- Specifying an output format, such as **"Output only the category,"** can make the AI's responses more consistent.
- Adding more examples does not automatically guarantee better results; the examples should be carefully selected to represent the task accurately.
