# Real-Time Fraud Call Detection and Prevention System
## Overview
This project addresses the growing issue of banking fraud by providing a proactive solution to detect and prevent scams in real-time. 
Fraudulent calls are a significant threat, tricking users into authorizing unauthorized transactions. Our system leverages Open Finance data, Natural Language Processing (NLP),
and speech-to-text technology to identify fraudulent calls as they happen, alert users, and coordinate with financial institutions to temporarily hold transactions.

## How It Works
When a call is received, the system captures the audio and converts it into a text transcript using speech-to-text processing. 
The transcript is then analyzed by a scam detection system built with NLP techniques, trained to recognize fraud-related keywords, patterns, and phrases. 
If the call is classified as a scam:

- User Alert: The user is immediately notified via phone vibration or on-screen warning.
- Transaction Hold: The bank is informed to temporarily hold any transactions for 30 minutes, preventing potential losses.
## Technical Workflow
- Audio Processing: Capture the incoming call audio and convert it into text.
- Fraud Detection: Analyze the text transcript using an NLP model to classify the call as either "Scam" or "Not Scam."
- Preventive Action:
  - Notify the user in real-time about the suspicious call.
  - Collaborate with the user’s bank to put transactions on hold temporarily.
