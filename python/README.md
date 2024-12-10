## Overview
This readme documents how to implement the video upload functionality. For a general project overview, including website setup, see the [main documentation.](https://github.com/bendsouza2/yt-translator)

## Video Creation
Videos are created and uploaded by a Lambda function which runs once a day. This function:
	* Interacts with OpenAI (Dalle) to generate images
	* Uses LLMs to create a word of the day and associated sentences/definitions for the word
	* Combines audio, text and images to generate a video using moviepy
	* Uploads the generated content to YouTube
	* Logs the video creation and metadata to a MySQL DB

## Developer Customisation

The project defaults to creating Spanish language learning content but has been designed to be easily customisable for other languages.

To customise the project and deploy the video creation capabilities, complete the following steps:

1. Clone the repository

2. In the constants.py file:
   - Set the LANGUAGE_TO_LEARN variable to the language you want to publish language learning videos for: e.g. `LANGUAGE_TO_LEARN = "es"`
   - Set the NATIVE_LANGUAGE variable to the language which should be used as a base language to learn the secondary language from: e.g. `NATIVE_LANGUAGE = "en"`

3. You'll need to authorise the uploader app. You can do this by running the yt_authenticator.py script, which will take you to an oauth consent screen. Follow the prompts in your browser and click 'Allow all'. The oauth creds should automatically be written to your local directory and saved as an environment variable. 


4. Build the docker image, in the base directory run:
   - `docker build -t <IMAGE_NAME> -f python/Dockerfile .`

5. Push the docker image to ECR. Assuming you have [configured your AWS CLI profile](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html) and setup the ECR repo, run:
   - `docker tag <REPO_NAME/IMAGE_NAME> <LINK_TO_REPO/IMAGE_NAME>`
   - `docker push <LINK_TO_REPO/IMAGE_NAME>`

6. Create a new Lambda function using the image hosted in ECR.
   - Note that the image is built for arm64 architecture, so make sure to specify that in the Lambda configuration
   - The default timeout on Lambda is 3 seconds. From my tests the function takes about a minute to run, so you'll need to increase the timeout limit.

7. Make sure the below environment variables have been added to the Lambda function:
   - `DB_HOST` = The RDS endpoint for the database
   - `DB_USER` = The username with read/write access
   - `DB_PASSWORD` = The password for the username
   - `DB_NAME` = The name of the database
   - `YT_CREDENTIALS` = The oauth credentials, including refresh token and access token

8. Assign an IAM role to the Lambda function which has the following permissions attached:
   - AmazonS3FullAccess
   - AmazonRDSFullAccess
   - AWSLambdaBasicExecutionRole

9. Assuming your RDS instance is within a VPC your Lambda function needs to be within the same VPC to access it (Lambda functions don't have a static IP, so you can't just add an inbound rule allowing access from the Lambda function's IP).
   - This presents another problem as the Lambda function won't be able to make API calls from within a VPC. (See the docs)[https://repost.aws/knowledge-center/internet-access-lambda-function] on how to allow the Lambda function to make API calls from within a VPC

10. Setup a trigger for the Lambda function. Mine is just running a CRON job using EventBridge.

