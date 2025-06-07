# Nome dell'ambiente virtuale
VENV_DIR=".venv"

# Check if it already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creazione dell'ambiente virtuale in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Ambiente virtuale già presente in $VENV_DIR"
fi

# Activate your venv
source "$VENV_DIR/bin/activate"

# Aggiorna pip all'ultima versione
echo "⬆️ Aggiornamento di pip..."
pip install --upgrade pip

# Installing packages
if [ -f "requirements.txt" ]; then
    echo "📦 Installazione dei pacchetti da requirements.txt"
    pip install -r requirements.txt
else
    echo "⚠️

            File requirements.txt non trovato. Nessun pacchetto installato."
fi

echo "✅ Ambiente virtuale configurato con successo."