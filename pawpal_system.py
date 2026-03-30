from dataclasses import dataclass, field
from typing import List, Optional
import datetime
from datetime import timedelta

@dataclass
class Pet:
    Name: str
    Species: str
    Age: int
    SpecialRequirements: Optional[str] = None
    Tasks: List['Task'] = field(default_factory=list)

    def GetDetails(self) -> str:
        Reqs: str = self.SpecialRequirements if self.SpecialRequirements else "None"
        return f"{self.Name} the {self.Species} (Age: {self.Age}, Special Needs: {Reqs})"

    def UpdateDetails(self, Name: str, Species: str, Age: int, SpecialRequirements: str) -> None:
        self.Name = Name
        self.Species = Species
        self.Age = Age
        self.SpecialRequirements = SpecialRequirements

    def AddTask(self, NewTask: 'Task') -> None:
        self.Tasks.append(NewTask)

@dataclass
class Task:
    Description: str
    Duration: int
    PriorityLevel: int
    Frequency: str
    TargetPet: Pet
    Time: str = "00:00"
    DueDate: Optional[datetime.date] = None
    IsCompleted: bool = False

    def mark_complete(self) -> None:
        """Alias for mark complete mapped to test scripts."""
        self.MarkAsComplete()

    def MarkAsComplete(self) -> None:
        self.IsCompleted = True
        self._GenerateRecurring()

    def _GenerateRecurring(self) -> None:
        BaseDate: datetime.date = self.DueDate if self.DueDate else datetime.date.today()
        if self.Frequency.lower() == "daily":
            NextDate = BaseDate + timedelta(days=1)
            NextTask = Task(self.Description, self.Duration, self.PriorityLevel, self.Frequency, self.TargetPet, self.Time, NextDate)
            self.TargetPet.AddTask(NextTask)
        elif self.Frequency.lower() == "weekly":
            NextDate = BaseDate + timedelta(days=7)
            NextTask = Task(self.Description, self.Duration, self.PriorityLevel, self.Frequency, self.TargetPet, self.Time, NextDate)
            self.TargetPet.AddTask(NextTask)

    def UpdateDuration(self, NewDuration: int) -> None:
        self.Duration = NewDuration

    def UpdatePriority(self, NewPriority: int) -> None:
        self.PriorityLevel = NewPriority

class Owner:
    def __init__(self, Name: str, AvailableTime: int) -> None:
        self.Name: str = Name
        self.AvailableTime: int = AvailableTime
        self.Pets: List[Pet] = []

    def GetAvailableTime(self) -> int:
        return self.AvailableTime

    def UpdateAvailableTime(self, NewTime: int) -> None:
        self.AvailableTime = NewTime

    def AddPet(self, NewPet: Pet) -> None:
        self.Pets.append(NewPet)

    def GetAllTasks(self) -> List[Task]:
        AllTasks: List[Task] = []
        for PetItem in self.Pets:
            AllTasks.extend(PetItem.Tasks)
        return AllTasks

class Scheduler:
    def __init__(self, SystemOwner: Owner) -> None:
        self.SystemOwner: Owner = SystemOwner
        self.SelectedPlan: List[Task] = []

    def GenerateSchedule(self, AvailableTime: Optional[int] = None) -> List[Task]:
        Limit: int = AvailableTime if AvailableTime is not None else self.SystemOwner.AvailableTime
        AllTasks: List[Task] = self.SystemOwner.GetAllTasks()
        
        PendingTasks: List[Task] = [T for T in AllTasks if not T.IsCompleted]
        SortedTasks: List[Task] = sorted(PendingTasks, key=lambda T: T.PriorityLevel, reverse=True)
        
        self.SelectedPlan = []
        RemainingTime: int = Limit
        
        for TaskItem in SortedTasks:
            if TaskItem.Duration <= RemainingTime:
                self.SelectedPlan.append(TaskItem)
                RemainingTime -= TaskItem.Duration
                
        return self.SelectedPlan

    def SortByTime(self, TasksList: List[Task]) -> List[Task]:
        # Sort using zfill on strings to ensure standard time ascending formatting (e.g. 09:00 vs 14:00)
        return sorted(TasksList, key=lambda T: T.Time.zfill(5))

    def FilterTasks(self, IsCompleted: Optional[bool] = None, PetName: Optional[str] = None) -> List[Task]:
        Filtered: List[Task] = []
        for T in self.SystemOwner.GetAllTasks():
            if IsCompleted is not None and T.IsCompleted != IsCompleted:
                continue
            if PetName is not None and T.TargetPet.Name != PetName:
                continue
            Filtered.append(T)
        return Filtered

    def DetectConflicts(self) -> List[str]:
        Warnings: List[str] = []
        TimeMap = {}
        for T in self.SystemOwner.GetAllTasks():
            if not T.IsCompleted:
                if T.Time in TimeMap:
                    Warnings.append(f"WARNING: Lightweight Conflict - Both '{T.Description}' and '{TimeMap[T.Time].Description}' occur strictly at {T.Time}.")
                else:
                    TimeMap[T.Time] = T
        return Warnings
