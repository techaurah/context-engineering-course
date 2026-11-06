# Solution: Few-shot examples: buying accuracy with tokens

Complaint accuracy collapses: the one complaint test message ('Nobody answered the phone all morning, furious') is now labelled booking, the nearest remaining example by word overlap, and total accuracy caps at 0.875 (7 of 8) at every example count from 6 to 10. Count cannot substitute for coverage. The fix is one good example per region of the label space, then stop at the bend.
