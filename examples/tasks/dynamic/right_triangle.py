#!/usr/bin/env python3
"""
This task is example of simple right triangle dynamic generated choice tasks.
"""

class TriangleTask(datamodel.DynamicTask):
    def __init__(self):
        super().__init__()
        # generate sides of right trinagle with integer length
        sides = []
        for i in range(1, 301):
            for j in range(i, 301):
                if ((i**2 + j**2)**0.5).is_integer():
                    sides += [(i, j, int((i**2 + j**2)**0.5))]
        self._sides = []
        for (a, b, c) in sides:
            self._sides += [(a, b, c)]
            if a != b:
                self._sides += [(b, a, c)]
        
    def generate(self):
        from random import randrange
        task = datamodel.ChoiceTask()
        (a, b, c) = self._sides[randrange(len(self._sides))]
        question = "Jak dlouhá je odvěsna pravoúhlého trojúhelníka " + \
                   "pokud je druhá odvěsna dlouhá " + str(b) + " cm a " + \
                   "přepona měří " + str(c) + " cm?"
        task.set_question(question)
        start = randrange(-5, 1)
        if a + start < 1:
            start = 0
        answers = []
        for i in range(a + start, a + start + 6):
            answers += [(str(i) + " cm", True if i == a else False)]
        task.set_answers(answers)
        return task
        
task = TriangleTask()

