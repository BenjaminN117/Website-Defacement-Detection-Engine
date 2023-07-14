# Website Defacement Detection Engine (In Development)


## Description

This is an automated defacement detection engine, it allows the web code running on a public server to be compared known correct code stored in an S3 bucket. This allows for rapid detection when websites are defaced and works with the AWS SES system to send notification emails to select users to inform them within minutes of the website being defaced. Along with this it provides a sample of the code that was modified by a potiential threat actor.

## Data Generated

- Time of detection
- Domain of server
- Code that has been modified compared to original code

## Future Improvements

- Begin a redployment process for defaced websites, so they automatically correct themselves
- Integrate with Git so the code doesn't have to be copied into an S3 bucket, it automatically pulls is from Git, meaning the most up to date code from production is being checked
- Get the IP address of the server