DESCRIPTION

The Stay Alive Think and Drive App is a live app that can help you plan your journey by providing intelligent information about your planned travel route.
You can type in any set of destination and source locations (within Georgia) to get a route along with color-coded segments according to the danger level (based on past accident data), odds of accident danger according to current weather conditions and some statistics.

INSTALLATION

A guide on how to install and set up the Stay Alive Think and Drive App

0.) Make sure you have npm set up on your system (help link- https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

1.) Download the file "app_submission.tar"

2.) Untar the file (help link - https://kinsta.com/knowledgebase/unzip-tar-gz/)

3.) Go into the folder "node" inside the app_submission directory and then run npm install 

4.) Run "pip3 install -r python_code/requirements.txt" in order to install the necessary Python dependencies.

5.) Run the command "node index.js." This will set up the backend on port 3000.

6.) Go into the directory maps-app and run "npm i"

7.) Run the command "npm start" in the same directory ("maps-app"). This will render the front end on port 5000 of your system.

8.) Now type the link "http://127.0.0.1:5000/" on your browser, and press enter. You should be able to see the front-end interface on the above link.


EXECUTION

1.) You can enter any destination and source locations (within Georgia) into the form and click the submit button to get the results. 
The current latency to get the results might be high (depending on your system's resources), but this issue will be resolved with the AWS-deployed version of the app in the future.




