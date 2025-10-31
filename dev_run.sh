# !/bin/bash
set -e
echo ""
echo "---------------------------------------------"
echo "👨🏻‍💻 Launch app in developer mode (auto reload)"
echo "---------------------------------------------"
echo ""

# Run the app in developer mode
python -m uvicorn languageninja.api.main:app --reload
