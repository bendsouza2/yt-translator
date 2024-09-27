# YT-Translator

### Setup
1. Install the requirements to your venv `pip install -r requirements.txt`
2. To be able to import enchant in python we'll need to install the Enchant C library (on Mac)
	* Run `brew install enchant`
	* Configure the environment variables by opening the shell config file (~/.bashrc or ~/.zshrc) and adding the lines:
	 `export DYLD_LIBRARY_PATH="<PATH_TO_ENCHANT_INSTALL>:$DYLD_LIBRARY_PATH"
	 export ENCHANT_LIBRARY_PATH="<PATH_TO_ENCHANT_INSTALL>"`

