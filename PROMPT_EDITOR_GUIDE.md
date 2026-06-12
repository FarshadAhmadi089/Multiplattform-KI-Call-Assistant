# Prompt Editor Guide

The built-in Prompt Editor allows you to customize how the AI behaves without manually editing text files.

## Overview

The AI Call Assistant uses two main prompts:

1. **Live Analysis Prompt**: Controls real-time feedback during calls
2. **Final Report Prompt**: Defines the structure of session reports

Both can be customized directly through the GUI.

## Opening the Editor

1. Launch the GUI: `python CallAssistantGUI.py`
2. Click **Edit Prompts** button at the bottom
3. A new window opens with the Prompt Editor

## Editor Interface

```
┌─────────────────────────────────────────────────────────┐
│ Prompt Editor                                      [ X ] │
├─────────────────────────────────────────────────────────┤
│ ┌─ Select Prompt ─────────────────────────────────────┐ │
│ │ Prompt Type: [Live Analysis        ▼] [Load]       │ │
│ │ Controls real-time feedback during the call.        │ │
│ │ Provides insights and questions.                    │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ ┌─ Prompt Content ────────────────────────────────────┐ │
│ │                                                      │ │
│ │  You are an AI assistant providing live feedback... │ │
│ │                                                      │ │
│ │  Your task is to:                                   │ │
│ │  1. Listen to the conversation                      │ │
│ │  2. Provide constructive insights                   │ │
│ │  3. Ask helpful questions                           │ │
│ │                                                      │ │
│ │  [Scrollable text editor]                           │ │
│ │                                                      │ │
│ └─────────────────────────────────────────────────────┘ │
│ 💡 Tip: Use placeholders like {participants_list}...   │
│                                                         │
│ [Save Changes] [Reset to Original]            [Close]  │
│ Loaded: prompts/live_analysis.txt                      │
└─────────────────────────────────────────────────────────┘
```

## Step-by-Step Usage

### 1. Select a Prompt

Click the dropdown and choose:
- **Live Analysis**: For customizing real-time feedback
- **Final Report**: For customizing the report structure

### 2. Load the Prompt

Click the **Load** button to:
- View the current prompt content
- See the description of what it does
- Enable editing capabilities

### 3. Edit the Content

The editor shows the full prompt text with:
- Monospace font (Consolas) for readability
- Scroll support for long prompts
- Full text editing capabilities

**Available Placeholders:**
- `{participants_list}` - Comma-separated participant names
- `{session_number}` - Current session number
- `{session_content}` - Content from session file
- `{participants_table}` - Auto-generated HTML table
- `{speaker_label}` - Your configured speaker label
- `{listener_label}` - Your configured listener label

### 4. Save or Reset

**Save Changes:**
- Click **Save Changes** button
- Confirm the save dialog
- Changes are immediately written to the prompt file

**Reset to Original:**
- Click **Reset to Original** button
- Confirm the reset dialog
- Editor reverts to the last loaded content

### 5. Close the Editor

Click **Close** or the window's X button to close.

## Customization Examples

### Example 1: Making Live Analysis More Technical

**Original:**
```
Provide constructive feedback and helpful questions.
Keep it friendly and encouraging.
```

**Modified for Code Reviews:**
```
Provide technical code review feedback focusing on:
- Best practices and design patterns
- Performance optimizations
- Security considerations
- Code maintainability

Format: Technical Issue | Severity | Suggestion
```

### Example 2: Adding Custom Report Section

**Original Final Report:**
```
## Session Summary

[AI-generated summary here]
```

**Modified with Metrics:**
```
## Session Summary

[AI-generated summary here]

## Metrics

| Metric | Value |
|--------|-------|
| Duration | {session_duration} |
| Participants Active | {active_count} |
| Key Decisions | {decision_count} |
| Action Items | {action_count} |
```

### Example 3: Changing Feedback Tone

**Original (Friendly):**
```
Great discussion! Here are some thoughts...
```

**Modified (Professional):**
```
Analysis of discussion points:
1. [Point]
2. [Point]

Recommended actions:
- [Action]
```

### Example 4: Focus on Specific Domain

**For Teaching/Tutoring:**
```
You are an educational assistant analyzing tutoring sessions.

Focus areas:
1. Student understanding and comprehension
2. Teaching methodology effectiveness
3. Knowledge gaps to address
4. Recommended follow-up topics

Provide feedback that helps improve learning outcomes.
```

**For Sales Meetings:**
```
You are a sales analysis assistant reviewing client calls.

Focus areas:
1. Client needs and pain points
2. Objections raised and handled
3. Next steps and commitments
4. Deal progression indicators

Provide actionable insights for closing deals.
```

## Tips and Best Practices

### General Tips

1. **Backup Before Major Changes**: Copy the original prompt text before making significant modifications
2. **Test Incrementally**: Make small changes and test before big rewrites
3. **Use Placeholders Wisely**: They make prompts dynamic and reusable
4. **Keep It Clear**: AI performs better with clear, specific instructions
5. **Iterate**: Refine prompts based on results

### Live Analysis Prompt Tips

- **Be Specific About Tone**: Specify exactly how formal/casual you want feedback
- **Set Clear Frequency**: Mention how often to provide insights
- **Define Format**: Specify if you want bullet points, paragraphs, etc.
- **Limit Length**: Consider asking for concise feedback to avoid overwhelming output

### Final Report Prompt Tips

- **Structure Matters**: Use markdown headings and tables for clarity
- **Include Examples**: Show the AI what format you expect
- **Use Placeholders**: Make reports consistent across sessions
- **Test Output**: Generate a report and adjust the prompt if needed

### Common Placeholders Reference

```
{participants_list}      → "Alice, Bob, Charlie"
{session_number}         → "1"
{session_content}        → [Content from sessions/session_1.txt]
{participants_table}     → [Auto-generated HTML table]
{speaker_label}          → "Moderator" (or your custom label)
{listener_label}         → "Participants" (or your custom label)
```

## Troubleshooting

### "File Not Found" Error

**Problem**: Prompt file doesn't exist

**Solution**:
- Ensure `prompts/` folder exists
- Check that `live_analysis.txt` and `final_report.txt` are present
- Restore from backup or create new files

### Changes Not Taking Effect

**Problem**: Modifications don't appear in output

**Solution**:
- Ensure you clicked **Save Changes**
- Restart the recording session to reload prompts
- Check that the correct prompt file was edited

### Prompts Too Long

**Problem**: API timeout or truncated responses

**Solution**:
- Shorten the prompt
- Remove unnecessary details
- Focus on the most important instructions

### Poor AI Performance

**Problem**: AI doesn't follow instructions well

**Solution**:
- Make instructions more explicit
- Add examples in the prompt
- Use numbered lists for clarity
- Specify output format explicitly

## Advanced Customization

### Multi-Language Support

Add language instructions to prompts:

```
Provide all feedback in German.
Use formal "Sie" form for professional contexts.
```

### Conditional Logic

While prompts don't support true conditionals, you can give AI contextual guidance:

```
If technical discussion detected:
- Focus on implementation details
- Suggest best practices

If business discussion detected:
- Focus on ROI and outcomes
- Suggest action items
```

### Personality Customization

Give the AI a specific personality:

```
Act as a senior software architect with 15 years of experience.
Be direct but constructive in feedback.
Use industry-standard terminology.
Prioritize scalability and maintainability.
```

## Security Considerations

- **Don't Include Secrets**: Never put API keys or passwords in prompts
- **Review Before Sharing**: Check prompts before sharing projects
- **Backup Regularly**: Keep copies of working prompts
- **Version Control**: Consider tracking prompt changes in git

## Getting Help

- **Full Documentation**: See [README.md](README.md)
- **Examples**: Check `prompts/` folder for default templates
- **Issues**: Report problems on [GitHub Issues](https://github.com/FarshadAhmadi089/Multiplattform-KI-Call-Assistant/issues)

---

**Happy customizing! ✨**
