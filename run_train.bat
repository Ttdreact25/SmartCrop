@echo off
cd /d "c:\Users\Admin\Documents\new dev kiran\Smart-Crop-Recommendation-System-main (2)\Smart-Crop-Recommendation-System-main (1)\Smart-Crop-Recommendation-System-main"
call venv\Scripts\pip.exe install pandas scikit-learn numpy
call venv\Scripts\python.exe train_fertilizer_model.py
pause

