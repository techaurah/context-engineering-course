"""Assembly helpers shared by the lessons: segments, rendering,
and the budget ledger."""

from .tokenizer import approx_tokens


def segment(seg_id, text, facts=None, kind="data"):
    return {"id": seg_id, "text": text, "facts": facts or [],
            "kind": kind}


def render(segments):
    return "\n\n".join(s["text"] for s in segments)


def total_tokens(segments):
    return sum(approx_tokens(s["text"]) for s in segments)


class BudgetLedger:
    """Track token spending per component against a window budget."""

    def __init__(self, window):
        self.window = window
        self.spent = {}

    def charge(self, component, tokens):
        self.spent[component] = self.spent.get(component, 0) + tokens

    def charge_text(self, component, text):
        self.charge(component, approx_tokens(text))

    @property
    def used(self):
        return sum(self.spent.values())

    @property
    def remaining(self):
        return self.window - self.used

    def over_budget(self):
        return self.used > self.window

    def report(self):
        rows = {k: v for k, v in sorted(self.spent.items())}
        rows["TOTAL"] = self.used
        rows["REMAINING"] = self.remaining
        return rows
