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

- **Tradeoff:** The conflict detection algorithm is lightweight and currently only flags a warning if two tasks have the exact same start time (`HH:MM`).
- **Reasoning:** It intentionally skips mathematically calculating overlapping minutes between variable `Duration` lengths. This is a reasonable tradeoff because PawPal+ acts primarily as a flexible daily checklist assistant for humans, not a rigid server CPU thread scheduler. An owner can logically adapt to minor duration overlaps (e.g., spending 15 minutes grooming the cat while the dog eats its 20-minute breakfast), whereas an exact start-time conflict usually implies an immediate logistical clash requiring a warning.

---

## 3. AI Collaboration

**a. How you used AI**

- VS Code Copilot's *Inline Chat* and *Agent Mode* were the most effective tools for building the logic. Agent Mode easily flushed out the skeleton dependencies between `Owner` and `Pet`, whereas Inline Chat was heavily targeted for precise logic algorithms like building `SortedByTime(AllTasks)`.
- Using separate chat sessions for different architectural phases prevented prompt saturation. Dedicating an entirely clean thread to Testing allowed Copilot to focus entirely on parsing edge cases instead of getting distracted by existing UI markup. 

**b. Judgment and verification**

- An AI suggestion originally proposed mathematically parsing overlapping duration collisions into the `DetectConflicts` scheduler logic (e.g., checking if Task A's 15-minute runtime collided with Task B's start block). I rejected the complex loop in favor of an O(N) exact-time map, keeping my system design functionally lighter and cleaner since pet schedules are inherently flexible check-ins rather than rigid server cycles.
- Functioning as the "lead architect" taught me that AI operates best as an instantaneous junior developer executing your blueprint. By forcing AI components to hook exactly onto *my* explicitly designed UML architectures and evaluating them against *my* own isolated test frameworks, I dictated the overall quality of the build rather than letting the AI decide the logic constraints.

---

## 4. Testing and Verification

**a. What you tested**
- I built a comprehensive unit suite targeting logical data array manipulation across the `Scheduler` bounds.
- I tested **Sorting Correctness**, **Recurrence Generation**, **Conflict Detection**, **Task Addition**, and **Task Completion**.
- These were critical because algorithmic filtering, cloning, and sorting are silent "backend" operations. If these operations fail mathematically, the Streamlit frontend would simply display fundamentally broken lists lacking priority without directly crashing, making it impossible to debug logically later.

**b. Confidence**

- I am 5/5 highly confident in the backend infrastructure as verified natively by the `Pytest` run displaying 100% assertions passed.
- If granted more iterations natively, I would test scaling large data limits (e.g. 5,000 tasks attached to multiple pets dynamically), testing explicit invalid HH:MM string bounds exceptions, and handling negative duration inputs intelligently inside `Scheduler`.

---

## 5. Reflection

**a. What went well**

- Transitioning from placeholder `.py` skeleton dictionaries into fully initialized modular backend instances (`Owner`, `Task`, `Scheduler`) through Python Dataclasses mapped exceptionally cleanly once connected natively inside `st.session_state`.

**b. What you would improve**

- I would expand conflict detection beyond the exact lightweight start-times and into mathematical overlapping span logic scaling against the explicit duration intervals if I allocated more time to refactor.

**c. Key takeaway**

- Building systems alongside AI requires operating actively as the Lead Architect making explicit, structural decisions independently beforehand (`UML`) instead of just asking an AI to solve an ambiguous problem natively from scratch.
