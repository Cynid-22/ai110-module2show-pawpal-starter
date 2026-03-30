# PawPal+ Project Reflection

## 1. System Design

**Core Actions:**
1. Enter basic owner and pet information (e.g., add a pet).
2. Add, edit, and track pet care tasks (e.g., schedule a walk with duration and priority).
3. Generate and view a daily schedule/plan that fits within constraints and priorities.

**a. Initial design**

- The initial UML design centered heavily around separating the logic into four simple, modular domains: `Pet`, `Owner`, `Task`, and `Scheduler`.
- Classes included:
  - `Pet`: Responsibilities include persisting information about the individual pet's characteristics (Name, Species, Age, Special Requirements).
  - `Owner`: Centralizes the user's available time constraints and acts as the container for their array of pets.
  - `Task`: A Python Dataclass that holds the duration and status information for a specific, discrete pet care need (e.g. morning walk, feeding).
  - `Scheduler`: Acts as the app's logical brain. It intakes raw tasks and available times, filtering and structuring out a definitive subset plan that respects user time constraints.

**b. Design changes**

- Yes, design changes occurred dynamically during skeleton implementation based on AI analysis.
- Change 1: Added a `TargetPet` relation inside the `Task` dataclass. Why? A task cannot float in a vacuum; if an owner has multiple pets, a task needs to be hard-linked to the specific pet receiving the care.
- Change 2: Transitioned `PriorityLevel` from an ambiguous `str` (e.g., "High", "Low") to an explicit `int`. Why? Comparing, sorting, and maximizing `int` values via algorithms natively allows the `Scheduler` to mathematically pack high-priority tasks in limited time gaps faster and safer.
- Change 3: Bound `Scheduler` to an `Owner` object at initialization. Why? Passing `Owner` dynamically avoids unassociated `AvailableTime` states and grounds the schedule around one specific owner's domain boundaries.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
