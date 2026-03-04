#!/bin/bash
# install-skill.sh - 一键安装脚本

echo "Installing PDF Knowledge Extractor Skill..."

# Clone repository
REPO_URL="https://github.com/pyh-pan/knowledgebase-creator.git"
INSTALL_DIR="${HOME}/.local/share/opencode/skills/pdf-knowledge-extractor"

git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Install dependencies
pip install -r requirements.txt

echo "Installation complete!"
echo "Location: $INSTALL_DIR"
echo ""
echo "Quick start:"
echo "  cd $INSTALL_DIR"
echo "  python scripts/extract.py --help"
