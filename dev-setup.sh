#!/bin/bash

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing core dev tools: Python, pip, GCC, Ruby, Node.js, npm..."
sudo apt install -y \
    python3 \
    python3-pip \
    build-essential \
    ruby-full \
    nodejs \
    npm \
    curl \
    git

echo "🌈 Installing NVM (Node Version Manager)..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Load NVM into the current session
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

echo "⬇️ Installing latest Node.js via NVM..."
nvm install node

echo "🐍 Installing common Python packages with pip..."
python3 -m pip install --upgrade pip
python3 -m pip install \
    virtualenv \
    ipython \
    black \
    flake8 \
    requests \
    httpie \
    rich \
    jupyter \
    pandas \
    matplotlib \
    numpy

echo "🟢 Installing global npm packages..."
npm install -g \
    yarn \
    typescript \
    eslint \
    prettier \
    nodemon \
    serve \
    http-server \
    npm-check \
    degit

echo "💎 Installing common Ruby gems..."
gem install \
    bundler \
    rake \
    rubocop \
    pry \
    irbtools \
    jekyll

# Optional CLI goodness
read -p "⚡ Want to install bonus CLI tools (fzf, bat, ripgrep, etc)? [y/n] " install_cli

if [[ "$install_cli" =~ ^[Yy]$ ]]; then
    echo "✨ Installing CLI tools..."
    sudo apt install -y fzf ripgrep bat fd-find zoxide

    # bat is installed as batcat on Ubuntu
    if ! command -v bat &> /dev/null; then
        echo "🛠 Linking batcat to bat..."
        sudo ln -s /usr/bin/batcat /usr/local/bin/bat
    fi
fi

echo "✅ Setup complete! Restart your terminal to apply changes."

