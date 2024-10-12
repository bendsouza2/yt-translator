# YT-Translator

### Project Overview
The aim of this project is to provide language learning resources. The project was developed with Spanish as the target language to learn and English as the base language. However this can easily be changed in the project configuration to provide language learning resources for other languages. See project setup for details.

The project is currently still in development and is not yet in mainenance mode.

### Setup
1. Install the requirements to your venv `pip install -r requirements.txt`
2. To be able to import enchant in python we'll need to install the Enchant C library (on Mac)
	* Run `brew install enchant`
	* Configure the environment variables by opening the shell config file (~/.bashrc or ~/.zshrc) and adding the lines:
	 	* `export DYLD_LIBRARY_PATH="<PATH_TO_ENCHANT_INSTALL>:$DYLD_LIBRARY_PATH"`
	 	* `export ENCHANT_LIBRARY_PATH="<PATH_TO_ENCHANT_INSTALL>"`
3. Configure environment variables:
	* OPENAI_API_KEY = <YOUR_API_KEY>
4. Run `npm install` to install the Node.js dependencies (echogarden)
5. In the constants.py file:
	* Set the LANGUAGE_TO_LEARN variable to the language you want to publish language learning videos for: e.g. `LANGUAGE_TO_LEARN = "es`
	* Set the NATIVE_LANGUAGE variable to the language which should be used as a base language to learn the secondary language from: e.g. `NATIVE_LANGUAGE = "en`

