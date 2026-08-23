# Omaudit v0.1.0

Omaudit is a static capability audit for Omarchy 4 shell plugins. It helps
people understand what plugin source can reach before installation and records
an accepted baseline for detecting later capability drift.

This first release includes local and CI scans, declaration verification,
install-time review, installed-plugin checks, report cards, and an explicitly
invoked ecosystem census. It never executes plugin QML and does not claim to be
a sandbox, malware detector, or proof of safety.
