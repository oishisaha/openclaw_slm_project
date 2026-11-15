

#!/bin/bash



python3 /home/vboxuser/.openclaw/train_housing_complete.py 2>&1 | tee model_results.txt

cat << 'ENDREPORT' >> model_results.txt

# Model Training Summary (Results to be generated)
ENDREPORT
