# Responsible disclosure for audit findings

Omaudit findings are heuristic and can be false positives. Do not publicly name
or accuse a plugin or maintainer based only on an automated grade.

Before publishing a plugin-specific claim:

1. Reproduce it against an immutable commit.
2. Read the cited source and confirm the capability is reachable runtime code.
3. Separate capability from intent; do not describe a capability as malicious
   without independent evidence.
4. Contact the maintainer privately with the commit, rule, evidence, and a
   reasonable opportunity to respond.
5. Use GitHub's private vulnerability reporting when the repository provides it.

Aggregate census statistics may be published without naming individual
projects, provided the methodology and Omaudit version are included.
