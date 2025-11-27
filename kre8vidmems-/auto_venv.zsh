# Add to ~/.zshrc for automatic venv activation when entering the project

# Kre8VidMems auto-activation
kre8vidmems_auto_venv() {
    local project_dir="/Users/kckc/Downloads/memvideo"
    local venv_dir="$project_dir/.venv"
    
    # Check if we're in the project directory
    if [[ "$PWD" == "$project_dir"* ]]; then
        # Check if venv exists and is not already activated
        if [[ -d "$venv_dir" ]] && [[ "$VIRTUAL_ENV" != "$venv_dir" ]]; then
            source "$venv_dir/bin/activate"
            echo "✓ Kre8VidMems virtual environment activated"
        fi
    else
        # Deactivate if we leave the project directory
        if [[ "$VIRTUAL_ENV" == "$venv_dir" ]]; then
            deactivate
        fi
    fi
}

# Add hook to run on directory change
autoload -U add-zsh-hook
add-zsh-hook chpwd kre8vidmems_auto_venv

# Also run on shell startup if we're already in the directory
kre8vidmems_auto_venv
