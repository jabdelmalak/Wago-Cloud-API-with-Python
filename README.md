# Wago-Cloud-API-with-Python

Wago Cloud API with Python 
Ex: Import/Export of an Alarm from one account to another

Disclaimer:
This documentation and code are not indicative of best practices in terms of HTTP handling and security. Proceed with the notion that there may very well be additional security measures necessary for your specific use case. This paper was written by a conceited Wago engineer that thinks of himself as a programmer and has a fascination with automated cloud processes.
Much like the Temple of Doom (a REALLY old movie starring Kylo Ren’s dad), proceed at your own risk!
Intro: 
Wago Cloud is an industrialized alternative to the many existing cloud solutions in the current Cloud ecosystem (AWS, Azure, Google Cloud, etc.). With Wago’s specialized approach to the industrial automation world, we create a more streamlined progression while focusing on metric analysis, data management, dashboarding, and alarming.
While the features for the Wago Cloud are expansive and lend themselves to easy startup, Wago has integrated a REST-API for further scalability and automated management. The REST-API allows the user to gain access to many Wago Cloud data points such as subscriptions, alarm settings, live PLC data, and much more.
Ok, so now that I’ve earned my paycheck talking about how great a Wago product is, let’s get into it!

Grabbing API key from Wago Cloud:
First things first, the API key is an authentication tool for utilizing the API. One of several layers of security for a secure cloud connection.
Let’s go ahead and log into your Wago Cloud account via https://cloud.wago.com:
 
Figure 1: cloud.wago.com credentials
On the very top right of the screen, you’ll click on the subscription settings button represented as a stack of pages shown in the picture below. Then you will scroll down to the REST-API tab and click “Create REST-API key”:

 
Figure 2: Subscription settings in Wago Cloud to access API key

Important! You’ll need to keep track of the API Key as this will be needed for most of the HTTP requests later on. If you lose the key, you’ll need to create a new one and retroactively update your program.

Explaining HTTP requests in Python:

For this example, we will be utilizing the Requests library for python which is detailed in the attached link: https://docs.python-requests.org/en/latest/
The main two requests used within the program are GET & POST.
In short, the GET requests main function is for viewing data or other endpoints of interest, while a POST request is used for writing to the endpoint. Essentially, the POST allows you input data and the GET allows you to just ask for data.
More information about each request type can be found here: https://www.w3schools.com/tags/ref_httpmethods.asp
Now that we got over that hot potato explanation, let’s get into some cloud characteristics and Code.

Credentials for Wago Cloud API:

Remember when I said earlier that the API-key was a variable needed to access the cloud API? Well there is another credential needed by the user to initiate GET/POST commands to the API known as the Authorization Token.
The token value expires after 1 hour from the initial post request. It is recommended that the token is saved via an independent variable and re-requested once the hour has expired. In the case of my program which runs not often enough for that to be a concern, I request a new token with each program run.
In order to request a token there is some formatting that needs to be adhered too, pictured below:

 
Figure 3: Wago Cloud API documentation highlighting the Token post formatting


 
Figure 4: Access Token format

Figure 3 is utilizing cURL, but now let’s see how that looks in python and how to validate that the request was acknowledged with no errors.


Token POST request via Python:
 
Figure 5: Setting HTTP request payload via Python 

The POST method for requesting a token is comprised of three parts: URL, Headers, and data (Figure 6).
The URL shows the absolute web path for the specific information specified. 
The headers…well they do a lot. But in this case, the header is used to define how the data is being presented to and from the client.
The data is the information sent to the web service.
 
Figure 6: HTTP POST command via Python for token information

Regarding the output of this function, let’s look at the two print statements below the Find_Token declaration.
Print(Find_Token) will output the HTTP response from the API. This will show whether the message was sent successfully or not.

Print(Find_Token.json()) will format the data received by the Cloud into a python dictionary, a format nearly identical to JSON.

 
Figure 7: Print statements for HTTP response and JSON
Formatting








Figure 8: JSON output string of Find_Token.json()


Swagger for Wago Cloud API:
Now that we have all of the pertinent credentials necessary for reading and writing to the API, let’s talk about what data we can get from the API itself.
A great resource for looking at possible Wago Cloud API data is the Swagger UI. Swagger allows you to look through all of the folders available through the API and the GET/PUT/POST commands within each folder or directory.
The link for the Swagger UI is here: https://cloud.wago.com/api/doc/index.html

 
Figure 9: Swagger UI sample

By selecting the definition, you can view all HTTP commands within that directory.
 
Figure 10: Swagger UI directory/definition drop down

In short, Swagger is a great way to test the function of your requests to the cloud and even get an idea of certain expected formats for each request.



Wago Cloud User Hierarchy:
Remember that the objective of this paper is to take an alarm from one cloud account to another account using this API. 
Keeping that in mind, the first steps should be to find the account that the contains the original alarm and the account that you’d like to copy that alarm to. The giving and receiving accounts, so to speak.
When finding the accounts, we’d need to understand how the accounts are structured. In Wago Cloud, the subscription houses all the users that the administrator assigns. 
Each user within the subscription has a workspace ID that’s used to reference any data requested within that person’s account. 

Finding the Structure:
 
Figure 11: Wago Cloud GET method for subscriptions in Python
Like the POST function in figure 6, the GET function does not require a payload, since we are requesting information. Figure 12 shows the JSON output of that function, highlighting ID, name, and description of each subscription. 
Now we’d need to store the ID for the subscription that houses the workspaces we’re after (Figure 13). Keep in the mind the workspaces don’t have to be within the same subscription, but you will have to reference the proper workspace IDs.







                                                 Figure 12: JSON output for subscription GET

 
Figure 13: Storing subscription ID in variable subscriptionID

The subscriptions.json() output is an array, with each array element providing all information related to each subscription. The subscription I’m interested in is the one named Wago, so I am grabbing the ID specifically from that subscription (Figure 13).

Finding the Workspaces:
We can now use the subscription ID to call the workspace request (figure 14) and a collapsed view of its JSON output (figure 15). 
 
Figure 14: Workspace request and print output

 
Figure 15: Collapsed view of Workspaces JSON string showing ID and Name

We now have a list of all the Workspace IDs for each account within this subscription as well as the names that tie them together. This is essential in reading existing alarm data from the account we’d like to copy alarm data from. 
The first order of business is now to find the two accounts we are interested in working with. Iterating through via For Loop, I am requesting the workspace ID by the name of the account (figure 16).
 
Figure 16: Collecting Workspace ID based on names

Finding available alarms:

Once a workspace ID is collected for both the receiving and accepting accounts, we will now search for all available alarms. The alarms are found within the Alarm configurations URL and the pertinent workspace ID (Figure 17). The output is shown below (Figure 18) which shows one test alarm called “Joe’s other test”…don’t ask what happened to the first one.

 
Figure 17: Alarm configuration GET request using Adam’s workspace ID

 
Figure 18: Collapsed JSON output of the Alarm config GET of Adam’s account 


Finding Value based alarms:
In the world of the Wago cloud, there are several different types of alarms. The main alarm type we will go through is a Value Based Alarm, which ties a variable to a specific variable range, in turn triggering that alarm. 
To access all alarms under the “ValueBased” type class we will be using the code below. The for loop is simply used to create a list of Value based alarms (figure 19).
 
Figure 19: Variable declaration of alarm types & adding alarms to a Python list
Note: This configuration for finding all alarm types and storing them into a list can extend for all different alarm types.

It’s also important to note that within this Wago cloud platform, many alarms are tied to a specific device within the workspace. If you want to link one alarm from one account to another, then you’ll need to link them at the device level. And in order to do that, you’ll need to find device IDs for each account. 
Are you sick of finding things yet? Yeah me too…but hey that’s the beauty of an automated process; you’ll never have to touch the code again after this and it’ll just run without a hitch.
Disclaimer: That last sentence was a bold-faced lie. Debugging never ends. You’ll never rest.
Finding all device ids:
As mentioned before, we’ll need to request all of the device IDs for my account as well as Adam’s. Once that is done, we will store both ideas in their respective arrays. This will then allow us to map alarms from device to device (figure 20).
 
Figure 20: Finding and storing device IDs for Adam’s account and Joe’s account


Changing Alarm JSON format for a POST:
So we’ve reached the final steps of this process and like most things, there are a few difficulties. It turns out that you can’t just take the alarm data from one account and post it to another account. The reason for this…formatting.
The data required for a POST is different than the data coming out of the GET. For value based alarms in particular, you need to map the device, variable structure (Collection), and the variable itself (tagKey) to relevant data of the new account (figure 21).
 
Figure 21: Changing data format for new account

With this new formatting you should now be able to print alarms from one account to the next. Some things to note with this program: 
The mapping of one device’s alarms to another device’s alarms is not an automated process. This is currently done by accessing the structure of AlarmConfig and changing those data points by hand. Of course, this can be done in an automated way (but I’m not clever enough).
The hope for this documentation is to show some functionality within the Wago Cloud API as well as showing a general sequence of events for the code structure when dealing with our API. There may be other developers out there that are more familiar with best practices in terms of security or even logic (In fact there definitely are).
As I post this out in the world I’d love to hear feedback for the code or even the API itself. Wago is constantly investigating new features for our software and product base, so feel free to let me know what you think!


