# Solution: Memory formats: the reader is part of the format

Prose breaks too: its extractor captures the first word after 'is', so the stored status reads back as just 'paid'. Quoted CSV and JSON survive by design, because both delimit values structurally. The naive and unquoted paths break again. The single rule is: never store state in a format whose delimiter can appear unescaped in a value. Every failure in this lesson is that rule, broken at write time and discovered at read time, which is the most expensive time to discover anything.
