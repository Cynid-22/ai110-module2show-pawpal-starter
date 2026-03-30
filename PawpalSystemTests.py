import unittest
import pawpal_system

class PawpalSystemTests(unittest.TestCase):
    def test_TaskCompletion(self) -> None:
        # Arrange
        PetInstance: pawpal_system.Pet = pawpal_system.Pet(
            Name="Rex",
            Species="Dog",
            Age=3,
            SpecialRequirements=None
        )
        TaskInstance: pawpal_system.Task = pawpal_system.Task(
            Description="Walk",
            Duration=30,
            PriorityLevel=1,
            Frequency="Daily",
            TargetPet=PetInstance
        )
        
        # Act
        TaskInstance.MarkAsComplete()
        
        # Assert
        self.assertTrue(TaskInstance.IsCompleted)

    def test_TaskAddition(self) -> None:
        # Arrange
        PetInstance: pawpal_system.Pet = pawpal_system.Pet(
            Name="Luna",
            Species="Cat",
            Age=2,
            SpecialRequirements=None
        )
        TaskInstance: pawpal_system.Task = pawpal_system.Task(
            Description="Feed",
            Duration=10,
            PriorityLevel=2,
            Frequency="Twice Daily",
            TargetPet=PetInstance
        )
        
        # Act
        StartingCount: int = len(PetInstance.Tasks)
        PetInstance.AddTask(TaskInstance)
        EndingCount: int = len(PetInstance.Tasks)
        
        # Assert
        self.assertEqual(StartingCount, 0)
        self.assertEqual(EndingCount, 1)

if __name__ == "__main__":
    unittest.main()
