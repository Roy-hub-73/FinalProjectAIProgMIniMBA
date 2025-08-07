#!/bin/bash

echo "📦 Erstelle virtuelle Umgebung..."
python3 -m venv venv

echo "🚀 Aktiviere virtuelle Umgebung..."
source venv/bin/activate

echo "📚 Installiere Abhängigkeiten..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup abgeschlossen. Du kannst jetzt mit 'source venv/bin/activate' starten."
