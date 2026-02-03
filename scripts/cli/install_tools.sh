#!/bin/sh

# List of tools to install
TOOLS="uv helm kubectl"

# Function to detect the operating system
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        MINGW*)     echo "windows";;
        *)          echo "unknown";;
    esac
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Homebrew if not present
install_homebrew() {
    if ! command_exists brew; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
}

# Function to install a tool
install_tool() {
    tool=$1
    if ! command_exists "$tool"; then
        echo "Installing $tool..."
        case "$tool" in
            "uv")
                brew install uv
                ;;
            "helm")
                brew install helm
                ;;
            "kubectl")
                brew install kubectl
                ;;
        esac
    else
        echo "$tool already installed"
    fi
}

# Function to print installation instructions
print_instructions() {
    tool=$1
    echo "To install $tool, please follow these steps:"
    case "$tool" in
        "uv")
            echo "  - Visit https://github.com/astral-sh/uv for installation instructions"
            ;;
        "helm")
            echo "  - Visit https://helm.sh/docs/intro/install/ for installation instructions"
            ;;
        "kubectl")
            echo "  - Visit https://kubernetes.io/docs/tasks/tools/install-kubectl/ for installation instructions"
            ;;
    esac
    echo ""
}

# Get OS
OS=$(detect_os)

echo "Platform detected: $OS"

if [ "$OS" = "macos" ]; then
    # Install Homebrew if not present
    install_homebrew
    export HOMEBREW_NO_AUTO_UPDATE=1

    # Install all tools
    echo "Installing all available tools..."
    for tool in $TOOLS; do
        install_tool "$tool"
    done
else
    echo "This script currently only supports automatic installation on macOS."
    echo "For other platforms, please follow these installation instructions:"
    echo ""

    # Show instructions for all tools
    for tool in $TOOLS; do
        print_instructions "$tool"
    done

    echo "Error: This script requires macOS to continue automatically."
    exit 1
fi
