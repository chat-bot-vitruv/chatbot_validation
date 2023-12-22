### 가상환경설치

python 3.3 이상 필요
```
python -m venv ./env
```

Viture Envrionment 접속
https://docs.python.org/3/library/venv.html
```
// macOs
source env/bin/activate

// windows
.\env\Scripts\activate.bat

// powerShell
.\env\Scripts\Activate.ps1
```


가상 환경 접속 후 package 설치
```
// python 3.12 error 발생 -> 3.11.6 
pip install -r requirements.txt
```

가상 환경 종료
```
deactivate
```

가상환경에서 streamlit 실행
```
streamlit run Home.py
```
