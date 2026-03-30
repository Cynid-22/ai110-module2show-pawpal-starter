import pawpal_system
from typing import List

def Main() -> None:
    # Constants
    OWNER_AVAILABLE_TIME: int = 90
    
    WALK_DURATION: int = 45
    FEEDING_DURATION: int = 15
    GROOMING_DURATION: int = 40
    
    PRIORITY_HIGH: int = 3
    PRIORITY_MEDIUM: int = 2
    PRIORITY_LOW: int = 1
    
    DOG_AGE: int = 5
    CAT_AGE: int = 3

    # Initialize Core System
    SystemOwner: pawpal_system.Owner = pawpal_system.Owner("Alice", OWNER_AVAILABLE_TIME)

    # Create Pets
    PetDog: pawpal_system.Pet = pawpal_system.Pet(
        Name="Buddy", 
        Species="Dog", 
        Age=DOG_AGE, 
        SpecialRequirements="Requires slow feeder"
    )

    PetCat: pawpal_system.Pet = pawpal_system.Pet(
        Name="Whiskers", 
        Species="Cat", 
        Age=CAT_AGE, 
        SpecialRequirements=None
    )

    # Add Pets to Owner
    SystemOwner.AddPet(PetDog)
    SystemOwner.AddPet(PetCat)

    # Create Tasks
    MorningWalk: pawpal_system.Task = pawpal_system.Task(
        Description="Morning Walk",
        Duration=WALK_DURATION,
        PriorityLevel=PRIORITY_HIGH,
        Frequency="Daily",
        TargetPet=PetDog
    )

    DogFeeding: pawpal_system.Task = pawpal_system.Task(
        Description="Breakfast",
        Duration=FEEDING_DURATION,
        PriorityLevel=PRIORITY_HIGH,
        Frequency="Daily",
        TargetPet=PetDog
    )

    CatGrooming: pawpal_system.Task = pawpal_system.Task(
        Description="Brushing",
        Duration=GROOMING_DURATION,
        PriorityLevel=PRIORITY_LOW,
        Frequency="Weekly",
        TargetPet=PetCat
    )

    CatFeeding: pawpal_system.Task = pawpal_system.Task(
        Description="Breakfast",
        Duration=FEEDING_DURATION,
        PriorityLevel=PRIORITY_MEDIUM,
        Frequency="Daily",
        TargetPet=PetCat
    )

    # Add Tasks to Pets
    PetDog.AddTask(MorningWalk)
    PetDog.AddTask(DogFeeding)
    PetCat.AddTask(CatGrooming)
    PetCat.AddTask(CatFeeding)

    # Initialize Scheduler
    DailyScheduler: pawpal_system.Scheduler = pawpal_system.Scheduler(SystemOwner)

    # Generate Schedule
    GeneratedPlan: List[pawpal_system.Task] = DailyScheduler.GenerateSchedule()

    # Output to Terminal
    print("--- Today's Schedule ---")
    print(f"Owner: {SystemOwner.Name} | Available Time: {SystemOwner.AvailableTime} minutes")
    print()

    TotalTimeUsed: int = 0
    for ScheduledTask in GeneratedPlan:
        print(f"[Priority {ScheduledTask.PriorityLevel}] {ScheduledTask.TargetPet.Name} - {ScheduledTask.Description} ({ScheduledTask.Duration} mins)")
        TotalTimeUsed += ScheduledTask.Duration

    print()
    print(f"Total Time Scheduled: {TotalTimeUsed} minutes")
    print(f"Time Remaining: {SystemOwner.AvailableTime - TotalTimeUsed} minutes")

if __name__ == "__main__":
    Main()
