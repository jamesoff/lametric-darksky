A LaMetric skill(?) to push DarkSky information to your alarm clock.

Rough-and-ready.

## Configuration/set up

* Sign up for Dark Sky API
* Sign up for LaMetric as a developer
* Create an app. Specify a basic thing for it to display (like a weather icon and "Hello" text). The content to display is pushed by the code when it updates, so you don't need to worry about including enough cards or anything.
* Create (or already have) an S3 bucket which will store the code package during deployment. Doesn't need to be public.
* Install `jq` and sam-local

Create `params.json` as a standard CloudFormation parameters JSON file.

Specify the following keys:

* DarkskyApiKey: your Dark Sky API key
* Latitude: the latitude to fetch weather for
* Longitude: the longitude
* LaMetricToken: your API token for LaMetric
* LaMetricKey: your app key for LaMetric

## Deployment

Something like:

`pip3 install -r requirements.txt` in the `darksky` directory.

In the sam-app directory,
`sam package --template-file template.yaml --s3-bucket YOUR_S3_BUCKET --output-template-file output.yaml`

This pushes the code up to S3 for the deployment to pick up later, and outputs the template for CloudFormation to use.

Then:

`aws cloudformation deploy --template-file output.yaml --stack-name darksky-function --capabilities CAPABILITY_IAM --parameter-overrides $(jq -r '.[] | [.ParameterKey, .ParameterValue] | join("=")' params.json)`

Note that `deploy` doesn't take a params file parameter so we have to fudge it with `jq`.

Every 30 mins (0/30 mins past the hour) the code will run and update your LaMetric. It doesn't run overnight. Modify the `cron(...)` property in the CloudFormation template to adjust.
