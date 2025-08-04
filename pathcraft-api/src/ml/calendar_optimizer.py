from ortools.sat.python import cp_model

class CalendarOptimizer:
    def __init__(self, tasks, slots):
        """
        tasks: A list of tasks, where each task is a dictionary with 'name' and 'duration'.
        slots: A list of available time slots, where each slot is a dictionary with 'name', 'start', and 'end'.
        """
        self.tasks = tasks
        self.slots = slots
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def optimize(self):
        """
        Find the optimal assignment of tasks to slots.
        """
        # Create the variables.
        # task_in_slot[i, j] is 1 if task i is assigned to slot j, and 0 otherwise.
        task_in_slot = {}
        for i, task in enumerate(self.tasks):
            for j, slot in enumerate(self.slots):
                task_in_slot[i, j] = self.model.NewBoolVar(f'task_{i}_in_slot_{j}')

        # Each task must be assigned to exactly one slot.
        for i, task in enumerate(self.tasks):
            self.model.Add(sum(task_in_slot[i, j] for j, slot in enumerate(self.slots)) == 1)

        # The total duration of tasks in a slot must not exceed the slot's duration.
        for j, slot in enumerate(self.slots):
            slot_duration = (slot['end'] - slot['start']).total_seconds() / 60 # Duration in minutes
            self.model.Add(sum(task_in_slot[i, j] * self.tasks[i]['duration'] for i, task in enumerate(self.tasks)) <= int(slot_duration))

        # Solve the model.
        status = self.solver.Solve(self.model)

        # Print the solution.
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution = {}
            for j, slot in enumerate(self.slots):
                solution[slot['name']] = []
                for i, task in enumerate(self.tasks):
                    if self.solver.Value(task_in_slot[i, j]) == 1:
                        solution[slot['name']].append(task['name'])
            return solution
        else:
            return None

if __name__ == '__main__':
    # Example usage
    tasks = [{'name': 'Task 1', 'duration': 2}, {'name': 'Task 2', 'duration': 1}]
    slots = [{'name': 'Slot A', 'start': 9, 'end': 12}, {'name': 'Slot B', 'start': 13, 'end': 15}]

    optimizer = CalendarOptimizer(tasks, slots)
    solution = optimizer.optimize()

    if solution:
        print("Optimal solution found:")
        for slot_name, assigned_tasks in solution.items():
            print(f"  {slot_name}: {assigned_tasks}")
    else:
        print("No solution found.")
