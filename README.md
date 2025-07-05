# Gran Turismo 7 digital display

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<div align="center">

[![GT7 SIMDASH IN ACTION](https://img.youtube.com/vi/Pckp1NWW3_M/0.jpg)](https://www.youtube.com/watch?v=Pckp1NWW3_M)

<h3>

 [Video 1](https://www.youtube.com/watch?v=Pckp1NWW3_M) | [Documentation](https://github.com/chrshdl/gt7-simdash/wiki)

</h3>

</div>

---

This is a very simple, lightweight HMI for a Gran Turismo 7 digital display. Written in Python and based on an event-driven architecture, it aims to be the easiest framework to add new features to.

## Install on Raspberry Pi with Blinkt! LED

First do a `pip3 install pipenv` to install the virtualenv management tool. After that edit `~/.profile` and check if `PATH` includes the user's private bin.

```sh
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

Source it by executing `source ~/.profile`. Now you are ready do create the virtual environment and install all dependencies needed by the project. From the repo root execute:

```sh
pipenv --python 3.10 # or 3.11
pipenv shell
pipenv install
```

## Install on macOS

### Recommended: Step-by-step installation (tested working)

**Important:** This project requires Python 3.10 or 3.11 (NOT 3.12) due to deprecated `imp` module usage in some dependencies.

```sh
# Step 1: Install Python 3.10 via Homebrew
brew install python@3.10

# Step 2: Navigate to project directory
cd /path/to/gt7-simdash

# Step 3: Remove any existing virtual environments
rm -rf .venv
pipenv --rm 2>/dev/null || true

# Step 4: Create virtual environment with explicit Python 3.10 path
/opt/homebrew/bin/python3.10 -m venv .venv

# Step 5: Activate virtual environment
source .venv/bin/activate

# Step 6: Verify correct Python version (should show 3.10.x)
python --version

# Step 7: Upgrade pip
pip install --upgrade pip

# Step 8: Install dependencies
pip install -r requirements.txt

# Step 9: Run the application
python main.py
```

### Alternative Options

#### Option 1: Using pipenv (if you prefer it)

First, ensure you have pipenv installed and force Python 3.10:

```sh
pip3 install pipenv

# Remove any existing environment
pipenv --rm

# Create new environment with explicit Python path
pipenv --python /opt/homebrew/bin/python3.10
pipenv install -r requirements.txt
pipenv shell
python main.py
```

#### Option 2: Using Python venv (standard approach)

```sh
# Create virtual environment with Python 3.10
python3.10 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### ⚠️ Important Notes for macOS:

- **Python Version**: Must use Python 3.10 or 3.11 (NOT 3.12)
- **Homebrew Path**: Use explicit path `/opt/homebrew/bin/python3.10` to avoid system Python
- **Platform Packages**: Raspberry Pi packages (`blinkt`, `rpi-lgpio`) are automatically skipped on macOS
- **Dependencies**: All GT7 telemetry and AI features work on macOS without hardware-specific components

## Usage

Start the application from inside the virtual environment with `python main.py`. Enter the IP of your Playstation using the buttons and press OK. The application will attempt to establish a connection with the Playstation. 

<div align="left">
<picture>
  <img width=600px src="https://raw.githubusercontent.com/chrshdl/gt7-simdash/main/assets/gt7-simdash-enter-ip.png" />
</picture>

If the Playstation isn't ready to connect yet (because powered off) you will see a waiting screen. Power on your Playstation and start Gran Turismo 7. Once the opening trailer is shown the application will automatically connect and change to the initial view. Now you are ready to go. Start a race to trigger a car update and the dashboard will show the corresponding telemetry data.

<picture>
  <img width=600px src="https://raw.githubusercontent.com/chrshdl/gt7-simdash/main/assets/gt7-simdash-connecting.png" />
</picture>
</div>

## Troubleshooting

### Python version issues (macOS)

If you encounter `ModuleNotFoundError` or `imp` module errors:

**Problem:** Using Python 3.12 instead of Python 3.10/3.11
```sh
# Check your Python version
python --version
# If it shows Python 3.12.x, you need to use Python 3.10
```

**Solution:** Use the exact working commands from the installation section above.

### pipenv shell issues

If you encounter "Shell for UNKNOWN_VIRTUAL_ENVIRONMENT already activated" error:

1. **Reset the environment:**
   ```sh
   # Exit current shell or open a new terminal
   # Then run:
   pipenv --rm  # Remove existing virtual environment
   pipenv --python /opt/homebrew/bin/python3.10  # Recreate with Python 3.10
   pipenv install -r requirements.txt  # Install dependencies
   pipenv shell  # Activate shell
   ```

2. **Alternative: Use pipenv run directly:**
   ```sh
   pipenv run python main.py
   ```

3. **Check environment status:**
   ```sh
   pipenv --venv  # Show virtual environment path
   pipenv graph   # Show installed packages
   ```

### Raspberry Pi package build errors

If you see build errors for `lgpio` or `rpi.gpio` on macOS:

**Problem:** These are Linux-only packages that can't build on macOS
**Solution:** Use the fixed `requirements.txt` which automatically skips these packages on macOS

### Verification commands

To verify your installation is working:
```sh
# Check Python version (should be 3.10.x or 3.11.x)
python --version

# Test pygame installation
python -c "import pygame; print('Pygame version:', pygame.version.ver)"

# Test GT7 telemetry library
python -c "import granturismo; print('GT7 library imported successfully')"

# Run the application
python main.py
```

## Whats next

- [x] ~~Improve Feed performance~~
- [x] ~~Efficient RPM gauge~~
- [x] ~~Fix LED bugs~~
- [x] ~~Calculate current lap time~~
- [x] ~~Pause current lap measurement if game paused~~
- [x] ~~Show simdash in action~~
- [x] ~~Draw "init" screen on boot / errors~~
- [x] ~~Implement "Set up a new device"~~
- [x] ~~Minimap refinement~~
- [ ] Documentation + quick start guide

## License
All of my code is MIT licensed. Libraries follow their respective licenses.
