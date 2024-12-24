# YT-Translator


## Project Overview
This project aims to provide free and accessible language learning resources in the form of video content created leveraging LLMs. There are three main components to this project:

1. [Video creation]((https://www.youtube.com/channel/UCQjyvCIR9IkG02Q0Wmpz9sQ))
2. Web backend
3. [Web frontend](videos.internationalwordoftheday.info)


The project was created with Spanish as the target language to learn, and English as the base language. However, this can easily be customised to provide language learning resources for other languages. I have written [detailed documentation](https://github.com/bendsouza2/yt-translator/tree/main/python/README.md) on the video creation side of the project, which you can [view here](https://github.com/bendsouza2/yt-translator/tree/main/python/README.md) if you want to clone the project for your own use case. 


You can [watch the videos here.](https://www.youtube.com/channel/UCQjyvCIR9IkG02Q0Wmpz9sQ) New videos are uploaded every day at 12pm UTC. 

Or [go straight to the website.](videos.internationalwordoftheday.info)


## Developer Customisation - Video Uploads

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
   - This presents another problem as the Lambda function won't be able to make API calls from within a VPC. [See the docs](https://repost.aws/knowledge-center/internet-access-lambda-function) on how to allow the Lambda function to make API calls from within a VPC

10. Setup a trigger for the Lambda function. Mine is just running a CRON job using EventBridge.


## Potential Problems (Video Generation)
Some problems I encountered in setup or that you might encounter if working with the project for the first time:

* I'm using enchant to verify that the 'word of the day' is real. The dockerfile handles the install of enchant, but if you're working with a new language, the dictionary for that language may not be pre-installed. You can find a list of [available language dictionaries here.](https://cgit.freedesktop.org/libreoffice/dictionaries/tree/) If you need to install a new dictionary, just add a line to the docker file:
   - `curl -o <LINK_TO_DICT_FILE>`


## Backend Setup

The backend is built using Django, connects to the frontend via REST APIs and is hosted on AWS EC2. Data is stored and managed in a MySQL instance hosted in AWS RDS. General instructions on the setup are below.

1. Create your EC2 instance and configure the Amazon Machine Image, instance type and network settings. 
   - This repo is built for ARM64 architecture, so I'd recommend going with ARM64 for compatability.
   - Make sure to create a new key pair for the new instance.
   - Using AWS CLI you can run:
      - `aws ec2 run-instances --image-id <AMI_IMAGE_ID> --instance-type <INSTANCE_TYPE> --network-interfaces '{"AssociatePublicIpAddress":true,"DeviceIndex":0,"Groups":["sg-preview-1"]}' --credit-specification '{"CpuCredits":"unlimited"}' --metadata-options '{"HttpEndpoint":"enabled","HttpPutResponseHopLimit":2,"HttpTokens":"required"}' --private-dns-name-options '{"HostnameType":"ip-name","EnableResourceNameDnsARecord":true,"EnableResourceNameDnsAAAARecord":false}' --count "1" `
   - Also make sure ports 80 (HTTP) and 443 (HTTPS) are open.
2. Add an inbound rule to make sure the VPC hosting your RDS instance allows access from the EC2 instance.
3. Use `scp` to transfer the cluster_setup.sh script to your EC2 instance:
   - `scp app/setup-script.sh ec2-user@<your-ec2-ip>:~/`
4. SSH into the EC2 instance and run the script. 
   - `./setup-script.sh`
5. Make sure there's a valid SSL certificate, run:
   - `sudo certbot certonly --standalone --preferred-challenges http --email your-email@example.com -d yourdomain.com`
6. Setup Gunicorn and configure it to use the SSL cert.
   - Create a new service file: `sudo nano /etc/systemd/system/gunicorn.service`
      - Make sure the ExecStart is pointing to the right location, using the correct port and using your wsgi application.
      - Also make sure that the user used in the Gunicorn service file has access to read the SSL .pem files, as these might be restricted.
   - To start gunicorn run the below:
      - `sudo systemctl daemon-reload`
      - `sudo systemctl start gunicorn`
      - `sudo systemctl enable gunicorn`
   - To check it's running correctly, run:
      - `sudo systemctl status gunicorn`
7. Install and [setup Nginx](https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview) or handle redirection within Django. To force secure connections with Django, update the settings.py file:
   - `SECURE_SSL_REDIRECT = True`
   - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') `




## Project Structure


```plaintext
yt_translator/
├── requirements.txt
├── base_config.py
├── python/                  # Contains video generation in Python
│   ├── Dockerfile
│   ├── lambda_handler.py
├── node/                    # Contains video generation in Node.js
├── app/                     # Django files
│   ├── video_host/          # Central project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── today/               # Latest day's videos and related APIs/models
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── views.py
│   ├── manage.py
├── frontend/                # Vue.js files
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── webpack.config.js



