# Learning Profiles



This directory stores local learning profiles for Aksara Nusantara users.



A learning profile represents a learner's progress within the application. It is **not** intended for user authentication or online accounts.



Each profile may contain information such as:



- Display name

- Learning progress

- Completed lessons

- Quiz history

- Achievement records

- Personal learning statistics

- User preferences (optional)



## Purpose



The profile system allows each learner to maintain an independent learning journey.



Examples include:



- Continuing lessons from previous sessions

- Tracking quiz scores over time

- Measuring learning progress

- Unlocking future achievements and milestones



## Directory Structure



A typical profile directory may look like:



```text

profiles/

│

├── README.md

│

├── alice/

│   ├── profile.json

│   ├── progress.json

│   ├── quiz_history.json

│   └── achievements.json

│

└── guest/

    ├── profile.json

    └── progress.json

```



## Notes



- Profiles are stored locally on the user's computer.

- Multiple profiles are supported.

- Each profile is independent.

- Deleting a profile permanently removes its learning history.

- Future versions may support optional cloud synchronization.



## Future Extensions



The profile system is designed to support future features, including:



- Learning statistics

- Achievement badges

- Daily learning streaks

- Personalized recommendations

- Cloud synchronization

- Cross-device progress synchronization



These features are outside the scope of Core Engine v1.0.

