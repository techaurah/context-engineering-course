# Solution: Context rot: the cost of length itself

With the target first, recall at 2,212 tokens is far higher (its facts sit near position 0, where the position weight is near 1.0, so only the rot penalty applies). In the middle, position weight and rot multiply against the facts. The two runs separate the effects: rot alone costs a little at this size; position alone costs some; together they cost almost everything. Lesson 05 now isolates position the same way.
