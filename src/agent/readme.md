# 1. Navigate to the folder where you created the .venv (looks like your root folder)
cd C:\Users\Win11-User\Desktop\edrpublicsource-main\edrpublicsource-main

# 2. Activate the virtual environment
.\.venv\Scripts\Activate

# 3. Install your required packages (assuming you have a requirements.txt here)
pip install fastapi uvicorn requests

# 4. Navigate back to your app directory
cd src\backend\app

# 5. Run the server! Since you added the uvicorn.run block in the code, you can just do:
python main.py
