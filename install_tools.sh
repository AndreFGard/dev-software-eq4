pipurl="https://bootstrap.pypa.io/get-pip.py"
wget $pipurl
python3 get-pip.py
echo 'PATH="$PATH:$HOME/.local/bin"' >> $HOME/.bashrc
export PATH="$PATH:$HOME/.local/bin"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 23
cd frontend
npm install 
cd ..
