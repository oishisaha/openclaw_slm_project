

#!/bin/bash



python3 /home/vboxuser/.openclaw/train_housing.py >> model_results.txt 2>&1

cat << 'REPORT_END' > /home/vboxuser/.openclaw/model_results_summary.md
# Housing Price Prediction Model Results


## Summary Report (to be generated)

The model will generate predictions and feature importance analysis here.

REPORT_END


