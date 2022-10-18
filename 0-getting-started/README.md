# Prerequisites to ensure you have the smoothest experience for the hackathon

## Credentials
To write programs which automatically fetch data from reddit or twitter, you need to generate credentials which let your code authenticate with those websites. This is a guide on how to obtain them, as it's a little bit tedious. Only one set of credentials is required per hackathon team / project.

### 1- get twitter credentials
To get twitter credentials, you will first need a regular twitter account.<br>
We suggest creating a dummy one using your student or academic email if you have one, as many university domains are whitelisted by twitter so they will approve your request instantly.<br>
Using a personal email or twitter account that you already use is also fine, as the name of the account or its info will be completely seperate from the project.<br>
You need to have a confirmed phone number associated to your twitter account to make the request, but you can later remove that number (which we suggest) once this is done. You can also confirm multiple twitter accounts with a single number (also tried). To do this go to the normal twitter consumer frontpage, click the "more" section in the side panel on the left > "Setting and Security" > "Your Account" > "Account information".

1) with a twitter account logged in and a phone number verified, visit `https://developer.twitter.com/en/portal/petition/essential/basic-info`.
2) fill in your basic info, and follow through the steps. At the end of the process you'll be asked to do some multiple factor authentication which will be either an email or a text message.
3) Once the above is done you will be prompted to "Create an app". This may sound confusing, but it is simply the way twitter organizes your keys for different projects a developer may have. It doesn't matter at all what name you give it, but in the off chance they run some NLP methods to check whether they approve you, do **NOT** call it something like "twitter clone to steal all their users" or "super money maker 3000".
4) Fill in the form to create an app, write something like "university project to learn about machine learning" every time they ask you describe your usage, and make sure to answer all questions about monetization or government use with a no. If you don't get a form (happens with some email domains) then good for you.
5) It shows you your _API_ key and secret. You don't need to save them just yet because the ones you see here don't yet have the right privileges for our usage of the API.
6) To get the right priviledges, Go to your [twitter developper portal](https://developer.twitter.com/en/portal/dashboard) and from the left-side panel navigate to "Products" > "Twitter API". On the top of that page click the "Elevated" tab, click "Apply". Check that the info in the form that opens is correct, and fill-in what needs to be filled in. Under "The Specifics", only check the first box (uncheck all others), and write something nice for the twitter NLP verification bot to read :)
7) Now, still in the developer Dashboard, go back to the [projects dashboard](https://developer.twitter.com/en/portal/) and make sure there is a little grey badge that says "elevated" above the "Projects" box. If there isn't you might have to wait anywhere between a minute to a day (this means you wrote something too spicy for the verification bot and a human has to check your request). If there is, click your project and click the "keys" tab.
8) Now generate/regenerate everything and _this time_ save the credentials you see to a file somewhere (**SUPER IMPORTANT**). <br>Remember to also write down which string corresponds to what (key, secret, etc), to save your future self frustration. In theory, credentials like this should be treated almost like an account password and not shared, but in practice you can send them to the team groupchat.

At this point you should have a text or config file `twitter_creds` which has something like:
```
API_key=
API_secret=
access_token=
access_secret=
```


### 2- get reddit credentials
The reddit api doesn't have access keys and credentials like many others, but you still need an "App ID" and secret to authenticate with it.<br>
You will need a reddit account, it can be created with any email.
To get your credentials, the following guide works well:
https://github.com/reddit-archive/reddit/wiki/OAuth2
When asked to provide a "redirect uri", you can just put `http://localhost:8080`.<br>
Here you don't need to save anything, once you've created an app with the above guide, all info will be stored on your [apps dashboard](https://www.reddit.com/prefs/apps) on reddit in plaintext.
## Setup a Google Cloud Platform account and project
### 0- Intro
Google cloud platform provides all the components you would expect a server or computer to have (environments to run code, networking, storage, databases, etc) in the form of *managed services*, where you as a developer don't need to worry about the details of how the services you need are implemented.<br><br>

To be able to collaborate on deploying your model and the associated automation code to the cloud, every team member should have a google account. <br>One team member should have a credit card that they are willing to provide Google with. No money will be charged from the card for this project, as you normally receive 300€ worth of Google Cloud credits upon starting, and we will be running services which don't typically cost that much, during a relatively short period of time.
<br>

### 1- Basics (only the "project owner" should do this)
Navigate to https://console.cloud.google.com/ and click the dropdown list at the top right next to the Google Cloud logo. In the window that opens, click "new project" at the top. Name the project, don't give it an organisation name, and click create. Once it's ready and you can switch to it do so and this is where the fun begins.<br>
In the search bar at the top, search "IAM and admin", or go to https://console.cloud.google.com/iam-admin/, and at the top click on "Grant Access", and add the emails of everyone in your team with the role "Owner".<br><br>
Finally, try opening the tab for another service, or searching for a new one like "BigQuery", "Cloud Run", or "Cloud Storage" (all services we will use, though you can try something else) and open that service's start page.<br> When you start using a scalable service available in Google Cloud for the first time, you are prompted to "enable the API" for this service. The first time you enable the API for a service you will be be able to setup a payment method which is required to start a trial period with your free credits. You can later remove the payment method, and as long as you don't go over to 300 € limit, not a cent will be charged from your card.
### 2- Download and configure the Google cloud CLI to interact with your project from a terminal (everyone should do this)
As you might have noticed, the Google Cloud web console (UI) has all the information you need, but it is clunky and rather slow. We'll try to favor using the cloud command line interface, to configure and create the services we need. You can install it for your platform by following [this link](https://cloud.google.com/sdk/docs/install9).<br>
In theory, everything that can be done from the web console can also be done from the CLI and vice versa. In practice, new services and objects are generally created from the web console, and the configuration of existing ones is done from the CLI. We will try to stick to this pattern during these tutorials.