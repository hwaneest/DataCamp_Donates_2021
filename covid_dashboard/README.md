# Get Started
### Linux/Mac
```shell
# Docker(Recommended)
git clone https://github.com/cozytk/covid_dashboard.git
docker build -f Dockefile -t taekkim/covid-dashboard:latest .
docker run -p 8080:8080 taekkim/covid-dashboard:latest
```

```shell
# venv
git clone https://github.com/cozytk/covid_dashboard.git
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py
```

# Service

https://user-images.githubusercontent.com/59143479/145184721-ec3bf47e-6688-49f9-a305-485e59f1d60e.mov
