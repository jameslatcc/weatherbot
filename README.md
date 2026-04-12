### Weatherbot
Query rainfall data by weather API, sent Line messages if status is changed.

```mermaid
graph TD
    A[User enter station name] --> B{Is station name valid?}

    B -- Yes --> C[Fetch data from API]
    B -- No --> A

    C --> D{Fetch successful?}

    D -- Yes --> E[Reset error counter]
    E --> F[Parse API response]

    D -- No --> G[Retry and log error]
    G --> H{Retry with exponential backoff}

    H -- Yes --> F
    H -- No --> I[Log critical error]
    I --> J[Increment failure count]

    J --> K{Reached max retries?}
    K -- Yes --> L[Send LINE system alert]
    K -- No --> H

    L --> Q{LINE send successful?}

    F --> M[Load previous state]
    M --> N[Compute new state]

    N --> O{State changed?}

    O -- Yes --> P[Send LINE rain alert]
    O -- No --> Z[End]

    P --> Q

    Q -- Yes --> R[Persist new state]
    Q -- No --> S[Log critical error]

    R --> Z
    S --> Z
```

This program parses weather API data and use Line message to notify user the weather state is changed significantly.


User enter station name:
    - Ask user to input valid station name if station name isn't exist or invalid.
Fetch data from API:
    - If station name is valid, fetch weather data though API.

There are two conditions while querying API.
If fail, we have to retry, implement "exponential backoff algorithm" and jitter to retry.
    - fail count increase, once reach to maximum value, stop retry.
        - once reach maximum fail count, send out line message to notify user "api service is unavailable now"
    - every retry should keep results as log.
    - once success, reset fail count to 0.
If success, proceed and reset fail count to 0.

Start parsing weather API data, and compare it with previous state.
    - if it is the first request, no comparison.
    - if state changed, send line message to notify user "the weather is changed"
    - according to the level of change, defind "light" or "heavy" rain.
    - if line message fail to send out message, log critical error, send out email "Line message failed"

End of the process