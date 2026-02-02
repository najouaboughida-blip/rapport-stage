@echo off
echo Installation du Générateur de Rapports Académiques...
echo.

cd /d "%~dp0"

echo 1. Mise à jour de pip...
python -m pip install --upgrade pip

echo 2. Installation de setuptools et wheel...
pip install setuptools==65.5.0 wheel==0.38.4

echo 3. Installation de Flask et dépendances...
pip install flask==2.3.3 flask-cors==4.0.0 Jinja2==3.1.2 Werkzeug==2.3.7

echo 4. Installation des autres dépendances...
pip install python-dotenv==1.0.0 openai==1.3.0 reportlab==4.0.4 python-docx==1.1.0 uuid==1.30

echo 5. Vérification de l'installation...
pip list

echo.
echo ✅ Installation terminée !
echo.
echo Pour démarrer l'application :
echo python app.py
echo.
pausepip list