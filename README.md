# **Persistence_Diff**

Checking the persistence locations on an infected system is a common task for defenders. Microsoft Defender provides a persistence location report in JSON format through [live response](https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/live-response?view=o365-worldwide).

The file can be overwhelming to analyze. Comparing the persistence location report with that of a clean system can significantly reduce the number of items to analyze.

To use the script, you need to download the persistence locations from a confirmed clean system and compare it with the persistence locations on the infected system.

## **Dependencies Installation**

```bash
pip3 install deepdiff
```

## **Usage**

```bash
python3 persistence_diff.py --infected infected.json --clean clean.json
```

This command compares the persistence locations in the **`infected.json`** file with those in the **`clean.json`** file.
