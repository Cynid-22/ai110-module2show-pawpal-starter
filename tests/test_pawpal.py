import sys
import os
import unittest
import datetime
from datetime import timedelta

# Add parent directory to path to import pawpal_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pawpal_system

class TestPawpal(unittest.TestCase):
    def setUp(self) -> None:
        self.Owner = pawpal_system.Owner("Test", 120)
        self.Pet = pawpal_system.Pet("Rex", "Dog", 3)
        self.Owner.AddPet(self.Pet)
        self.Scheduler = pawpal_system.Scheduler(self.Owner)

    def test_task_completion(self) -> None:
        task = pawpal_system.Task("Walk", 30, 1, "Once", self.Pet)
        
        if hasattr(task, 'mark_complete'):
            task.mark_complete()
        else:
            task.MarkAsComplete()
            
        self.assertTrue(task.IsCompleted)

    def test_task_addition(self) -> None:
        task = pawpal_system.Task("Feed", 10, 2, "Once", self.Pet)
        initial_count = len(self.Pet.Tasks)
        self.Pet.AddTask(task)
        self.assertEqual(len(self.Pet.Tasks), initial_count + 1)

    def test_sorting_correctness(self) -> None:
        task_a = pawpal_system.Task("Late", 10, 1, "Once", self.Pet, "18:00")
        task_b = pawpal_system.Task("Early", 10, 1, "Once", self.Pet, "08:00")
        task_c = pawpal_system.Task("Mid", 10, 1, "Once", self.Pet, "12:00")
        
        self.Pet.AddTask(task_a)
        self.Pet.AddTask(task_b)
        self.Pet.AddTask(task_c)
        
        sorted_tasks = self.Scheduler.SortByTime(self.Owner.GetAllTasks())
        
        self.assertEqual(sorted_tasks[0].Description, "Early")
        self.assertEqual(sorted_tasks[1].Description, "Mid")
        self.assertEqual(sorted_tasks[2].Description, "Late")

    def test_recurrence_logic(self) -> None:
        base_date = datetime.date(2025, 1, 1)
        task = pawpal_system.Task("Daily Walk", 30, 2, "Daily", self.Pet, "09:00", base_date)
        self.Pet.AddTask(task)
        
        task.mark_complete()
        
        self.assertTrue(task.IsCompleted)
        self.assertEqual(len(self.Pet.Tasks), 2)
        new_task = self.Pet.Tasks[-1]
        
        self.assertEqual(new_task.Description, "Daily Walk")
        self.assertFalse(new_task.IsCompleted)
        self.assertEqual(new_task.DueDate, base_date + timedelta(days=1))

    def test_conflict_detection(self) -> None:
        task_1 = pawpal_system.Task("Meal 1", 10, 1, "Once", self.Pet, "07:00")
        task_2 = pawpal_system.Task("Meal 2", 10, 1, "Once", self.Pet, "07:00")
        
        self.Pet.AddTask(task_1)
        self.Pet.AddTask(task_2)
        
        warnings = self.Scheduler.DetectConflicts()
        
        self.assertTrue(len(warnings) >= 1)
        self.assertIn("WARNING: Lightweight Conflict", warnings[0])

if __name__ == "__main__":
    unittest.main()
