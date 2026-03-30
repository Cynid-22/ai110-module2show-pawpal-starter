import pawpal_system
from typing import List
import datetime

def Main() -> None:
    # Constants
    OWNER_AVAILABLE_TIME: int = 120
    PRIORITY_HIGH: int = 3
    PRIORITY_MEDIUM: int = 2
    PRIORITY_LOW: int = 1
    DOG_AGE: int = 5

    # Initialize Core System
    SystemOwner: pawpal_system.Owner = pawpal_system.Owner("Alice", OWNER_AVAILABLE_TIME)
    
    # Create Pet
    PetDog: pawpal_system.Pet = pawpal_system.Pet(
        Name="Buddy", 
        Species="Dog", 
        Age=DOG_AGE, 
        SpecialRequirements="Requires slow feeder"
    )
    SystemOwner.AddPet(PetDog)

    # Create Tasks Unordered with Conflicts
    Task1: pawpal_system.Task = pawpal_system.Task(
        Description="Evening Walk", Duration=30, PriorityLevel=PRIORITY_MEDIUM, Frequency="Daily", TargetPet=PetDog, Time="18:00", DueDate=datetime.date.today()
    )
    Task2: pawpal_system.Task = pawpal_system.Task(
        Description="Breakfast", Duration=15, PriorityLevel=PRIORITY_HIGH, Frequency="Daily", TargetPet=PetDog, Time="08:00", DueDate=datetime.date.today()
    )
    Task3: pawpal_system.Task = pawpal_system.Task(
        Description="Grooming", Duration=40, PriorityLevel=PRIORITY_LOW, Frequency="Once", TargetPet=PetDog, Time="14:00"
    )
    # Task 4 conflicts explicitly with Task 2
    Task4: pawpal_system.Task = pawpal_system.Task(
        Description="Vet Visit", Duration=60, PriorityLevel=PRIORITY_HIGH, Frequency="Once", TargetPet=PetDog, Time="08:00"
    )

    # Add Tasks
    PetDog.AddTask(Task1)
    PetDog.AddTask(Task2)
    PetDog.AddTask(Task3)
    PetDog.AddTask(Task4)

    # Init Engine
    DailyScheduler: pawpal_system.Scheduler = pawpal_system.Scheduler(SystemOwner)

    print("--- Conflict Detection ---")
    Conflicts: List[str] = DailyScheduler.DetectConflicts()
    if Conflicts:
        for Warning in Conflicts:
            print(Warning)
    else:
        print("No conflicts detected.")

    print("\n--- Sorted By Time ---")
    AllTasks: List[pawpal_system.Task] = SystemOwner.GetAllTasks()
    SortedPlan: List[pawpal_system.Task] = DailyScheduler.SortByTime(AllTasks)
    for T in SortedPlan:
        print(f"[{T.Time}] {T.Description}")

    print("\n--- Filtering: Completed/Recurring Trigger ---")
    print(f"Total system tasks BEFORE completion trick: len({len(SystemOwner.GetAllTasks())})")
    Task2.MarkAsComplete() # This will complete Task 2 and auto-generate tomorrow's breakfast!
    CompletedTasks: List[pawpal_system.Task] = DailyScheduler.FilterTasks(IsCompleted=True)
    for CountT in CompletedTasks:
        print(f"[{CountT.Time}] {CountT.Description} (Completed)")
    print(f"Total system tasks AFTER completion trick: len({len(SystemOwner.GetAllTasks())})")

    print("\n--- Filtering: Pending Tasks Remaining ---")
    PendingTasks: List[pawpal_system.Task] = DailyScheduler.FilterTasks(IsCompleted=False)
    for CT in PendingTasks:
        DateStr = CT.DueDate.strftime("%Y-%m-%d") if CT.DueDate else "None"
        print(f"[{CT.Time}] {CT.Description} (Due: {DateStr})")

if __name__ == "__main__":
    Main()
