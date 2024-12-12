from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient

AccountManagementAgent = '''AWS STEPS -
 DigitalEx allows users to onboard AWS Billing and Usage Accounts.
 Billing Account
 The billing account in an AWS organization is the management account that is used to manage the AWS accounts and pay for charges that 
are incurred by the member accounts. This account has the responsibilities of a payer account and cannot be changed, as it is the 
organization's management account. It is important to properly set up and manage the billing account in an AWS organization to ensure that 
charges are accurately tracked and paid in a timely manner.
 Usage Account
 A usage account in an AWS organization is a member account, which is any account that is not the management account. Member 
accounts make up all of the other accounts in the organization and can only be a member of one organization at a time. Policies can be 
attached to a usage account to apply controls specifically to that account. It is important to properly set up and manage member accounts in 
an AWS organization to ensure that resources are used effectively and in accordance with organizational policies and controls.
 31
AWS Biling Account Onboarding
 There are two ways to onboard AWS Billing accounts.
 1. Manual Onboarding
 Manual Onboarding 
You can onboard a Billing account in either of the below ways:
 Onboarding using Role ARN 
Onboarding using Access/Secret key 
2. Manual CLI Onboarding
 AWS Billing Account Manual CLI Onboarding 
3. Cloud Formation Based Onboarding (Automated)
 Cloud Formation Based Onboarding 
32
Manual Onboarding
 The process of onboarding a billing account manually involves below steps.
 Step-1: Enable CUR & Cost Explorer
 Step-2: Enable Cost Allocation Tags
 Step-3: Create Role / IAM User
 Step-4: Retrieve AWS Billing Account ID.
 Step-5: Connect Billing Account on DigitalEx Dashboard
 33
Step-1: Enable CUR & Cost Explorer
 If you have cost and usage reports already created follow Use already created report otherwise Create new report
 Use already created report
 1. Log into AWS Console and go to Billing service
 2. On the billing page, look for Cost & Usage Reports section
 3. Out of multiple available reports, choose the oldest and the one having following properties
 a. Time granularity : Daily / Hourly
 b. File format : text/csv
 4. Capture the S3 bucket, Report path prefix fields from the report details section for the report you chose in the previous step
 34
5. Go to 
Step-2: Enable Cost Allocation Tags 
Creating New Report
 1. Log into AWS Console and go to Billing service
 2. On the billing page, select Cost & Usage Reports section from the sidebar and click Create Report
 3. Give the name of your choice and enable the below options 
a. Include Resource IDs
 b. Split cost allocation data
 c. Automatically refresh your Cost & Usage Report when charges are detected for previous months with closed bills
 35
4. Click Next
 a. configure bucket by choosing one of the existing or creating a new one
 b. set following properties
 i. Enter the S3 path prefix 
ii. Time granularity : Daily
 iii. Report versioning : overwrite existing report
 iv. Compression type : GZIP
 36
5. Click Next -> Review and complete
 6. Click on the Report created and Capture Bucket Name, Report Path.
 37
7. To enable cost explorer follow the steps mentioned here  
Enabling Cost Explorer - AWS Cost Management 
AWS takes up to 24 hours to create first report to the configured bucket
 38
Step-2: Enable Cost Alocation Tags
 Below are the steps to Enable Cost Allocation Tags:
 1. Log into AWS Console and go to Billing from the Services tab.
 2. On the Billing page, click on Cost Allocation Tags
 3. Click on AWS Generated cost Allocation tags.
 39
4. Select the tags you want to use as dimensions for grouping and filtering cost data and click on Activate to activate them.
 40
Step-3: Create Role / IAM User
 DigitalEx supports both types of AWS authentications,
 1. Role Based
 2. Access/Secret Key Based
 Role-based access is generally considered to be more secure than user-based access, as it allows organizations to control access to 
resources and functions based on defined roles and responsibilities. We recommend using roles over individual users whenever possible
 Creating Role
 1. Go to IAM from the Services tab.
 2. Click on Roles from the left menu options and Click on 
Create Role
 3. Select 
AWS Accounts and select 
Another AWS Account from 
an AWS Account  tab
 41
a. specify 
Account ID as 
911403356698 (This is the Account Id of DigitalEx which is universal)
 b. Check on options 
Require external ID and enter the tenant id. To get the tenant id to follow instructions,
 i. Login to DigitalEx
 ii. From the side menu, select 
API under the 
Admin section
 iii. Capture the Tenant ID & enter it into the External ID field
 4. Click 
Next: Permissions , don’t select any permissions
 5. Click 
Next: Tags
 6. Click 
Next: Review 
42
Enter the role name with prefix 'digitalex-' e.g: digitalex-rolename
 7. Enter the Role Name of your choice and Click Create Role.
 8. A new role should be created and displayed on the list.
 9. Click on the newly created Role which is navigated to the below page
 10. Click on 
Add Permissions -> Create Inline Policy under 
Permissions Tab & Click on 
following JSON
 11. JSON
 1 { 
2   
3    
4        
5            
6            
"Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 JSON tab & replace existing JSON with the 
"Action": [
 43
44
 12. And replace <BUCKET_NAME> on lines 11 & 12 with the name of the bucket captured in Step-1: Enable CUR & Cost Explorer 
13. Review Policy, Name it & Click Create policy
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31        },
 32        {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:Get*",
 36                "iam:List*",
 37                "iam:SimulateCustomPolicy",
 38                "iam:SimulatePrincipalPolicy"
 39            ],
 40            "Resource": "*"
 41        },
 42        {
 43     "Effect": "Allow",
 44     "Action": [
 45                "cur:Get*",
 46                "cur:ValidateReportDestination",
 47                "cur:Describe*"
 48      ],
 49     "Resource": "*"
 50 }
 51    ]
 52 }
14. Capture 
Role ARN of the role we created from the summary section for the next steps.
 Creating IAM User & Access/Secret Keys
 This step is not required if you have created a Role.
 1. Go to IAM from the Services tab & navigate to Users tab
 45
2. Click Add Users, enter name of your choice 
3. Skip permissions for now. Keep doing Next & finally Create User.
 4. Open the User you have created & click on Security credentials.
 5. Scroll down & click on Create access key
 46
6. Select Others  & click on next
 7. Click on Create Access Key 
8. Save Access key ID and Secret access key for later use. 
9. Click Done
 10. Navigate to the details of the user we just created
 47
48
 11. Click Add Inline Policy under Permissions Tab & Click on JSON tab & replace existing JSON with the following JSON
 a. JSON
 1 { 
2   "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31        },
 32        {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:Get*",
 36                "iam:List*",
 37                "iam:SimulateCustomPolicy",
 38                "iam:SimulatePrincipalPolicy"
39            
40            
41        
42        
43     
44     
45                
46                
47                
48      
49     
50 }
 51    
52 }
 b. And replace 
],
 "Resource": "*"
 },
 {
 "Effect": "Allow",
 "Action": [
 ],
 "cur:Get*",
 "cur:ValidateReportDestination",
 "cur:Describe*"
 "Resource": "*"
 ]
 <BUCKET_NAME> on lines 11 & 12 with the name of the bucket captured in 
12. Review the policy & click create
 Step-1: Enable CUR & Cost Explorer 
49
Step-4: Retrieve AWS Biling Account ID.
 Below are the steps to Retrieve AWS Billing Account ID:
 1. Go to My Account page.
 2. On the My Account page, note the Account Id.
 50
Step-5: Connect Biling Account on DigitalEx Dashboard
 If you are onboarding an account for the first time, you will be presented with a screen that allows you to select the option to create a billing 
account
 Below are the steps to Create a Billing account:
 1. Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 51
2. Fill in the following details
 Account ID (
 Step-4: Retrieve AWS Billing Account ID. )
 Role ARN or Access/Secret Key (
 Bucket Name, Report Path (
 & Click +Billing Account
 Step-3: Create Role / IAM User )
 Step-1: Enable CUR & Cost Explorer )
 3. Click Connect
 4. The onboarded Management Account will be displayed with the list of All linked Member accounts.
 After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 52
5. Click Data Ingestion to skip waiting 
6. Go to the Menu option and Click Cost. 
7. Data will display immediately after successful ingestion.
 53
54
55
 AWS Billing Account Manual CLI Onboarding
 The steps below need to be executed in the AWS Cloud Shell. Please sign into the AWS console using the admin 
account where billing has been set up, and then initiate the Cloud Shell from the navigation bar.
 Step-1:  Configure Cost Export
 1. Use existing report
 a. Check if the cost report exists with Time granularity : Daily / Hourly and File format : text/csv
 If above command returns only one cost record then capture S3Bucket, S3Prefix and Report Name
 If above command returns more than one report then choose oldest record from UI.
 Log into AWS Console and go to Billing service
 On the billing page, look for Cost & Usage Reports section
 Out of multiple available reports, choose the oldest and the one having following properties
 a. Time granularity : Daily / Hourly
 b. File format : text/csv
 Capture the S3 bucket, Report path prefix fields from the report details section for the report you
 2. Creating new report (This step is not required if you have a exiting report)
 a. Create new S3 bucket by entering <S3BucketName> (Skip this step if you want to use exiting S3 bucket)
 b. Apply policy to S3 bucket by entering <S3BucketName> and AWS billing account id
 1 aws cur --region us-east-1 describe-report-definitions --max-items 5 --query "ReportDefinitions[?
 TimeUnit=='DAILY'||TimeUnit=='HOURLY' && Format=='textORcsv'].{ReportName:ReportName, S3Bucket: S3Bucket, 
S3Prefix: S3Prefix}"
 1 aws s3 mb s3://<S3BucketName>
 1 aws s3api put-bucket-policy --bucket <S3BucketName> --policy '{
 2  "Statement": [
 3    {
 4      "Effect": "Allow",
 5      "Principal": {
 6        "Service": "billingreports.amazonaws.com"
 7      },
 8      "Action": [
 9        "s3:GetBucketAcl",
 10        "s3:GetBucketPolicy"
 11      ],
 12      "Resource": "arn:aws:s3:::<S3BucketName>",
 13      "Condition": {
 14        "StringEquals": {
 15          "aws:SourceArn": "arn:aws:cur:us-east-1:<AccountId>:definition/*",
 16          "aws:SourceAccount": "<AccountId>"
 17        }
 18      }
 19    },
 20    {
 21      "Sid": "Stmt1335892526596",
 22      "Effect": "Allow",
 23      "Principal": {
 24        "Service": "billingreports.amazonaws.com"
56
 c. Create new cost and usage report by entering <ReportName> of your choice, <S3BucketName> & <S3BucketPrefix> 
created/caputured in above steps 
Step-2: Enable Cost Allocation Tags
 1. List cost allocation tags and capture the tags you want to use as dimensions for grouping and filtering cost data.
 2.  Active cost allocation tags which you want from above tags by entering <"TagValue">
 Step-3: Create Role / IAM User
 1. Role Based 
Role-based access is generally considered to be more secure than user-based access, as it allows organizations to control access to 
resources and functions based on defined roles and responsibilities. We recommend using roles over individual users whenever 
possible.
 a. Create Role by Entering RoleName of your choice and tenantid(provided by your partner) and capture role ARN from output
 25      },
 26      "Action": "s3:PutObject",
 27      "Resource": "arn:aws:s3:::<S3BucketName>/*",
 28      "Condition": {
 29        "StringEquals": {
 30          "aws:SourceArn": "arn:aws:cur:us-east-1:<AccountId>:definition/*",
 31          "aws:SourceAccount": "<AccountId>"
 32        }
 33      }
 34    }
 35  ]
 36 }'
 1 aws cur put-report-definition --region us-east-1 --report-definition '{
 2    "ReportName": "<ReportName>",
 3    "TimeUnit": "DAILY",
 4    "Format": "textORcsv",
 5    "Compression": "GZIP",
 6    "AdditionalSchemaElements": [
 7      "RESOURCES"
 8    ],
 9    "S3Bucket": "<S3BucketName>",
 10    "S3Prefix": "<S3BucketPrefix>",
 11    "S3Region": "us-east-1",
 12    "AdditionalArtifacts": [],
 13    "RefreshClosedReports": true,
 14    "ReportVersioning": "OVERWRITE_REPORT"
 15  }'
 AWS takes up to 24 hours to create first report to the configured bucket
 1 aws ce list-cost-allocation-tags
 1 aws ce update-cost-allocation-tags-status --cost-allocation-tags-status TagKey=<"TagValue">,Status=Active 
TagKey=<"TagValue">,Status=Active
57
 b. Update role policy by entering <RoleName> created above, <PolicyName> of your choice. Enter <S3BucketName> captured from 
Step-1 while configuring Cost report
 1 aws iam create-role --role-name <RoleName> --assume-role-policy-document '{
 2    "Version": "2012-10-17",
 3    "Statement": [
 4      {
 5        "Effect": "Allow",
 6        "Principal": {
 7          "AWS": "arn:aws:iam::911403356698:root"
 8        },
 9        "Action": "sts:AssumeRole",
 10        "Condition": {
 11          "StringEquals": {
 12            "sts:ExternalId": "<tenantid>"
 13          }
 14        }
 15      }
 16    ]
 17  }'
 1 aws iam put-role-policy --role-name <RoleName> --policy-name <PolicyName>  --policy-document '{
 2  "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31            },
 32            {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:Get*",
 36                "iam:List*",
 37                "iam:SimulateCustomPolicy",
 38                "iam:SimulatePrincipalPolicy"
58
 2. Access/Secret Key Based (This step is not required if you have created a Role)
 a. Create User by Entering <UserName> of your choice
 b. Update user policy by Entering <UserName> created above,Enter <PolicyName> of your choice. Enter <S3BucketName> captured 
from Step-1 while configuring Cost report
 39            ],
 40            "Resource": "*"
 41        }
 42        {
 43     "Effect": "Allow",
 44     "Action": [
 45                "cur:Get*",
 46                "cur:ValidateReportDestination",
 47                "cur:Describe*"
 48      ],
 49     "Resource": "*"
 50 }
 51    ]
 52 }'
 1 aws iam create-user --user-name <UserName>
 1 aws iam put-role-policy --role-name <RoleName> --policy-name <PolicyName>  --policy-document '{
 2  "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31            },
 32            {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:Get*",
 36                "iam:List*",
37                
38                
39            
40            
41        
42        
43     
44     
45                
46                
47                
48      
49     
50 }
 51    
52 }'
 "iam:SimulateCustomPolicy",
 "iam:SimulatePrincipalPolicy"
 ],
 "Resource": "*"
 }
 {
 "Effect": "Allow",
 "Action": [
 ],
 "cur:Get*",
 "cur:ValidateReportDestination",
 "cur:Describe*"
 "Resource": "*"
 ]
 c. Create AccessKey and SecretAccessKey
 1 aws iam create-access-key --user-name ${UserName}
 Step-4: Get Account ID 
1. Get your Account ID
 1 aws sts get-caller-identity --query Account --output text
 Step-5: Submit Details in DigitalEx
 Get the details Account ID, Role ARN or Access/Secret Key, Bucket Name, Report Path Prefix
 Follow the below steps to onboard the billing account in DigitalEx.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link Azure Connect Billing Account for Partner to onboard additional providers
 59
1. Click on AWS Provider
 2. Click on Connect manually.
 3. Click on Connect Billing Account
 4. Enter the details which you have captured above.
 5. Click on connect & done.
 If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1. Navigate to Menu > Admin > Public Clouds > +Account.
 60
2. Click on AWS Provider & Click on Manual tab.
 3. Enter the details which you have captured above.
 5. The onboarded Billing Account will be displayed with the list of All linked Subscription accounts.
 4. Click Connect
 61
After adding a new account, it may take up to 30 minutes for the system to discover and process the data.
 6. Go to the Menu option and Click Cost.
 7. Data will display immediately after successful ingestion.
 62
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
63
Cloud Formation Based Onboarding
 The process of onboarding a billing account for use with CloudFormation involves below steps
 Step-1: Login to AWS account 
Step-2: Run Template 
"Here is the link to the CloudFormation template for the billing account onboarding."
 Billing Account CFN Template
 64
Step-1: Login to AWS account
 Onboarding from DigitalEx setup page 
Below is the setup page displayed if user login for the first time and didn’t onboarded any cloud providers
 1. Click the Login button and page is navigated to the AWS login page where the user needs to enter AWS credentials. After successful 
login into the AWS account Enable Cost Explorer, the user should come back to DigitalEx to Run Template
 2. After Login to AWS  follow Step 2 
Step-2: Run Template 
Onboarding from DigitalEx Admin page
 If user already onboarded any of the cloud provider below are the steps that needs to be performed 
1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 65
4. Click on +Account
 5. Click Cloud Formation 
66
6. Click the Login button and page is navigated to the AWS login page where the user needs to enter AWS credentials. After successful 
login into the AWS account Enable Cost Explorer, the user should come back to DigitalEx to perform 
https://digitalexio.atlassian.net/wiki/spaces/MCX/pages/39977120 
67
Step-2: Run Template
 Onboarding from DigitalEx setup page
 Click Run Template after completing 
Step-1: Login to AWS account 
1. Page is navigated to AWS cloud formation where all the details will be auto-generated as shown in the below snap.
 68
2. Check I acknowledge that AWS Cloud Formation might create IAM resources.
 3. Click Create Stack button and wait till the template running is completed and status in AWS shows as CREATE_COMPLETE.
 4. Click Done Button as shown in the image below.
 69
5. Click on Proceed to Dashboard
 Onboarding from DigitalEx Admin page
 If user already onboarded any of the cloud provider below are the steps that needs to be performed 
1. Click Run Template. 
70
2. The page is navigated to AWS cloud formation where all the details will be auto-generated as shown below snap.
 3. Check I acknowledge that AWS Cloud Formation might create IAM resources.
 4. Click Create Stack button and wait till the template running is completed and the status in AWS shows as CREATE_COMPLETE.
 71
5. Click on the Done button in DigitalEx after the template running is successfully completed.
 6. The onboarded Management Account will be displayed with the list of All linked Member account.
 Wait for next scheduled ingestion(once in 6hrs) to be completed to see cost data
 7. Go to the Menu option and Click Cost. 
72
8. Data will display immediately after successful ingestion.
 73
The following are the steps you should take if you're unable to view cost data from the previous 13 months
 If the data for previous months isn't visible on cost dashboard due to missing historical Cost and Usage Report (CUR) files, there are a 
couple of solutions to retrieve the data:
 1. Request the missing month's CUR from AWS Support. Ensure to designate the same bucket you used during the onboarding process 
and request them to upload the CUR file into that specific bucket.
 2. Leverage AWS Explorer APIs, which charge based on the usage account. This cost is a one-time fee. If you choose this route, follow the 
steps outlined below.
 Click on Menu > Admin > Public Clouds
 Click on AWS Tab > Edit Icon > Configure
 Enable the Toggle, Click Ok & Done
 Wait for next scheduled ingestion(once in 6hrs) to be completed to see cost data
 74
75
Cloudformation Description
 Cloudformation Template executes below functions needed to onboard the AWS Billing Account and Usage Account.
 Function Name
 Description
 BucketName
 CloudWizBillingOnboardingFunctionRole
 ReportName
 RoleName
 FunctionName
 RoleForConfig
 RoleForUsageOnboardingFunctionExec
 BucketName
 ConfigurationRecorderName
 DeliveryChannelName 
RoleName
 Bucket is where the Reports are stored. DigitalEx 
uses existing bucket or creates a new one if no 
existing bucket is found.
 This requires to execute the Lamdba function
 This is the name of the report created in S3
 This is the Role created for onboarding in DigitalEx
 Description
 This is the role created for Config to track resource 
inventory and changes
 This requires to execute the Lamdba function
 Bucket is where the Reports are stored. 
MultoCloudX uses existing bucket or creates a new 
one if no existing bucket is found.
 This requires to record the resources.
 This is the role created for onboarding in DigitalEx
 SnsTopicName 
76
AWS Control Tower Biling Account Onboarding
 You need to follow the below sequence while onboarding Control Tower Account :
 1. Audit
 2. Log Archive
 3. Other Accounts
 Click on the below link to onboard the AWS Control Tower Billing Account    
AWS Billing Account Onboarding 
77
Update AWS Management Account Manualy.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Edit Button
 4. Enter new Role ARN
 78
5. Click on Update
 6. AWS Management account will get Updated Successfully.
 79
Update AWS Management Account Using Cloudshel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Edit Button
 4. Click on the login button(AWS CloudShell will get opened)
 Note: Make sure you are logged in to AWS provider account
 80
5. Copy the script 
6. Paste the script into AWS CloudShell & Click Enter
 7. Come back to DigitalEx & click on Done
 8. AWS Management account will get Updated Successfully.
 81
AWS Member Account Onboarding
 There are three ways to on-board AWS Usage accounts.
 1. Manual Onboarding
 AWS Member Account Manual Onboarding 
2. Cloud Formation Based Onboarding (Bulk Onboarding)
 AWS Member Account CloudFormation Onboarding (Org) 
3. Cloud Formation Based Onboarding (Individual Onboarding)
 AWS Member Account CloudFormation Onboarding 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
82
AWS Member Account Manual Onboarding
 Step-1:Enable Compute Optimizer
 Step-2: Create an IAM role for DigitalEx
 83
Step-1:Enable Compute Optimizer
 This step should be carried out for every individual member account.
 1. Login to your AWS Member account as Administrator
 2. Then search for AWS Compute Optimizer in a search bar & select it. You will land on the home page of Compute Optimizer Service
 3. Click on Get started
 84
Step-2: Create an IAM role for DigitalEx
 This steps only provides illustrations on creating a role but a user with access/secret key is also supported. If you wish to create a 
user, please assign similar permissions as documented for a role below. We encourage a use of a Role over a User as its more 
secure.
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Roles from the left menu, and click 
IAM service using 
Create role . One the create role screen please select the 
configuration as follows
 a. Trusted entity type: AWS Account
 b. An AWS account: Choose 
Another AWS account and fill in the account number as 
911403356698
 Next
 c. External ID: In this field, please put the Tenant ID for your DigitalEx account. To get the tenant id follow instructions outlined in this 
page Retrieve the Tenant Id
 d. Finally click 
85
3. Click 
Next , on next screen for permissions, please choose 'All Types' in the filter and select the listed policies below.
 ReadOnlyAccess
 ViewOnlyAccess
 IAMReadOnlyAccess
 CloudWatchReadOnlyAccess
 ComputeOptimizerReadOnlyAccess
 AWSOrganizationsReadOnlyAccess
 86
4. Click 
Next again & on a final page, give a name to the role & click 
Create role
 5. Open the newly created role 
6. Click on Add permissions → Create inline policy.
 7. Search for Cost Explorer Service
 8. Click on Write → 
StartSavingsPlansPurchaseRecommendationGeneration →
 9. Enter the policy name. 
10. Click on
 Create policy .
 Next
 11. Once the role is created, please note the ARN of a role, which will be required in the next step.
 87
If you still wish to prefer using access/secret access key .Follow below steps
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Users from the left menu
 3. Click on Create User
 4. Enter the Username & click Next.
 IAM service using 
5. Select Attach policies directly, on next screen for permissions, please choose 'All Types' in the filter and select the listed policies below.
 ReadOnlyAccess
 ViewOnlyAccess
 IAMReadOnlyAccess
 CloudWatchReadOnlyAccess
 88
ComputeOptimizerReadOnlyAccess
 AWSOrganizationsReadOnlyAccess
 6. Click 
Next again & on a final page, give a name to the role & click 
Create user
 7. Once the user is created, please click on the user to create a Secret Key
 8. Go to Security Credentials tab & Click on Create Access Key
 9. Select Application running outside AWS & Click on Next
 89
10. Click on Create access key.
 11. Secret Key will get generated.
 12. Copy the Access Key & Secret Key which will be required in the next step.
 13. Open newly created user
 14. Click on Add permissions → Create inline policy.
 15. Search for Cost Explorer Service
 16. Click on Write → 
StartSavingsPlansPurchaseRecommendationGeneration →
 Next
 90
17. Enter the policy name. 
18. Click on
 Create policy .
 91
AWS Member Account CloudFormation Onboarding (Org)
 You can onboard all member  accounts  using bulk onboarding option once by following below steps 
Step-1 : Login to DigitalEx
 Step-2 : Run Template
 "Here is the link to the CloudFormation template for the organization onboarding."
 Organization CFN Template
 92
Step-1 : Login to DigitalEx
 Below are the steps to log in to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner
 3. Click on Public Clouds under Admin
 93
4. Below Page will be displayed with the list of All linked Member accounts.
 5. You can directly click on +Member Accounts
 6. Click on Cloud Formation
 7. Click on the Login button Page is navigated to the AWS login page where the user needs to enter AWS credentials. After successful login 
into the AWS account, a user should come back to digital to Run Template
 94
Step-2 : Run Template
 Below are the steps to Run the Template.
 1. Click Run Template
 2. On step 2 Select Root if you want to onboard all the org accounts or if you want to onboard individual accounts select the accounts you 
want to onboard 
3. The page is navigated to AWS cloud formation where all the details will be auto generated.
 4. Change the stack name.
 95
4. Check I acknowledge that AWS Cloud Formation might create IAM resources.
 5. Click the Create Stack button and wait till the template running is completed and the status in AWS shows as CREATE_COMPLETE.
 6. Click on the Done button after the template running is successfully completed.
 7. On-boarded Member Account will be displayed on the list of member account
 8. Click the Resource from a Menu option.
 96
9. Resources take up to 2 hours to discover in DigitalEx and will be displayed as shown below.
 97
98
AWS Member Account CloudFormation Onboarding
 Step-1 :Login to DigitalEx
 Step-2 :Run Template
 "Here is the link to the CloudFormation template(CFN) for the member account."
 Member Account CFN Template
 99
Step-1 :Login to DigitalEx
 Below are the steps to log in to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner
 3. Click on Public Clouds under Admin
 100
4. Below Page will be displayed with the list of All linked Member accounts.
 5. Please access the 'Connect' button for the member account you'd like to bring on board.
 6. Click on Cloud Formation
 7. Click on the Login button Page is navigated to the AWS login page where the user needs to enter AWS credentials. After successful login 
into the AWS account, a user should come back to digital to Run Template
 101
Step-2 :Run Template
 Below are the steps to Run the Template.
 1. Click Run Template
 2. The page is navigated to AWS cloud formation where all the details will be auto generated.
 3. Change the stack name.
 4. Check I acknowledge that AWS Cloud Formation might create IAM resources.
 5. Click the Create Stack button and wait till the template running is completed and the status in AWS shows as CREATE_COMPLETE.
 102
6. Click on the Done button after the template running is successfully completed.
 7. On-boarded Member Account will be displayed on the list of member account
 8. Click the Resource from a Menu option.
 103
9. Resources take up to 2 hours to discover in DigitalEx and will be displayed below.
 104
105
AWS Control Tower Usage Account Onboarding
 Note: We Recommend not to onboard master account as usage account
 While Onboarding Usage Account you need to follow the sequence below
 1. Audit
 2. Log Archive
 3. Other remaining accounts
 At the time of onboarding Other remaining usage accounts(point-3), login as respective AWS account rather than login as SSO 
account
 Click on below link to onboard the AWS Control Tower Usage Account   
AWS Member Account Onboarding 
106
Onboarding using terraform
 1. Download & extract the terraform (
 Install | Terraform | HashiCorp Developer )
 2. Go to command prompt /terminal 
3. Enter the below command to check that terraform is installed 
1 terraform -version
 4. Enter the below command to check that AWS CLI is installed if not install(
 Command Line Interface )
 1 aws --version
 Install or update to the latest version of the AWS CLI - AWS 
5. Enter the below command to Configure the AWS
 1 aws configure
 6. Enter the access key & secret access key of the user you wish to onboard the account
 7. Enter the region (e.g:- us-east-1)
 8. Click enter for default output format
 9. If you want you can add AWS profiles to ~/.aws/credentials file and onboard multiple accounts 
9. Enter the below command to clone the repository
 1 git clone https://github.com/cloudwizio/terraform
 10. Open the command prompt /terminal & go to the location where you configured the terraform
 11. Enter the below command to initialize the terraform
 1 chmod +x run-terraform.sh
 12. Navigate to your tenant eg: 
13. Login to DigitalEx 
cloudwiz.io - cloudwiz Resources and Information. 
14. Go to Menu & open API page 
107
15. Copy tenant id & Paste in command prompt /terminal
 16. Copy the JWT & paste the token into the command prompt /terminal
 17. Enter the below command to onboard usage account, paste the TENANT_ID and BEARER_TOKEN copied from the above steps, and 
add aws profile you want to onboard
 1 ./run-terraform.sh <MCX_TENANT_ID> <MCX_BEARER_TOKEN> <AWS_PROFILE> [profile2] [profile3] ...
 18. Usage account will get onboarded successfully.
 108
109
Update AWS Member Account manualy.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Edit Button
 4. Enter new Role ARN
 110
5. Click on Update
 6. AWS Member account will get Updated Successfully.
 111
Update AWS Member Account Using Cloudshel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Edit Button
 4. Click on the login button(AWS CloudShell will get opened)
 Note: Make sure you are logged in to AWS provider account
 112
5. Copy the script
 6. Paste the script into AWS CloudShell & Click Enter
 7. Come back to DigitalEx & click on Done
 8. AWS Member account will get Updated Successfully.
 113
Depreciate
 114
AWS Usage Account Manual Onboarding(Not Recommended/Depreciated)
 Below are the steps to Onboard Usage Account manually.
 Step-1:Enable Compute Optimizer.
 Step-2: Enable AWS Config & Setup SNS (Per Region)
 Step-3: Create an IAM role for DigitalEx.
 Step 4: Retrieve AWS Account Id.
 Step-5: Create Usage Account in DigitalEx.
 115
Step-1:Enable Compute Optimizer.
 This step should be carried out for every individual member account.
 1. Login to your AWS Member account as Administrator 
2. Then search for AWS Compute Optimizer in a search bar & select it. You will land on the home page of Compute Optimizer Service 
3. Click on Get started 
116
117
Step-3: Create an IAM role for DigitalEx.
 This step only provides illustrations on creating a role but a user with access/secret key is also supported. If you wish to create a 
user, please assign similar permissions as documented for a role below. We encourage a use of a Role over a User as its more 
secure.
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Roles from the left menu, and click 
IAM service using 
Create role . One the create role screen please select the 
configuration as follows,
 a. Trusted entity type: AWS Account
 b. An AWS account: Choose 
Another AWS account and fill in the account number as 
911403356698
 Retrieve the Tenant Id
 c. External ID: In this field, please put the Tenant ID for your DigitalEx account. To get the tenant id follow instructions outlined in this 
page 
d. Finally click 
Next
 118
e. Click 
Next , on next screen for permissions, please select the aws managed policy called 
ReadOnlyAccess
 119
f. Click 
Next again & on a final page, give a name to the role & click 
Create role
 g. Once the role is created, please note the ARN of a role, which will be required in the next step.
 120
Step 4: Retrieve AWS Account Id.
 Below are the steps to Retrieve AWS Account Id:
 1. Go to the My Account page
 2. On the My Account page, note the Account Id
 121
Step-5: Create Usage Account in DigitalEx.
 Below are the steps to Create a Usage Account in DigitalEx:
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 4. Below Page will be displayed with the list of All linked Member accounts. 
122
5. Click on 
Connect , and switch to 
Manual tab, and fill up the details as follows,
 a. Role ARN: Fill in the Role ARN captured in last step. Please note if you have chose to create a user instead of a role, check the box 
named Use access / secret keys and fill in related details.
 b. Bucket Name: this parameter takes a list of buckets you used to setup your AWS Config regional service. This can very well be also 
just one bucket in case you used same bucket for all the region.
 c. To get the Account id follow instructions outlined in this page 
Step 4: Retrieve AWS Account Id. 
6. After filling in all the details, click 
Connect your account should get onboarded successfully.
 The values depicted in the images are merely provided as sample values for the purpose of illustration, and they may vary in your 
specific situation.
 123
7. On-boarded Member Account will be displayed on the list of member account
 8. Click the Resource from the Menu option.
 124
9. A Resource takes up to 2hrs to discover in DigitalEx and will be displayed as shown below.
 125
126
AWS Usage Account Cloud Formation(Not Recommended/Depreciated)
 Cloud Formation Usage Account onboarding has different steps.
 Onboard Usage Account using Cloud Formation
 127
Onboard Usage Account using Cloud Formation
 Below are the steps to Onboard Usage Account using Cloud Formation
 Step -1 : Login to DigitalEx
 Step -2 : Select regions
 Step -3 : Run Template
 128
Step -1 : Login to DigitalEx
 Below are the steps to log in to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 129
4. Below Page will be displayed with the list of All linked Member accounts.
 5. Click on the Connect button of a specific member account/ You can directly click on +Member Account
 6. Click on Cloud Formation 
7. Click on the Login button Page is navigated to the AWS login page where the user needs to enter AWS credentials. After successful login 
into the AWS account, a user should come back to digital to Run Template
 130
131
Step -2 : Select regions
 To select All-Regions, Check the All-Region Check box(By default it is selected)
 Steps to Select Multi-region/Single Region:
 1. Uncheck the All-Region Check box 
2. Click on the Region dropdown
 3. Select the region(s) you wish to discover the assets
 Note:
 Non Control Tower Accounts
 If you select all, all active regions will be configured
 If you select specific regions, then out of those specific regions only active regions will be configured
 Control Tower Accounts
 If you select all, only control tower governed regions will be configured
 If you select specific, then out of those specific regions only control tower governed regions will be configured
 132
Step -3 : Run Template
 Below are the steps to Run the Template
 1. Click Run Template 
2. The page is navigated to AWS cloud formation where all the details will be auto-generated
 3. Change the stack name if you have an on-boarded region(s) earlier and are now onboarding more regions
 133
4. Check I acknowledge that AWS Cloud Formation might create IAM resources
 5. Click the Create Stack button and wait till the template running is completed and the status in AWS shows as CREATE_COMPLETE.
 6. Click on the Done button after the template running is successfully completed.
 7. On-boarded Member Account will be displayed on the list of member account 
8. Click the Resource from a Menu option. 
134
9 Resources take up to 2 hours to discover in DigitalEx and will be displayed as shown below.
 135
136
Delete AWS Member Account Prerequisites
 Below are the steps that needs to be performed before deleting the Usage Account :
 Delete Cloud Formation Stack From AWS
 Delete SNS Subscriptions From AWS
 137
Delete Cloud Formation Stack From AWS
 Below are the steps to delete cloud formation stack from AWS:
 1. Select the region you have used to onboard Cloudformation stack for usage account 
2. Go to Cloudformation from the Services tab
 3. On the  Cloudformation Dashboard page, click on the Stacks from the left menu
 4. Select the stack you used to onboard usage account and click on the delete button on the top
 5. Confirm the deletion by clicking on Delete Stack button shown in the box
 6. You will see the notification of successful deletion
 Below is the description of the steps to delete stack from AWS:
 1. Select the region you have used to onboard Cloudformation stack for usage account 
2. Go to Cloudformation from the Services tab
 3. On the  CloudFormation Dashboard page, click on the Stacks from the left menu
 138
4. Select the stack you used to onboard usage account and click on delete button on the top
 5. Confirm the deletion by clicking on Delete Stack button shown in the box
 139
6. You will see the notification of successful deletion
 140
Delete SNS Subscriptions From AWS
 Below are the steps to delete Subscriptions from AWS:
 1. Select a Region to delete the SNS service
 2. Go to SNS from the Services tab
 3. On the SNS Dashboard page, click on the Subscriptions link from the left menu
 4. Select the particular webhook you used to onboard the usage account to delete and click on the Delete Button on the top
 5. Confirm the deletion by Clicking Delete Button in the box
 6. You will see the status message of the SNS you deleted
 Note : Similarly you can go to each region and  delete the webhook 
Below is the description of the steps to delete Webhook from AWS:
 1. Select a Region to delete the SNS service
 2. Go to SNS from the Services tab
 3. On the SNS Dashboard page, click on the Subscriptions link from the left menu
 141
4. Select the particular webhook you used to onboard the usage account to delete and click on the Delete Button on the top
 5. Confirm the deletion by Clicking Delete Button in the box
 142
6 . You will see the status message of the SNS you deleted
 Note : Similarly you can go to each region and  delete the webhook 
143
Delete AWS Biling Account Prerequisites
 To delete Billing Account we need to delete the Stack from AWS 
Below are the steps to delete stack from AWS:
 1. Select the region you have used to onboard Cloudformation stack for billing account
 2. Go to Cloudformation from the Services tab
 3. On the Cloudformation Dashboard page, click on the Stacks from the left menu
 4. Select the stack you used to onboard billing account and click on the delete button on the top
 5. Confirm the deletion by clicking on Delete Stack button shown in the box
 6. You will see the notification of successful deletion
 Below is the description of the steps to delete stack from AWS:
 1. Select the region you have used to onboard Cloudformation stack for billing account 
2. Go to Cloudformation from the Services tab 
3. On the Cloudformation Dashboard page, click on the Stacks from the left menu
 144
4. Select the stack you used to onboard billing account and click on the delete button on the top
 5. Confirm the deletion by clicking on Delete Stack button shown in the box
 145
6. You will see the notification of successful deletion
 146
AWS Account Onboarding Questionnaire
 To ensure a smooth and comprehensive onboarding experience, it's crucial that the DigitalEx team is prepared and informed. This 
questionnaire aims to understand your needs and expectations better, thereby ensuring an efficient and enriched onboarding process.
 Q1: What is your monthly spend on AWS?
 Understanding your monthly spending will help us provide better cost management and optimization strategies.
 Q2: Is AWS Cost and Usage Reports (AWS CUR) enabled for your account?
 If AWS CUR is already enabled, DigitalEx can ingest historical cost data. If not, we can obtain up to 12 month's worth of historical cost data 
through Cost Explorer APIs.
 The mentioned feature specifically focuses on cost-related information and certain attributes/features may not function as expected with 
AWS CUR (Cost and Usage Report) since it does not include tag information. Some features might be impacted like perspective and 
resources
 Reference: AWS CUR Guide
 Q3: Is the AWS Cost and Usage Report (AWS CUR) configured to use hourly or daily granularity?
 While hourly granularity provides more detailed data, it generates significantly more data than daily granularity. We prefer using daily 
granularity, but our CloudFormation template can adapt to the existing granularity level for historical cost data.
 Q4: How many linked accounts do you have?
 To continuously discover resources and collect key metrics for insight and optimization, it is necessary to onboard each linked account 
individually.
 Q5: In what currency is your invoice generated?
 This information will help us better understand your billing structure.
 Q6: Do you have billing accounts using multiple currencies?
 DigitalEx supports multiple currencies which is configurable from DigitalEX UI
 Q7: Is your AWS account configured to use AWS Control Tower?
 Our CloudFormation is designed to automatically detect and onboard the relevant accounts if AWS Control Tower is in use.
 Reference: AWS Control Tower
 Q8: Did you purchase AWS resources directly from AWS or through a CSP/reseller?
 If resources were purchased through a CSP/reseller, the billing account onboarding CloudFormation must be executed on the payer/master 
AWS account, and access to this account will be necessary.
 We appreciate your cooperation in providing this information. It will significantly enhance the onboarding process, ensuring we can provide 
the best possible service.
 147
AWS Account Onboarding Security FAQs
 As part of our commitment to a smooth and secure onboarding process, we've prepared the following FAQs to help address any queries you 
might have about AWS account onboarding with DigitalEx. 
Q1: What is the process for onboarding an AWS account with DigitalEx?
 In AWS, there are two main types of accounts:
 Management Account (Payer/Master account)
 Member Account
 In DigitalEx, the Management Account is onboarded as a billing account and Member Accounts as usage accounts. These can be 
onboarded either using AWS CloudFormation templates or manually with a step-by-step guide.
 Q2: What is a billing account and why does DigitalEx need it?
 In DigitalEx, a "billing account" refers to the AWS Management Account. It provides access to cost data, allowing the DigitalEx platform to 
perform analysis, waste identification, budget management, and mre. 
Q3: What is a usage account and why does DigitalEx need it?
 A "usage account," a term used by DigitalEx, refers to AWS Member Accounts. We recommend onboarding all of them as usage accounts in 
DigitalEx. This allows real-time resource inventory across all your accounts, cost analysis of resources over time, identification of unused 
resources, and more.
 Q4: How do I access the guide for onboarding my billing account?
 The guide for onboarding your billing account is available at this link: AWS Billing Account Onboarding Guide
 Q5: How do I access the guide for onboarding my usage account?
 The guide for onboarding your usage account can be found at this link: AWS Usage Account Onboarding Guide 
Q6: Is it secure to onboard my AWS account with DigitalEx? If so, why?
 Yes, DigitalEx has implemented strict measures to ensure the security of your account and data. We use role-based access for AWS 
accounts, secured by a trust relationship between DigitalEx and the client's AWS account. The secret keys generated in this way are 
temporary and cannot be reused. DigitalEx only has read access to the S3 bucket storing AWS CUR reports and AWS Config snapshots, 
and CloudWatch metrics.
 Q7: How does billing account onboarding using AWS CloudFormation work?
 We've created a one-click onboarding automation to streamline the process and eliminate potential errors. During execution, we check for 
existing AWS Cost and Usage Reports (AWS CUR) and create one if not available. We also set up an IAM role granting DigitalEx read-only 
access to the CUR reports stored in the bucket. You can check out the template here.
 148
Q8: How does usage account onboarding using AWS CloudFormation work?
 Our one-click onboarding automation simplifies the process. If AWS Control Tower is set up, we utilize its configuration to retrieve AWS 
Config snapshots. If not, we set up the AWS Config service and an SNS topic for resource snapshots and real-time updates. Finally, we set 
up an IAM role granting DigitalEx read-only access to the bucket storing AWS Config snapshots. You can check out the template here.
 Your cooperation with these guidelines will significantly enhance the onboarding process, ensuring we can provide the best possible service.
 149
AWS Troubleshooting
 The following are the steps you should take if you're seeing a warning message on the public clouds page. 
Click on Edit of the billing/member account which shows warning.
 Copy the command
 Login to your AWS account where billing is configured.
 Open the cloudshell
 Run the command  wait for 5mnts till Cloud formation template gets updated
 Click Done from DigitalEx UI & Run the Data ingestion
 150
IAM permissions missing
 We are requesting IAM permissions to verify whether the provided Role ARN or credentials possess the necessary policies for successful 
data ingestion. The specific permissions needed are:
 iam:ListUserPolicies : To enumerate policies linked to the user's access key and secret
 iam:ListAttachedUserPolicies : To identify policies attached to the user
 iam:ListRolePolicies : To enumerate policies linked to the Role ARN
 iam:ListAttachedRolePolicies : To identify policies attached to the Role ARN
 Compute Optimizer Permission missing
 We are requesting Compute Optimizer to generate native recommendations
 Below are the actions you should take when you encounter the following error message.
 When you encounter this error message, it indicates that you've already onboarded an account with this Account 
ID.
 151
If you encounter this error message, it means that you've partially entered an incorrect Account ID.
 152
153
When you come across this error message, it indicates that you've entered the invalid Account ID.
 154
155
When encountering this error message, verify that you have correctly entered the Access key.
 156
157
When encountering this error message, verify that you have correctly entered the Secret key.
 158
159
If you come across this error message, consider double-checking the Bucket Name
 160
161
If you encounter this error message, please input the accurate Role ARN.
 162

AZURE STEPS -
Azure
 DigitalEx enables users to onboard their Azure billing account. This process involves setting up the necessary accounts and permissions, 
configuring the billing and cost management settings, and integrating the billing data with DigitalEx. Onboarding the Azure billing account 
with DigitalEx allows users to track and manage their Azure costs and usage, and to optimize their use of Azure resources to reduce costs. 
It is important to carefully follow the steps in the onboarding process to ensure that the Azure billing account is set up correctly and able to 
accurately track and report on costs.
 Billing Account
 The billing accounts feature in DigitalEx allows users to view the cost of resources from their Azure accounts and regions in a single 
interface. With this feature, users can search and view the cost of resources across all regions and all accounts, and see where resources 
are located. The cost dashboard provides a snapshot of costs, enabling users to quickly understand overall trends and gain visibility into 
their spending across all their public and private cloud providers. This feature can be helpful for organizations looking to optimize their Azure 
usage and reduce costs.
 DigitalEx supports three different types of accounts:
 1. Customer Agreement billing account: This billing account is managed by the organization itself, and the billing ID is used in the billing 
level scope for onboarding.
 2. Partner Agreement billing account: This billing account is managed by a third-party seller and the end user has subscription level access. 
Users can onboard both the billing and subscription levels.
 3. Direct Enterprise Agreement customers: This account is similar to a direct Customer Agreement billing account.
 These different account types allow DigitalEx to support a variety of billing and payment arrangements, and to provide users with the tools 
and features they need to manage their cloud resources and costs effectively.
 Usage Account
 A usage account in an Azure organization is a subscription account, which is any account that is not the management account. Policies can 
be attached to a usage account to apply controls specifically to that account. It is important to properly set up and manage subscription 
accounts in an Azure organization to ensure that resources are used effectively and in accordance with organizational policies and controls.
 164
Azure Biling Account Onboarding
 There are two ways to onboard the Billing Account
 1. Manual UI Onboarding
 Azure Billing Account Manual UI Onboarding 
2. Manual CLI Onboarding
 Azure Billing Account Manual CLI Onboarding 
3. Cloud Shell Based Onboarding (Automated)
 Azure Billing Account Cloud Shell 
165
Azure Biling Account Manual UI Onboarding
 Account Type: MCA, MPA, CSP
 Account Type: Enterprise Account(EA)
 166
Account Type: MCA, MPA, CSP
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps.
 Step-1: Create Azure Active Directory app
 Step-2: Assign permissions to the app
 Step-3: Retrieve Account ID
 Step-4: Connect Billing Account
 167
Step-1: Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 168
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 169
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 170
Step-2: Assign permissions to the app
 In this step, we will assign the Billing Account Reader permission to the app created in Step 1. This role grants read access to account 
information and cost reports. It’s important to note that the Billing Account Reader role DOES NOT provide any WRITE permissions to 
DigitalEx platform.
 Procedure in this step is also documented by Azure here : assign-roles-azure-service-principals.
 If you choose to onboard the billing scope you must add the Billing Account Reader role
 If you choose to onboard the subscription scope, you must add the Cost Management Reader role
 1. Click on Menu 
2. Go to Cost Management + Billing
 3. Click on Access Control(IAM)
 4. Click on Add (Add role assignment page will get opened )
 5. Select the Billing account reader(Select based on your scope mentioned in the above note)
 6. Search the App created in Step 1
 7. Click on Add Button
 171
172
Step-3: Retrieve Account ID
 Steps to Retrieve Account ID:
 1. Click on Menu
 2. Click on Cost Management + Billing.
 3. Click on Properties
 4. Copy the Account ID
 Steps to Retrieve Tenant ID:
 1. Click on Menu
 2. Go to Azure Active directory.
 173
3. Click on App Registration
 4. Click on your application
 174
5. Copy the Application Client id & Tenant id 
6. Client Secret is already copied in 
Step-1: Create Azure Active Directory app 
Make sure to record all of the details that are retrieved, as they will be needed for the manual creation of a billing account.
 175
Step-4: Connect Biling Account
 If you set up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply select the 
"Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 176
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type (To know your Acc type follow this link 
ent )
 4. Select the Account Scope 
View your billing accounts in Azure portal - Microsoft Cost Managem
 Using subscription scope is not recommended as it provides limited features and cost savings opportunities.
 5. Fill in the following details captured in Step 1
 Billing Account ID
 Tenant ID
 Client ID
 Client Secret
 6. Click Connect 
177
5. The onboarded Enrollment Account will be displayed with the list of All linked Subscription accounts.
 6. Click Data Ingestion to skip waiting  
178
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 7. Go to the Menu option and Click Cost.
 8. Data will display immediately after successful ingestion.
 179
180
Account Type: Enterprise Account(EA)
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps.
 Scope: Billing Account
 Scope: Department
 181
Scope: Biling Account
 Step- 1: Create Azure Active Directory app
 Step- 2: Assign permissions to the app
 Step - 3: Connect Billing Account
 182
Step- 1: Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 183
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 184
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 185
Step- 2: Assign permissions to the app
 In this step, we will assign the EnrollmentReader permission to the app created in Step 1. This role grants read access to account 
information and cost reports. It’s important to note that the EnrollmentReader role DOES NOT provide any WRITE permissions to 
DigitalEx platform.
 Procedure in this step is also documented by Azure here : assign-roles-azure-service-principals.
 1. Unlike other billing account types, Azure does not allow role assignment of Enterprise Agreement (EA) accounts using the user 
interface. Instead, we’ll use the official Azure HTTP API to achieve this.
 2. Before hitting the API, lets capture few details we would need to pass to the API
 a. billingAccountName : This is simply an ID of your billing account you can capture from Cost Management + Billing > Overview 
page
 b. billingRoleAssignmentName : This parameter is a unique GUID that you need to provide. You can          
website to generate a unique GUID. 
use the GUID Generator 
c. Principal ID : This is Enterprise App’s Object ID. For this, navigate to Microsoft Entra ID > Enterprise applications and look for the 
app we created in step 1 and capture it’s Object ID
 186
3. We’re now ready to hit an API to make role assignment. Open following URL on the same browser window where you have Azure portal 
open : Role Assignments and click Try It and select correct directory if it asks. Fill in the parameters billingAccountName and 
billingRoleAssignmentName with the values captured in last step. And in the body section put following JSON,
 1 {
 2  
3    
4    
5    
6  
7 }
 "properties": {
 "principalId": "<principal_id>",
 "principalTenantId": "<tenant_id>",
 }
 "roleDefinitionId": "/providers/Microsoft.Billing/billingAccounts/<billing-account
id>/billingRoleDefinitions/24f8edb6-1668-4659-b5e2-40bb5f3a7d7e"
 4. Make sure to replace 
<principal_id>" and 
<tenant_id> and 
<billing-account-id> with correct values captured in earlier steps. 
roleDefinitionId is an ID for and EnrollmentReader role as documented here : permissions-that-can-be-assigned-to-the-service-principal
 After filling in all the parameters and body, click Run. API call should return 200 OK. if it doesn’t, do not proceed.
 187
Step - 3: Connect Biling Account
 If you are setting up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply 
select the "Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 188
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type as EA
 4. Select the Account Scope as Billing Account
 5. Fill in the following details capture in Step 1 and Step 2
 Billing Account ID
 Tenant ID 
Client ID 
Client Secret 
6. Click Connect 
189
7. The onboarded Account will be displayed with the list of All linked Subscription accounts.
 8. Click Data Ingestion to skip waiting  
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 9. Go to the Menu option and Click Cost.
 190
10. Data will display immediately after successful ingestion.
 191
192
Scope: Department
 Step- 1 : Create Azure Active Directory app
 Step - 2 : Assign permissions to the app
 Step - 3 : Connect Billing Account
 193
Step- 1 : Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 194
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 195
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 196
Step - 2 : Assign permissions to the app
 In this step, we will assign the DepartmentReader permission to the app created in Step 1. This role grants read access to department 
information and cost reports at department scope. It’s important to note that the DepartmentReader role DOES NOT provide any WRITE 
permissions to DigitalEx platform.
 Procedure in this step is also documented by Azure here : #assign-the-department-reader-role-to-the-service-principal
 1. Unlike other billing account types, Azure does not allow role assignment of Enterprise Agreement (EA) accounts using the user 
interface. Instead, we’ll use the official Azure HTTP API to achieve this.
 2. Before hitting the API, lets capture few details we would need to pass to the API
 a. billingAccountName : This is simply an ID of your billing account you can capture from Cost Management + Billing > Properties.
 b. departpartName : This is simply an ID of your department account you can capture from Cost       
Management + Billing > 
Overview
 c. billingRoleAssignmentName : This parameter is a unique GUID that you need to provide. You can          
website to generate a unique GUID.
 use the GUID Generator 
d. Principal ID : This is Enterprise App’s Object ID. For this, navigate to Microsoft Entra ID > Enterprise applications and look for the 
app we created in step 1 and capture it’s Object ID
 3. We’re now ready to hit an API to make role assignment. Open following URL on the same browser window where you have Azure portal 
open : Enrollment Department Role Assignments - Put and click Try It and select correct directory if it asks. Fill in the parameters, 
billingAccountName, departmentName and billingRoleAssignmentName with the values captured in last step. And in the body section 
put following JSON,
 1 {
 2  
3    
4    
5    
6  
7 }
 "properties": {
 "principalId": "<principal_id>",
 "principalTenantId": "<tenant_id>",
 }
 "roleDefinitionId": 
/providers/Microsoft.Billing/billingAccounts/<BILLING_ACCOUNT_ID>/departments/<DEPARTMENT_ID>/billingRoleDefini
 tions/db609904-a47f-4794-9be8-9bd86fbffd8a
 197
4. Make sure to replace 
<tenant_id> and 
<principal_id> and 
<BILLING_ACCOUNT_ID> and 
<DEPARTMENT_ID> with correct values 
captured in earlier steps. roleDefinitionId is an ID for DepartmentReader role as documented here : permissions-that-can-be-assigned
to-the-service-principal. After filling in all the parameters and body, click Run. API call should return 200 OK. if it doesn’t, do not proceed.
 198
Step - 3 : Connect Biling Account
 If you are setting up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply 
select the "Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 199
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type as ES
 4. Select the Account Scope as Department
 5. Fill in the following details captured in Step 1 and Step 2
 Department Id
 Tenant ID 
Client ID 
Client Secret 
200
6. Click Connect 
7. The onboarded Account will be displayed with the list of All linked Subscription accounts.
 8. Click Data Ingestion to skip waiting  
201
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 9. Go to the Menu option and Click Cost.
 202
10. Data will display immediately after successful ingestion.
 203
204
Azure Biling Account Manual CLI Onboarding
 The steps below need to be executed in the Azure Cloud Shell. Please log in to the Azure portal and launch the 
Cloud Shell from the navigation bar.
 To create Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can have both the 
Contributor and User Access Administrator roles.
 Step-1:  Create AD Application
 Execute the following command to create AD App
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME> : AD app name of your choice
 After executing the command, capture the App id, Password(secret) & Tenant.
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Step-2:  Assign permission to the app
 If you are onboarding billing scope as billing, Follow the below steps for assigning permission to the app   
a. Login to Azure console > Click on Menu > Cost Management + Billing > Access Control (IAM)
 b. Click Add > Select the Billing account reader > Enter the app created in Step-1 above. 
Follow this link to get detailed steps  
Step-2: Assign permissions to the app  
If you are onboarding subscription scope as billing. Execute the following command to assign permission to the app.
 1 az role assignment create --assignee "<APP_ID>" --role "Cost Management Reader" --scope 
/subscriptions/<SUBSCRIPTION_ID>
 <APP-ID> : AD app id captured in Step-1
 <SUBSCRIPTION_ID> : Your subscription id you wish to onboard
 Step-3: Retrieve Account ID
 Follow the steps to get the account id 
Step-3: Retrieve Account ID 
Step-4: Submit Details in DigitalEx
 Get the details Tenant ID, Client ID, Client Secret, Account ID.
 Follow the below steps to onboard the billing account in DigitalEx.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link Azure Connect Billing Account for Partner to onboard additional providers
 205
1. Click on Azure Provider
 2. Click on Connect manually
 206
3. Click on Connect Billing Account
 4. Enter the details which you have captured above.
 5. Click on connect & done.
 If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1. Navigate to Menu > Admin > Public Clouds > +Account.
 207
2. Click on Azure Provider & Click on Manual tab
 3. Enter the details which you have captured above.
 208
4. Click Connect
 5. The onboarded Billing Account will be displayed with the list of All linked Subscription accounts.
 209
After adding a new account, it may take up to 30 minutes for the system to discover and process the data.
 6. Go to the Menu option and Click Cost.
 7. Data will display immediately after successful ingestion.
 210
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
211
Azure Biling Account Cloud Shel
 Cloud Shell Billing Account onboarding has different steps.
 Step-1: Login to Azure account
 Step-2: Execute the script from the Azure Cloud Shell.
 212
Step-1: Login to Azure account
 To onboard Azure through the CLI, it is necessary to have the Owner role assigned.
 Below are the steps that need to be performed if the user registers for the first time, the below page is displayed.
 1. Click on the Login button and Login into Azure
 2. The page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx
 3. It will ask to select the environment (Select as per your choice)
 4. Copy the script.
 5. Paste in Cloud Shell Editor & Click Enter
 6. It will ask to select account type, select & click enter.
 7. Enter 'y' to confirm account. 
213
Ignore Bad request syntax or unsupported method retrying messages.
 8. Click on Done 
9. Click Skip waiting or wait for 24hrs to display the data.
 Below are the steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner
 3. Click on Admin > Cloud Providers 
4. Click on +Account
 5. Select Azure Provider
 6. Click on Cloud Shell
 7. Click on Log In 
214
The page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 Below are the description of steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3.  Click on Admin > Public Clouds
 4. Click on +Account
 5. Select Azure Provider 
6. Click on Cloud Shell 
215
7. Click on the Login button as shown in the above image
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 216
Step-2: Execute the script from the Azure Cloud Shel.
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step. 
2. It will ask to select the environment (Select as per your choice) 
3. Paste in Cloud Shell Editor and click Enter
 To onboard a subscription as a billing account, append the command with --sub as a suffix.
 217
4. It will ask for the account type, select & click enter. (Follow this link to know your account type 
l - Microsoft Cost Management )
 5. Enter 'y' to confirm account & subscription 
6. Script will run automatically
 View your billing accounts in Azure porta
 Ignore Bad request syntax or unsupported method retrying messages.
 7. Click on the Done button in DigitalEx , after the script running is successfully completed. 
218
8. Click Data Ingestion to skip waiting so that data is displayed immediately
 9. You will see the ingestion in progress 
10. The onboarded Enrollment Account will be displayed with the list of All linked Subscription accounts.
 219
11. Go to the Menu option and Click Cost to view the cost data. 
12. Data will display immediately after successful ingestion.
 220
221
Azure Management Group onboarding as biling
 You can onboard azure management group as billing by following the CLI steps provided below.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Create AAD
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: Enter the unique name. Recommended (digitalex_management_group)
 Capture App id and share it with Owner required to Assign Permissions to the App 
Capture Password (Secret) and Tenant id required to Connect Billing Account
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope 
"/providers/Microsoft.Management/managementGroups/<MANAGEMENT_GROUP-ID>" -o table
 <APP_ID> : Enter App id created in above step
 <MANAGEMENT_GROUP-ID>: Enter your management group Id(To Get Management Group id Navigate to Azure Console > Search 
Management Group > Capture tenant group id)
 Connect Billing Account
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds
 3. Click on +Account 
4. Select CSP as Account type and Billing Scope as Management group
 5. Enter required details 
6. Click Connect
 You can use the same credentials to onboard the Management Group as a usage account.
 LI Onboarding 
Azure Management Group Manual C
 222
Update Azure Enrolment / Contract Manualy.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Azure tab 
4. Click on the Edit Button 
5. Click on Manual tab
 6. Update the details 
223
7. Click on Update
 8. Azure Enrollment / Contract will get Updated Successfully.
 224
Update Azure Enrolment / Contract using Cloud Shel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure tab 
4. Click on the Edit Button
 5. Click on the login button(Azure CloudShell will get opened) 
Note: Make sure you are logged in to Azure provider account
 225
6. Copy the script
 7. Paste the script into Azure CloudShell & Click Enter
 8. Come back to DigitalEx & click on Done
 9. Azure Enrollment / Contract will get Updated Successfully.
 226
Azure Subscriptions Onboarding
 There are two ways to onboard the Subscriptions
 1. Manual Onboarding
 Azure Subscription Account Manual Onboarding 
2. Cloud Shell Based Onboarding (Automated)
 Azure Subscriptions Account Cloudshell Onboarding 
227
Management Groups
 Integrating subscriptions into DigitalEx grants access to valuable resources, metrics, and recommendations, optimizing cloud costs. Receive 
tailored recommendations for rightsizing, orphan, idle resources to optimize costs while maintaining performance. 
You can onboard subscriptions either of the way
 Azure Management Group Manual CLI Onboarding
 Azure Management Group Cloudshell Onboarding
 228
Azure Management Group Manual CLI Onboarding
 Azure Management Group CLI Onboarding 
You can onboard all subscriptions as a group by following the CLI steps provided below 
If you have already set up the Management Group for billing using the steps provided here 
Azure Management Group on
 boarding as billing  you can utilize the same credentials to onboard the Management Group again.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Create AAD
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: Enter the unique name. Recommended (digitalex_management_group)
 Capture App id and share it with Owner required to Assign Permissions to the App
 Capture Password (Secret) and Tenant id required to Connect Management Group 
To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope 
"/providers/Microsoft.Management/managementGroups/<MANAGEMENT_GROUP-ID>" -o table
 <APP_ID> : Enter App id created in above step
 <MANAGEMENT_GROUP-ID>: Enter your management group Id(To Get Management Group id Navigate to Azure Console > Search 
Management Group > Capture tenant group id)
 Connect Management Group
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds
 3. Click on +Management Groups & Enter required details
 4. Click Connect.
 229
Azure Management Group Cloudshel Onboarding
 Cloud Shell Management Group onboarding has different steps.
 Step-1: Login to Azure Cloud Shell
 Step-2 : Execute the Script
 230
Step-1: Login to Azure Cloud Shel
 User should be Log In as Billing Admin or Project admin.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner.
 3. Click on Public Clouds under Admin
 231
4. Below Page will be displayed with Management Group
 5. Click on Connect button of the Management Group
 232
6. Click on the Login button as shown in the above image.
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 233
Step-2 : Execute the Script
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 234
3. Script will run automatically.
 Ignore Bad request syntax or unsupported method retrying messages.
 4. Click on the Done button in DigitalEx, after the script running is successfully completed.
 235
5. On-boarded Management Group will be displayed with Active Status. It takes up to 2 hours to discover the data.
 6. Click the Resource from the Menu option.
 236
7. Click on Resources (All the resource data will be displayed) 
237
238
Individual Subscriptions
 Integrating subscriptions into DigitalEx grants access to valuable resources, metrics, and recommendations, optimizing cloud costs. Receive 
tailored recommendations for rightsizing, orphan, idle resources to optimize costs while maintaining performance.
 You can onboard subscriptions either of the way
 Azure Subscription Account Manual Onboarding 
Azure Subscriptions Account Cloudshell Onboarding 
239
Azure Subscription Account Manual Onboarding
 Manual Subscription onboarding can be done either through the Azure UI portal by following the steps below, or by using Azure CLI 
commands
 If you wish to onboard through Azure Manual UI folow below steps
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps
 Step-1 : Create Azure Active Directory app
 Step-2: Assign Permissions to an app
 Step-3: Connect Usage Account
 If you wish to onboard through Azure Manual CLI folow below steps
 The steps below need to be executed in the Azure Cloud Shell. Please log in to the Azure portal and launch the 
Cloud Shell from the navigation bar
 To manage an Azure Active Directory (AAD) app and to assign a role, the owner role is required.
 1. Login to Microsoft Azure Cloud Shell and execute the below command.
 1 az ad sp create-for-rbac -n <APP_NAME> --role Reader --scopes "/subscriptions/<SUBSCRIPTION_ID>"
 <APP_NAME> : App name of your choice
 <SUBSCRIPTION_ID> : Your azure subscription id, follow this link to get subscription id. 
al - Azure portal 
Get subscription and tenant IDs in the Azure port
 The above command will create an <APP_NAME> of your choice and assign the Reader role for the <SUBSCRIPTION_ID> subscription 
that you want to onboard as a usage account in DigitalEx.
 2. Go to the DigitalEx portal and follow this steps Connect Subscription and enter the credentials obtained in the previous cloud shell 
output. 
IF U DONT HAVE OWNER ROLE TO EXECUTE ABOVE COMMAND FOLLOW BELOW STEPS
 Create AAD & Secret
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required.
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: AD app name of your choice
 Capture App id and share it with Owner required to Assign Permissions to the App
 Capture App Id, Password(Secret) and Tenant id and share it with the partner company required to Connect Management Group
 240
To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope "/subscriptions/<SUBSCRIPTION_ID>" -o 
table
 <APP_ID> : Enter App id
 <SUBSCRIPTION_ID> : Enter your subscription id
 Connect Subscription
 1. Login to DigitalEx as Owner
 2. Go to Menu > Admin > Public Clouds
 3. Click on Connect for the subscription under subscriptions tab of Azure & Enter required details
 4. Click Connect.
 241
Step-1 : Create Azure Active Directory app
 Steps to Create an Application
 1. Click on Menu
 2. Go to Azure Active directory
 3. Click on App Registration 
242
4. Click on New Registration 
5. Enter Name of Application
 6. Supported account type is selected automatically.
 7. Click on Register
 243
8. App will get created as shown below.
 9. Copy Application Client id & Tenant id
 Steps to add client secret
 1. Click on Certificates & Secrets
 244
2. Click on New Client Secret 
3. Enter Description
 4. Select Expires as 24 months maximum
 5. Click Add
 6. Applied client secret will be displayed as shown below
 245
7.Copy the Value(not Secret ID) which is used later for manual creation of usage account .
 246
Step-2: Assign Permissions to an app
 In order to grant permissions to an app, the owner role is required.
 1. Click on Subscriptions
 2. Click on your subscription
 3. Click on Access Control (IAM)
 4. Click on Add → Add role assignment
 247
5. Click on the search box & enter the role name as Reader role
 6. Select the role & click next 
7. Click on Select Members
 248
8. Enter the App name (which you have created in 
Step-1 : Create Azure Active Directory app ) & Click Select
 9. Click Next 
249
10. Click Review + assign
 250
Step-3: Connect Usage Account
 Below are the steps to connect azure usage account:
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds 
3. Below Page will be displayed with the list of All linked Subscription accounts.
 4. Click on Connect button of the specific subscription account / You can directly click on +Subscription
 251
5. Click on Manual
 6. Fill in the following details. 
Active Directory (Tenant) ID 
Application (Client) ID 
Step-1 : Create Azure Active Directory app 
Step-1 : Create Azure Active Directory app 
Application (Client) Secret 
7. Click Connect
 Step-1 : Create Azure Active Directory app 
8. On-boarded Subscription accounts will be displayed on the list of a member accounts. It takes up to 2 hours to discover the data.
 9. Click the Resource from the Menu option.
 252
10. Resources will get discovered in DigitalEx
 253
254
Azure Subscriptions Account Cloudshel Onboarding
 Step-1 :Login to Azure Cloud Shell
 Step-2 :Execute the Script
 255
Step-1 :Login to Azure Cloud Shel
 User should be Log In as Billing Admin or Project admin.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner.
 3. Click on Public Clouds under Admin
 256
4. Below Page will be displayed with the list of All linked Member accounts.
 5. Click on Connect button of the specific subscription account/ You can directly click on +Subscription
 257
6. Click on the Login button as shown in the above image
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 258
Step-2 :Execute the Script
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 3. Script will run automatically.
 259
Ignore Bad request syntax or unsupported method retrying messages.
 4. Click on the Done button in DigitalEx, after the script running is successfully completed.
 5.  On-boarded Subscription accounts will be displayed on the list of a member accounts. It takes up to 2 hours to discover the data.
 260
6. Click the Resource from the Menu option.
 7. Click on Resources (All the resource data will be displayed) 
261
262
Update Azure Subscription Manualy
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure
 4. Go to Subscriptions
 5. Click on Edit Subscription Account
 6. Click on Manual
 7. Update the Details
 8. Click on Update
 263
8. Azure Subscription will get Updated Successfully.
 264
Update Azure Subscription using Cloud Shel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure
 4. Go to Subscriptions
 5. Click on the Edit button which the Subscription Account you want to update
 5. Click on the login button(Azure CloudShell will get opened)
 Make sure you are logged in to Azure provider account
 265
6. Come back to DigitalEx & click on Done
 11. Azure Subscriptions will get Updated Successfully.
 266
Azure Account Onboarding Questionnaire
 As part of our commitment to ensure a seamless onboarding experience for our clients, we have compiled a list of frequently asked 
questions (FAQs) that may arise during the Azure account onboarding process. This information is crucial in helping the DigitalEx/partner 
team understand the needs and expectations of our clients, thereby providing a comprehensive and enjoyable onboarding experience.
 Q1: What is the monthly spend on Azure resources?
 This helps us understand the scale of operations and the resource allocation required for your account.
 Q2: What type of Azure account does the client have?
 There are several types of Azure accounts:
 1. Direct CSP/MCA (Microsoft Cloud Solution Provider/Microsoft Customer Agreement).
 2. Indirect CSP/MCA or via a reseller.
 3. EA (Enterprise Agreement).
 Knowing the type of account helps us tailor the onboarding process to suit your specific requirements.
 Q3: Is cost export enabled for the client's Azure account with the following settings?
 Metric type: Actual cost
 Export type: Daily export of month-to-date
 File partitioning: enabled.
 Note: It is recommended to use an existing export, and our automated on-boarding script is designed to detect and utilize an 
existing export when on-boarding the billing account. Regardless of whether you have prior exports or not, we can capture the 
historical cost through Billing APIs.
 Q4: How many subscriptions does the client have?
 It is necessary to onboard each subscription individually. This allows DigitalEx to continuously discover resources and collect key metrics for 
providing insight, optimization, and security recommendations. Although cost ingestion only requires billing account onboarding, resource 
discovery requires onboarding each subscription separately. 
Q5: In what currency is the invoice generated?
 The currency of the invoice has implications for billing and financial tracking.
 Q6: Does the client have billing accounts that use multiple currencies, such as two billing accounts 
in different currencies?
 DigitalEx supports multiple currencies which is configurable from DigitalEX UI
 Q7: In the case of an indirect CSP/MCA/reseller type of Azure account, does the client have 
access to billing level information?
 If the client does not have access to billing level information, they will need to onboard the subscription as a billing account. Please note that 
an automated option is not currently available for this process.
 267
You’re understanding and cooperation with these questions will significantly enhance the onboarding process and ensure we can provide 
you with the best possible service.
 268
Azure Account Onboarding Security FAQs
 Our commitment to a seamless onboarding experience includes providing comprehensive answers to frequently asked questions. Here are 
some of the key FAQs related to Azure Account Onboarding with DigitalEx:
 Q1: What is the process for onboarding an Azure account with DigitalEx?
 Azure Billing Accounts and Azure Subscriptions are onboarded differently:
 Azure Billing Account: Manages invoices, payments, and cost tracking for one or more subscriptions. This can be onboarded as a 
billing account, either automatically through a script or manually with instructions.
 Azure Subscriptions (usage accounts): Used to create Azure resources, and it is recommended to onboard all subscriptions as usage 
accounts.
 If your Azure account is an Indirect CSP/MCA/reseller and you don't have billing access from the reseller, the subscription may need to be 
onboarded as a billing account.
 Q2: What is a billing account and why does DigitalEx need it?
 A billing account, also known as an Azure Billing Account, allows DigitalEx to display detailed cost data on its dashboard and perform cost 
and budget management functions.
 Q3: What is a usage account and why does DigitalEx need it?
 A usage account, or Azure Subscription, is used to create Azure resources. Onboarding usage accounts with DigitalEx enables you to view 
your resource inventory across all subscriptions in one place, analyze resource costs over time, identify unused resources, and receive 
valuable recommendations.
 Q4: How do I access the guide for onboarding my billing account?
 The guide for onboarding your billing account is available at this link: Azure Billing Account Onboarding Guide
 Q5: How do I access the guide for onboarding my usage account?
 The guide for onboarding your usage account can be found at this link: Azure Usage Account Onboarding Guide
 Q6: Is it secure to onboard my Azure account with DigitalEx? If so, why?
 Yes, DigitalEx has implemented stringent measures to ensure the security of your account and data. We use Azure Active Directory (AAD) 
for access and grant our application only the minimum required read-only permissions. The application's secret keys are securely stored in a 
vault. For billing and usage accounts, DigitalEx has read access only to azure AD app.
 Q7: How does Azure CLI onboarding for billing accounts work?
 Using Azure CLI for onboarding can improve efficiency and reduce the risk of mistakes. When you execute the onboarding command, the 
system will:
 Display a list of accessible accounts for you to select which one to onboard.
 Create a new Azure AAD app and grant it read-only access to the app.
 Your understanding and cooperation will significantly improve the onboarding process, ensuring we can provide the best possible service.
 269
Azure Troubleshooting
 The following are the steps you should take if you're seeing a warning message on the public clouds page.
 Click on Edit of the billing/subscription account which shows warning.
 Copy the command
 Login to your Azure account where billing/subscription is configured.
 Open the cloudshell
 Run the command and till its completed.
 Click Done from DigitalEx UI & Run the Data ingestion
 If you come across any error message on DigitalEx UI while onboarding Billing account or subscription, please adhere to the following table 
for resolution.
 Below are the actions you should take when you encounter the following error message.
 If you come across this error message; it signifies that an account with this Account ID has already been 
onboarded.
 270
When encountering this error message, you have entered the invalid Account ID.
 271
272
If you encounter this error message, it means that you've partially entered an incorrect Account ID.
 273
274
When you come across this error message, it indicates that you've entered the invalid Subscription ID.
 275
276
If you encounter this error message, it means that you've partially entered an incorrect Subscription ID.
 277
278
When you come across this error message, it indicates that you've entered the invalid Tenant ID.
 279
280
If you encounter this error message, it means that you've partially entered an incorrect Tenant ID.
 281
282
If you encounter this error message, it means that you've partially entered an incorrect or invalid Client ID.
 283
284
If you encounter this error message, it means that you've partially entered an incorrect or invalid Secret.
 285
286
 If a WARNING message appear on the DigitalEx public page interface, please adhere to the following table for resolution
 Microsoft.Storage/BlobReader This permission is necessary 
to access and read the cost 
exports from the bucket.
 Add "Storage Blob Data 
Reader" manually from Azure 
portal 
https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap   
Microsoft.Billing/billingAccountsO
 R/subscriptions
 This permission is necessary 
to access and read historical 
cost-related information at 
the scope of billing or 
subscription.
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope
 https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Microsoft.CostManagement/query To retrieve cost-related data 
from previous months within 
the scope of billing or 
subscription, this particular 
permission is necessary.
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope 
https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Microsoft.CostManagement/gener
 ateCostDetailsReport
 This permission is needed to 
use the API to produce cost 
exports for historical months 
within the scope of billing or 
subscription
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope
 https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Permission Details Resolution Doc References
Common Troubleshooting
 If you come across an issue related to access levels within your Azure portal, here are some potential solutions.
 a. To create exports and assign roles to AAD app we need Owner (recommended) or both Contributor and User Access Administrator 
role for logged in user (Ref:  
Azure built-in roles - Azure RBAC )
 b. To manage an AAD app and create a client secret we need Application Administrator role. 
(Ref:  
Microsoft Entra built-in roles - Microsoft Entra ID Azure
 DigitalEx enables users to onboard their Azure billing account. This process involves setting up the necessary accounts and permissions, 
configuring the billing and cost management settings, and integrating the billing data with DigitalEx. Onboarding the Azure billing account 
with DigitalEx allows users to track and manage their Azure costs and usage, and to optimize their use of Azure resources to reduce costs. 
It is important to carefully follow the steps in the onboarding process to ensure that the Azure billing account is set up correctly and able to 
accurately track and report on costs.
 Billing Account
 The billing accounts feature in DigitalEx allows users to view the cost of resources from their Azure accounts and regions in a single 
interface. With this feature, users can search and view the cost of resources across all regions and all accounts, and see where resources 
are located. The cost dashboard provides a snapshot of costs, enabling users to quickly understand overall trends and gain visibility into 
their spending across all their public and private cloud providers. This feature can be helpful for organizations looking to optimize their Azure 
usage and reduce costs.
 DigitalEx supports three different types of accounts:
 1. Customer Agreement billing account: This billing account is managed by the organization itself, and the billing ID is used in the billing 
level scope for onboarding.
 2. Partner Agreement billing account: This billing account is managed by a third-party seller and the end user has subscription level access. 
Users can onboard both the billing and subscription levels.
 3. Direct Enterprise Agreement customers: This account is similar to a direct Customer Agreement billing account.
 These different account types allow DigitalEx to support a variety of billing and payment arrangements, and to provide users with the tools 
and features they need to manage their cloud resources and costs effectively.
 Usage Account
 A usage account in an Azure organization is a subscription account, which is any account that is not the management account. Policies can 
be attached to a usage account to apply controls specifically to that account. It is important to properly set up and manage subscription 
accounts in an Azure organization to ensure that resources are used effectively and in accordance with organizational policies and controls.
 164
Azure Biling Account Onboarding
 There are two ways to onboard the Billing Account
 1. Manual UI Onboarding
 Azure Billing Account Manual UI Onboarding 
2. Manual CLI Onboarding
 Azure Billing Account Manual CLI Onboarding 
3. Cloud Shell Based Onboarding (Automated)
 Azure Billing Account Cloud Shell 
165
Azure Biling Account Manual UI Onboarding
 Account Type: MCA, MPA, CSP
 Account Type: Enterprise Account(EA)
 166
Account Type: MCA, MPA, CSP
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps.
 Step-1: Create Azure Active Directory app
 Step-2: Assign permissions to the app
 Step-3: Retrieve Account ID
 Step-4: Connect Billing Account
 167
Step-1: Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 168
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 169
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 170
Step-2: Assign permissions to the app
 In this step, we will assign the Billing Account Reader permission to the app created in Step 1. This role grants read access to account 
information and cost reports. It’s important to note that the Billing Account Reader role DOES NOT provide any WRITE permissions to 
DigitalEx platform.
 Procedure in this step is also documented by Azure here : assign-roles-azure-service-principals.
 If you choose to onboard the billing scope you must add the Billing Account Reader role
 If you choose to onboard the subscription scope, you must add the Cost Management Reader role
 1. Click on Menu 
2. Go to Cost Management + Billing
 3. Click on Access Control(IAM)
 4. Click on Add (Add role assignment page will get opened )
 5. Select the Billing account reader(Select based on your scope mentioned in the above note)
 6. Search the App created in Step 1
 7. Click on Add Button
 171
172
Step-3: Retrieve Account ID
 Steps to Retrieve Account ID:
 1. Click on Menu
 2. Click on Cost Management + Billing.
 3. Click on Properties
 4. Copy the Account ID
 Steps to Retrieve Tenant ID:
 1. Click on Menu
 2. Go to Azure Active directory.
 173
3. Click on App Registration
 4. Click on your application
 174
5. Copy the Application Client id & Tenant id 
6. Client Secret is already copied in 
Step-1: Create Azure Active Directory app 
Make sure to record all of the details that are retrieved, as they will be needed for the manual creation of a billing account.
 175
Step-4: Connect Biling Account
 If you set up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply select the 
"Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 176
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type (To know your Acc type follow this link 
ent )
 4. Select the Account Scope 
View your billing accounts in Azure portal - Microsoft Cost Managem
 Using subscription scope is not recommended as it provides limited features and cost savings opportunities.
 5. Fill in the following details captured in Step 1
 Billing Account ID
 Tenant ID
 Client ID
 Client Secret
 6. Click Connect 
177
5. The onboarded Enrollment Account will be displayed with the list of All linked Subscription accounts.
 6. Click Data Ingestion to skip waiting  
178
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 7. Go to the Menu option and Click Cost.
 8. Data will display immediately after successful ingestion.
 179
180
Account Type: Enterprise Account(EA)
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps.
 Scope: Billing Account
 Scope: Department
 181
Scope: Biling Account
 Step- 1: Create Azure Active Directory app
 Step- 2: Assign permissions to the app
 Step - 3: Connect Billing Account
 182
Step- 1: Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 183
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 184
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 185
Step- 2: Assign permissions to the app
 In this step, we will assign the EnrollmentReader permission to the app created in Step 1. This role grants read access to account 
information and cost reports. It’s important to note that the EnrollmentReader role DOES NOT provide any WRITE permissions to 
DigitalEx platform.
 Procedure in this step is also documented by Azure here : assign-roles-azure-service-principals.
 1. Unlike other billing account types, Azure does not allow role assignment of Enterprise Agreement (EA) accounts using the user 
interface. Instead, we’ll use the official Azure HTTP API to achieve this.
 2. Before hitting the API, lets capture few details we would need to pass to the API
 a. billingAccountName : This is simply an ID of your billing account you can capture from Cost Management + Billing > Overview 
page
 b. billingRoleAssignmentName : This parameter is a unique GUID that you need to provide. You can          
website to generate a unique GUID. 
use the GUID Generator 
c. Principal ID : This is Enterprise App’s Object ID. For this, navigate to Microsoft Entra ID > Enterprise applications and look for the 
app we created in step 1 and capture it’s Object ID
 186
3. We’re now ready to hit an API to make role assignment. Open following URL on the same browser window where you have Azure portal 
open : Role Assignments and click Try It and select correct directory if it asks. Fill in the parameters billingAccountName and 
billingRoleAssignmentName with the values captured in last step. And in the body section put following JSON,
 1 {
 2  
3    
4    
5    
6  
7 }
 "properties": {
 "principalId": "<principal_id>",
 "principalTenantId": "<tenant_id>",
 }
 "roleDefinitionId": "/providers/Microsoft.Billing/billingAccounts/<billing-account
id>/billingRoleDefinitions/24f8edb6-1668-4659-b5e2-40bb5f3a7d7e"
 4. Make sure to replace 
<principal_id>" and 
<tenant_id> and 
<billing-account-id> with correct values captured in earlier steps. 
roleDefinitionId is an ID for and EnrollmentReader role as documented here : permissions-that-can-be-assigned-to-the-service-principal
 After filling in all the parameters and body, click Run. API call should return 200 OK. if it doesn’t, do not proceed.
 187
Step - 3: Connect Biling Account
 If you are setting up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply 
select the "Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 188
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type as EA
 4. Select the Account Scope as Billing Account
 5. Fill in the following details capture in Step 1 and Step 2
 Billing Account ID
 Tenant ID 
Client ID 
Client Secret 
6. Click Connect 
189
7. The onboarded Account will be displayed with the list of All linked Subscription accounts.
 8. Click Data Ingestion to skip waiting  
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 9. Go to the Menu option and Click Cost.
 190
10. Data will display immediately after successful ingestion.
 191
192
Scope: Department
 Step- 1 : Create Azure Active Directory app
 Step - 2 : Assign permissions to the app
 Step - 3 : Connect Billing Account
 193
Step- 1 : Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Login to your Azure environment where billing account exist
 2. Navigate to Microsoft Entra ID > App registration >New registration
 3. Enter app name and keep the other options as default and click Register
 194
4. After app is created, you would land on app Overview page, capture following details from this page, Directory (tenant) ID and 
Application (client) ID
 5. Navigate to Certificates & secrets > New client secret and create a secret. After creation is successful, capture data under Value field
 195
6. By end of this step, you would have captured following information.
 Directory (tenant) ID
 Application (client) ID
 Secret Value
 196
Step - 2 : Assign permissions to the app
 In this step, we will assign the DepartmentReader permission to the app created in Step 1. This role grants read access to department 
information and cost reports at department scope. It’s important to note that the DepartmentReader role DOES NOT provide any WRITE 
permissions to DigitalEx platform.
 Procedure in this step is also documented by Azure here : #assign-the-department-reader-role-to-the-service-principal
 1. Unlike other billing account types, Azure does not allow role assignment of Enterprise Agreement (EA) accounts using the user 
interface. Instead, we’ll use the official Azure HTTP API to achieve this.
 2. Before hitting the API, lets capture few details we would need to pass to the API
 a. billingAccountName : This is simply an ID of your billing account you can capture from Cost Management + Billing > Properties.
 b. departpartName : This is simply an ID of your department account you can capture from Cost       
Management + Billing > 
Overview
 c. billingRoleAssignmentName : This parameter is a unique GUID that you need to provide. You can          
website to generate a unique GUID.
 use the GUID Generator 
d. Principal ID : This is Enterprise App’s Object ID. For this, navigate to Microsoft Entra ID > Enterprise applications and look for the 
app we created in step 1 and capture it’s Object ID
 3. We’re now ready to hit an API to make role assignment. Open following URL on the same browser window where you have Azure portal 
open : Enrollment Department Role Assignments - Put and click Try It and select correct directory if it asks. Fill in the parameters, 
billingAccountName, departmentName and billingRoleAssignmentName with the values captured in last step. And in the body section 
put following JSON,
 1 {
 2  
3    
4    
5    
6  
7 }
 "properties": {
 "principalId": "<principal_id>",
 "principalTenantId": "<tenant_id>",
 }
 "roleDefinitionId": 
/providers/Microsoft.Billing/billingAccounts/<BILLING_ACCOUNT_ID>/departments/<DEPARTMENT_ID>/billingRoleDefini
 tions/db609904-a47f-4794-9be8-9bd86fbffd8a
 197
4. Make sure to replace 
<tenant_id> and 
<principal_id> and 
<BILLING_ACCOUNT_ID> and 
<DEPARTMENT_ID> with correct values 
captured in earlier steps. roleDefinitionId is an ID for DepartmentReader role as documented here : permissions-that-can-be-assigned
to-the-service-principal. After filling in all the parameters and body, click Run. API call should return 200 OK. if it doesn’t, do not proceed.
 198
Step - 3 : Connect Biling Account
 If you are setting up a billing account for the first time, you will be presented with the following screen. To create a billing account, simply 
select the "Create Billing Account" option.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 199
2. Select Azure Provider & Click on Manual tab
 3. Choose your account type as ES
 4. Select the Account Scope as Department
 5. Fill in the following details captured in Step 1 and Step 2
 Department Id
 Tenant ID 
Client ID 
Client Secret 
200
6. Click Connect 
7. The onboarded Account will be displayed with the list of All linked Subscription accounts.
 8. Click Data Ingestion to skip waiting  
201
After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 9. Go to the Menu option and Click Cost.
 202
10. Data will display immediately after successful ingestion.
 203
204
Azure Biling Account Manual CLI Onboarding
 The steps below need to be executed in the Azure Cloud Shell. Please log in to the Azure portal and launch the 
Cloud Shell from the navigation bar.
 To create Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can have both the 
Contributor and User Access Administrator roles.
 Step-1:  Create AD Application
 Execute the following command to create AD App
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME> : AD app name of your choice
 After executing the command, capture the App id, Password(secret) & Tenant.
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Step-2:  Assign permission to the app
 If you are onboarding billing scope as billing, Follow the below steps for assigning permission to the app   
a. Login to Azure console > Click on Menu > Cost Management + Billing > Access Control (IAM)
 b. Click Add > Select the Billing account reader > Enter the app created in Step-1 above. 
Follow this link to get detailed steps  
Step-2: Assign permissions to the app  
If you are onboarding subscription scope as billing. Execute the following command to assign permission to the app.
 1 az role assignment create --assignee "<APP_ID>" --role "Cost Management Reader" --scope 
/subscriptions/<SUBSCRIPTION_ID>
 <APP-ID> : AD app id captured in Step-1
 <SUBSCRIPTION_ID> : Your subscription id you wish to onboard
 Step-3: Retrieve Account ID
 Follow the steps to get the account id 
Step-3: Retrieve Account ID 
Step-4: Submit Details in DigitalEx
 Get the details Tenant ID, Client ID, Client Secret, Account ID.
 Follow the below steps to onboard the billing account in DigitalEx.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link Azure Connect Billing Account for Partner to onboard additional providers
 205
1. Click on Azure Provider
 2. Click on Connect manually
 206
3. Click on Connect Billing Account
 4. Enter the details which you have captured above.
 5. Click on connect & done.
 If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1. Navigate to Menu > Admin > Public Clouds > +Account.
 207
2. Click on Azure Provider & Click on Manual tab
 3. Enter the details which you have captured above.
 208
4. Click Connect
 5. The onboarded Billing Account will be displayed with the list of All linked Subscription accounts.
 209
After adding a new account, it may take up to 30 minutes for the system to discover and process the data.
 6. Go to the Menu option and Click Cost.
 7. Data will display immediately after successful ingestion.
 210
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
211
Azure Biling Account Cloud Shel
 Cloud Shell Billing Account onboarding has different steps.
 Step-1: Login to Azure account
 Step-2: Execute the script from the Azure Cloud Shell.
 212
Step-1: Login to Azure account
 To onboard Azure through the CLI, it is necessary to have the Owner role assigned.
 Below are the steps that need to be performed if the user registers for the first time, the below page is displayed.
 1. Click on the Login button and Login into Azure
 2. The page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx
 3. It will ask to select the environment (Select as per your choice)
 4. Copy the script.
 5. Paste in Cloud Shell Editor & Click Enter
 6. It will ask to select account type, select & click enter.
 7. Enter 'y' to confirm account. 
213
Ignore Bad request syntax or unsupported method retrying messages.
 8. Click on Done 
9. Click Skip waiting or wait for 24hrs to display the data.
 Below are the steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner
 3. Click on Admin > Cloud Providers 
4. Click on +Account
 5. Select Azure Provider
 6. Click on Cloud Shell
 7. Click on Log In 
214
The page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 Below are the description of steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3.  Click on Admin > Public Clouds
 4. Click on +Account
 5. Select Azure Provider 
6. Click on Cloud Shell 
215
7. Click on the Login button as shown in the above image
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 216
Step-2: Execute the script from the Azure Cloud Shel.
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step. 
2. It will ask to select the environment (Select as per your choice) 
3. Paste in Cloud Shell Editor and click Enter
 To onboard a subscription as a billing account, append the command with --sub as a suffix.
 217
4. It will ask for the account type, select & click enter. (Follow this link to know your account type 
l - Microsoft Cost Management )
 5. Enter 'y' to confirm account & subscription 
6. Script will run automatically
 View your billing accounts in Azure porta
 Ignore Bad request syntax or unsupported method retrying messages.
 7. Click on the Done button in DigitalEx , after the script running is successfully completed. 
218
8. Click Data Ingestion to skip waiting so that data is displayed immediately
 9. You will see the ingestion in progress 
10. The onboarded Enrollment Account will be displayed with the list of All linked Subscription accounts.
 219
11. Go to the Menu option and Click Cost to view the cost data. 
12. Data will display immediately after successful ingestion.
 220
221
Azure Management Group onboarding as biling
 You can onboard azure management group as billing by following the CLI steps provided below.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Create AAD
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: Enter the unique name. Recommended (digitalex_management_group)
 Capture App id and share it with Owner required to Assign Permissions to the App 
Capture Password (Secret) and Tenant id required to Connect Billing Account
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope 
"/providers/Microsoft.Management/managementGroups/<MANAGEMENT_GROUP-ID>" -o table
 <APP_ID> : Enter App id created in above step
 <MANAGEMENT_GROUP-ID>: Enter your management group Id(To Get Management Group id Navigate to Azure Console > Search 
Management Group > Capture tenant group id)
 Connect Billing Account
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds
 3. Click on +Account 
4. Select CSP as Account type and Billing Scope as Management group
 5. Enter required details 
6. Click Connect
 You can use the same credentials to onboard the Management Group as a usage account.
 LI Onboarding 
Azure Management Group Manual C
 222
Update Azure Enrolment / Contract Manualy.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Azure tab 
4. Click on the Edit Button 
5. Click on Manual tab
 6. Update the details 
223
7. Click on Update
 8. Azure Enrollment / Contract will get Updated Successfully.
 224
Update Azure Enrolment / Contract using Cloud Shel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure tab 
4. Click on the Edit Button
 5. Click on the login button(Azure CloudShell will get opened) 
Note: Make sure you are logged in to Azure provider account
 225
6. Copy the script
 7. Paste the script into Azure CloudShell & Click Enter
 8. Come back to DigitalEx & click on Done
 9. Azure Enrollment / Contract will get Updated Successfully.
 226
Azure Subscriptions Onboarding
 There are two ways to onboard the Subscriptions
 1. Manual Onboarding
 Azure Subscription Account Manual Onboarding 
2. Cloud Shell Based Onboarding (Automated)
 Azure Subscriptions Account Cloudshell Onboarding 
227
Management Groups
 Integrating subscriptions into DigitalEx grants access to valuable resources, metrics, and recommendations, optimizing cloud costs. Receive 
tailored recommendations for rightsizing, orphan, idle resources to optimize costs while maintaining performance. 
You can onboard subscriptions either of the way
 Azure Management Group Manual CLI Onboarding
 Azure Management Group Cloudshell Onboarding
 228
Azure Management Group Manual CLI Onboarding
 Azure Management Group CLI Onboarding 
You can onboard all subscriptions as a group by following the CLI steps provided below 
If you have already set up the Management Group for billing using the steps provided here 
Azure Management Group on
 boarding as billing  you can utilize the same credentials to onboard the Management Group again.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Create AAD
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: Enter the unique name. Recommended (digitalex_management_group)
 Capture App id and share it with Owner required to Assign Permissions to the App
 Capture Password (Secret) and Tenant id required to Connect Management Group 
To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope 
"/providers/Microsoft.Management/managementGroups/<MANAGEMENT_GROUP-ID>" -o table
 <APP_ID> : Enter App id created in above step
 <MANAGEMENT_GROUP-ID>: Enter your management group Id(To Get Management Group id Navigate to Azure Console > Search 
Management Group > Capture tenant group id)
 Connect Management Group
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds
 3. Click on +Management Groups & Enter required details
 4. Click Connect.
 229
Azure Management Group Cloudshel Onboarding
 Cloud Shell Management Group onboarding has different steps.
 Step-1: Login to Azure Cloud Shell
 Step-2 : Execute the Script
 230
Step-1: Login to Azure Cloud Shel
 User should be Log In as Billing Admin or Project admin.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner.
 3. Click on Public Clouds under Admin
 231
4. Below Page will be displayed with Management Group
 5. Click on Connect button of the Management Group
 232
6. Click on the Login button as shown in the above image.
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 233
Step-2 : Execute the Script
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 234
3. Script will run automatically.
 Ignore Bad request syntax or unsupported method retrying messages.
 4. Click on the Done button in DigitalEx, after the script running is successfully completed.
 235
5. On-boarded Management Group will be displayed with Active Status. It takes up to 2 hours to discover the data.
 6. Click the Resource from the Menu option.
 236
7. Click on Resources (All the resource data will be displayed) 
237
238
Individual Subscriptions
 Integrating subscriptions into DigitalEx grants access to valuable resources, metrics, and recommendations, optimizing cloud costs. Receive 
tailored recommendations for rightsizing, orphan, idle resources to optimize costs while maintaining performance.
 You can onboard subscriptions either of the way
 Azure Subscription Account Manual Onboarding 
Azure Subscriptions Account Cloudshell Onboarding 
239
Azure Subscription Account Manual Onboarding
 Manual Subscription onboarding can be done either through the Azure UI portal by following the steps below, or by using Azure CLI 
commands
 If you wish to onboard through Azure Manual UI folow below steps
 The steps below will guide you through the process of onboarding from the Azure UI portal. Please log in to the 
Azure portal and follow these steps
 Step-1 : Create Azure Active Directory app
 Step-2: Assign Permissions to an app
 Step-3: Connect Usage Account
 If you wish to onboard through Azure Manual CLI folow below steps
 The steps below need to be executed in the Azure Cloud Shell. Please log in to the Azure portal and launch the 
Cloud Shell from the navigation bar
 To manage an Azure Active Directory (AAD) app and to assign a role, the owner role is required.
 1. Login to Microsoft Azure Cloud Shell and execute the below command.
 1 az ad sp create-for-rbac -n <APP_NAME> --role Reader --scopes "/subscriptions/<SUBSCRIPTION_ID>"
 <APP_NAME> : App name of your choice
 <SUBSCRIPTION_ID> : Your azure subscription id, follow this link to get subscription id. 
al - Azure portal 
Get subscription and tenant IDs in the Azure port
 The above command will create an <APP_NAME> of your choice and assign the Reader role for the <SUBSCRIPTION_ID> subscription 
that you want to onboard as a usage account in DigitalEx.
 2. Go to the DigitalEx portal and follow this steps Connect Subscription and enter the credentials obtained in the previous cloud shell 
output. 
IF U DONT HAVE OWNER ROLE TO EXECUTE ABOVE COMMAND FOLLOW BELOW STEPS
 Create AAD & Secret
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required.
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME>: AD app name of your choice
 Capture App id and share it with Owner required to Assign Permissions to the App
 Capture App Id, Password(Secret) and Tenant id and share it with the partner company required to Connect Management Group
 240
To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope "/subscriptions/<SUBSCRIPTION_ID>" -o 
table
 <APP_ID> : Enter App id
 <SUBSCRIPTION_ID> : Enter your subscription id
 Connect Subscription
 1. Login to DigitalEx as Owner
 2. Go to Menu > Admin > Public Clouds
 3. Click on Connect for the subscription under subscriptions tab of Azure & Enter required details
 4. Click Connect.
 241
Step-1 : Create Azure Active Directory app
 Steps to Create an Application
 1. Click on Menu
 2. Go to Azure Active directory
 3. Click on App Registration 
242
4. Click on New Registration 
5. Enter Name of Application
 6. Supported account type is selected automatically.
 7. Click on Register
 243
8. App will get created as shown below.
 9. Copy Application Client id & Tenant id
 Steps to add client secret
 1. Click on Certificates & Secrets
 244
2. Click on New Client Secret 
3. Enter Description
 4. Select Expires as 24 months maximum
 5. Click Add
 6. Applied client secret will be displayed as shown below
 245
7.Copy the Value(not Secret ID) which is used later for manual creation of usage account .
 246
Step-2: Assign Permissions to an app
 In order to grant permissions to an app, the owner role is required.
 1. Click on Subscriptions
 2. Click on your subscription
 3. Click on Access Control (IAM)
 4. Click on Add → Add role assignment
 247
5. Click on the search box & enter the role name as Reader role
 6. Select the role & click next 
7. Click on Select Members
 248
8. Enter the App name (which you have created in 
Step-1 : Create Azure Active Directory app ) & Click Select
 9. Click Next 
249
10. Click Review + assign
 250
Step-3: Connect Usage Account
 Below are the steps to connect azure usage account:
 1. Login to DigitalEx
 2. Go to Menu > Admin > Public Clouds 
3. Below Page will be displayed with the list of All linked Subscription accounts.
 4. Click on Connect button of the specific subscription account / You can directly click on +Subscription
 251
5. Click on Manual
 6. Fill in the following details. 
Active Directory (Tenant) ID 
Application (Client) ID 
Step-1 : Create Azure Active Directory app 
Step-1 : Create Azure Active Directory app 
Application (Client) Secret 
7. Click Connect
 Step-1 : Create Azure Active Directory app 
8. On-boarded Subscription accounts will be displayed on the list of a member accounts. It takes up to 2 hours to discover the data.
 9. Click the Resource from the Menu option.
 252
10. Resources will get discovered in DigitalEx
 253
254
Azure Subscriptions Account Cloudshel Onboarding
 Step-1 :Login to Azure Cloud Shell
 Step-2 :Execute the Script
 255
Step-1 :Login to Azure Cloud Shel
 User should be Log In as Billing Admin or Project admin.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner.
 3. Click on Public Clouds under Admin
 256
4. Below Page will be displayed with the list of All linked Member accounts.
 5. Click on Connect button of the specific subscription account/ You can directly click on +Subscription
 257
6. Click on the Login button as shown in the above image
 Page is navigated to the Azure login page where the user needs to enter Azure credentials. After successful login into the Azure 
account, the user should come back to DigitalEx to follow the next steps.
 258
Step-2 :Execute the Script
 Steps to Execute the Script from Azure Cloud Shell:
 1. Copy the script and Execute the command provided below from within the Azure CloudShell terminal window, which is shown at the 
bottom part of the Azure Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 3. Script will run automatically.
 259
Ignore Bad request syntax or unsupported method retrying messages.
 4. Click on the Done button in DigitalEx, after the script running is successfully completed.
 5.  On-boarded Subscription accounts will be displayed on the list of a member accounts. It takes up to 2 hours to discover the data.
 260
6. Click the Resource from the Menu option.
 7. Click on Resources (All the resource data will be displayed) 
261
262
Update Azure Subscription Manualy
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure
 4. Go to Subscriptions
 5. Click on Edit Subscription Account
 6. Click on Manual
 7. Update the Details
 8. Click on Update
 263
8. Azure Subscription will get Updated Successfully.
 264
Update Azure Subscription using Cloud Shel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on Azure
 4. Go to Subscriptions
 5. Click on the Edit button which the Subscription Account you want to update
 5. Click on the login button(Azure CloudShell will get opened)
 Make sure you are logged in to Azure provider account
 265
6. Come back to DigitalEx & click on Done
 11. Azure Subscriptions will get Updated Successfully.
 266
Azure Account Onboarding Questionnaire
 As part of our commitment to ensure a seamless onboarding experience for our clients, we have compiled a list of frequently asked 
questions (FAQs) that may arise during the Azure account onboarding process. This information is crucial in helping the DigitalEx/partner 
team understand the needs and expectations of our clients, thereby providing a comprehensive and enjoyable onboarding experience.
 Q1: What is the monthly spend on Azure resources?
 This helps us understand the scale of operations and the resource allocation required for your account.
 Q2: What type of Azure account does the client have?
 There are several types of Azure accounts:
 1. Direct CSP/MCA (Microsoft Cloud Solution Provider/Microsoft Customer Agreement).
 2. Indirect CSP/MCA or via a reseller.
 3. EA (Enterprise Agreement).
 Knowing the type of account helps us tailor the onboarding process to suit your specific requirements.
 Q3: Is cost export enabled for the client's Azure account with the following settings?
 Metric type: Actual cost
 Export type: Daily export of month-to-date
 File partitioning: enabled.
 Note: It is recommended to use an existing export, and our automated on-boarding script is designed to detect and utilize an 
existing export when on-boarding the billing account. Regardless of whether you have prior exports or not, we can capture the 
historical cost through Billing APIs.
 Q4: How many subscriptions does the client have?
 It is necessary to onboard each subscription individually. This allows DigitalEx to continuously discover resources and collect key metrics for 
providing insight, optimization, and security recommendations. Although cost ingestion only requires billing account onboarding, resource 
discovery requires onboarding each subscription separately. 
Q5: In what currency is the invoice generated?
 The currency of the invoice has implications for billing and financial tracking.
 Q6: Does the client have billing accounts that use multiple currencies, such as two billing accounts 
in different currencies?
 DigitalEx supports multiple currencies which is configurable from DigitalEX UI
 Q7: In the case of an indirect CSP/MCA/reseller type of Azure account, does the client have 
access to billing level information?
 If the client does not have access to billing level information, they will need to onboard the subscription as a billing account. Please note that 
an automated option is not currently available for this process.
 267
You’re understanding and cooperation with these questions will significantly enhance the onboarding process and ensure we can provide 
you with the best possible service.
 268
Azure Account Onboarding Security FAQs
 Our commitment to a seamless onboarding experience includes providing comprehensive answers to frequently asked questions. Here are 
some of the key FAQs related to Azure Account Onboarding with DigitalEx:
 Q1: What is the process for onboarding an Azure account with DigitalEx?
 Azure Billing Accounts and Azure Subscriptions are onboarded differently:
 Azure Billing Account: Manages invoices, payments, and cost tracking for one or more subscriptions. This can be onboarded as a 
billing account, either automatically through a script or manually with instructions.
 Azure Subscriptions (usage accounts): Used to create Azure resources, and it is recommended to onboard all subscriptions as usage 
accounts.
 If your Azure account is an Indirect CSP/MCA/reseller and you don't have billing access from the reseller, the subscription may need to be 
onboarded as a billing account.
 Q2: What is a billing account and why does DigitalEx need it?
 A billing account, also known as an Azure Billing Account, allows DigitalEx to display detailed cost data on its dashboard and perform cost 
and budget management functions.
 Q3: What is a usage account and why does DigitalEx need it?
 A usage account, or Azure Subscription, is used to create Azure resources. Onboarding usage accounts with DigitalEx enables you to view 
your resource inventory across all subscriptions in one place, analyze resource costs over time, identify unused resources, and receive 
valuable recommendations.
 Q4: How do I access the guide for onboarding my billing account?
 The guide for onboarding your billing account is available at this link: Azure Billing Account Onboarding Guide
 Q5: How do I access the guide for onboarding my usage account?
 The guide for onboarding your usage account can be found at this link: Azure Usage Account Onboarding Guide
 Q6: Is it secure to onboard my Azure account with DigitalEx? If so, why?
 Yes, DigitalEx has implemented stringent measures to ensure the security of your account and data. We use Azure Active Directory (AAD) 
for access and grant our application only the minimum required read-only permissions. The application's secret keys are securely stored in a 
vault. For billing and usage accounts, DigitalEx has read access only to azure AD app.
 Q7: How does Azure CLI onboarding for billing accounts work?
 Using Azure CLI for onboarding can improve efficiency and reduce the risk of mistakes. When you execute the onboarding command, the 
system will:
 Display a list of accessible accounts for you to select which one to onboard.
 Create a new Azure AAD app and grant it read-only access to the app.
 Your understanding and cooperation will significantly improve the onboarding process, ensuring we can provide the best possible service.
 269
Azure Troubleshooting
 The following are the steps you should take if you're seeing a warning message on the public clouds page.
 Click on Edit of the billing/subscription account which shows warning.
 Copy the command
 Login to your Azure account where billing/subscription is configured.
 Open the cloudshell
 Run the command and till its completed.
 Click Done from DigitalEx UI & Run the Data ingestion
 If you come across any error message on DigitalEx UI while onboarding Billing account or subscription, please adhere to the following table 
for resolution.
 Below are the actions you should take when you encounter the following error message.
 If you come across this error message; it signifies that an account with this Account ID has already been 
onboarded.
 270
When encountering this error message, you have entered the invalid Account ID.
 271
272
If you encounter this error message, it means that you've partially entered an incorrect Account ID.
 273
274
When you come across this error message, it indicates that you've entered the invalid Subscription ID.
 275
276
If you encounter this error message, it means that you've partially entered an incorrect Subscription ID.
 277
278
When you come across this error message, it indicates that you've entered the invalid Tenant ID.
 279
280
If you encounter this error message, it means that you've partially entered an incorrect Tenant ID.
 281
282
If you encounter this error message, it means that you've partially entered an incorrect or invalid Client ID.
 283
284
If you encounter this error message, it means that you've partially entered an incorrect or invalid Secret.
 285
286
 If a WARNING message appear on the DigitalEx public page interface, please adhere to the following table for resolution
 Microsoft.Storage/BlobReader This permission is necessary 
to access and read the cost 
exports from the bucket.
 Add "Storage Blob Data 
Reader" manually from Azure 
portal 
https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap   
Microsoft.Billing/billingAccountsO
 R/subscriptions
 This permission is necessary 
to access and read historical 
cost-related information at 
the scope of billing or 
subscription.
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope
 https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Microsoft.CostManagement/query To retrieve cost-related data 
from previous months within 
the scope of billing or 
subscription, this particular 
permission is necessary.
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope 
https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Microsoft.CostManagement/gener
 ateCostDetailsReport
 This permission is needed to 
use the API to produce cost 
exports for historical months 
within the scope of billing or 
subscription
 Add “Billing Account Reader” 
role at billing scope or add 
“Cost Management Reader” 
role at subscription scope
 https://help.digitalex.io/content/
 step-3-assign-required-roles
permissions-to-the-ap  
Permission Details Resolution Doc References
Common Troubleshooting
 If you come across an issue related to access levels within your Azure portal, here are some potential solutions.
 a. To create exports and assign roles to AAD app we need Owner (recommended) or both Contributor and User Access Administrator 
role for logged in user (Ref:  
Azure built-in roles - Azure RBAC )
 b. To manage an AAD app and create a client secret we need Application Administrator role. 
(Ref:  
Microsoft Entra built-in roles - Microsoft Entra ID

GCP STEPS -
GCP
 DigitalEx allows users to onboard GCP Billing and Usage Accounts.
 Billing Account
 Billing Accounts enable users to view costs from GCP accounts and regions in a single interface. Users can search and view the costs of 
resources across all regions and accounts, and visualize where resources are located. The Cost dashboard allows users to gain insight into 
their spending across all their public and private cloud providers. It provides a quick snapshot of costs, allowing users to easily understand 
overall trends.
 Usage Account
 A Usage Account is a project in a GCP organization. Projects are all the other accounts in an organization. An account can only be a project 
of one organization at a time
 288
GCP Biling Account Onboarding
 There are two ways to onboard GCP Billing accounts.
 1. Manual Onboarding
 GCP Project Billing Account Manual Onboarding 
2. Cloud Shell Based Onboarding (Automated)
 GCP Project Billing Account Cloud Shell  
289
290
Step-1: Enable Biling Export.
 If the standard report is already enabled, use the same dataset of the standard report else create a new dataset to be enabled & 
follow the below steps.
 Steps to create Dataset and Enable Billing Export
 1. Click on Billing from Dashboard.
 2. Click on Overview and capture Billing Account id which is required in subsequent steps
 3. Click on Billing Export.
 4. Clicking on Billing export navigates to the below page. Click on Edit settings.
 5. Click on Edit Settings for Detailed usage cost
 6. Clicking on Edit navigates to the below page.
 291
7. Select the project or it automatically gets selected if there is a single project.
 8. Make a note of selected project id which is required in subsequent steps.
 9. Click Create Dataset & click Save. 
10. After saving Detailed usage cost is enabled.
 11. Make a note of dataset name which is required in subsequent steps.
 292
12. Enable the BigQuery Data Transfer Service API.
 293
Step-2: Enable Cloud Resource Manager API.
 Select the project  from the dropdown where billing export was enabled
 Steps to Enable cloud resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select.
 2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box.
 3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below.
 294
295
Step-3: Grant permissions at project scope
 Prior to proceeding with the following steps, make sure to choose the project from the top dropdown menu that you had previously 
selected in 
Step-1: Enable Billing Export. or If you have an existing export, locate the project where the export is saved and 
choose that project from the top dropdown menu
 1. Go to IAM
 2. Click on Grant Access
 3. Enter service account id under the new principals.(To get the Service account id follow instructions outlined in this page 
Service Account Id )
 4. Add Viewer Role
 5. Click on Save
 Retrieve the 
296
297
Step-4: Grant permissions at Organization scope
 Prior to proceeding with the following steps, make sure to choose the organization from top drown down.
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 To Fetch your service account id follow steps outlined on this page 
Retrieve the Service Account Id
 3. Assign the Roles (Viewer, Organization Viewer, Browser, Billing Account Viewer)
 4. Click Save
 298
Step-5: Connect Biling Account.
 If you’re onboarding an account for the first time, you’ll see the following screen, just select Create Billing Account 
1. Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 299
2. Select the GCP provider.
 3. Fill in the required details captured during Step-1
 4. Click Connect
 300
5. The onboarded Account will be displayed with the list of All linked Projects.
 6. Click Data Ingestion to skip waiting 
Note: After adding a new account, it may take up to 30 minutes for the system to discover and process the data
 301
7. Go to the Menu option and Click Cost to view the cost data.
 8. Data will display immediately after successful ingestion.
 302
303
GCP Project Biling Account Cloud Shel
 Cloud Shell Billing Account onboarding has different steps.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1: Log In to GCP account.
 Step-2: Enable Billing Export from GCP Console.
 Step-3: Execute the script from the GCP Cloud Shell.
 304
Step-1: Log In to GCP account.
 User should be Log In as Billing Admin or Project admin.
 If User is Onboarding the Account from the Setup page both Billing & Usage Account gets Onboarded.
 Below are the steps that need to be performed if the user registers for the first time, the below page is displayed. 
1. Click on Login button and Login to GCP
 2. Page is navigated to the GCP login page where the user needs to enter GCP credentials. After successful login into the GCP account, 
the user should come back to DigitalEx 
3. Enable Billing Export from GCP Console, by clicking Show Instruction you will get the steps to follow.
 4. Copy the script 
5. Paste in Cloud Shell Editor & Click Enter 
6. Click Authorize
 7. Enter 'y' to confirm the project
 8. Enter 'y' to confirm cloud billing export (After Completing the Script Execution user should come back to DigitalEx) 
305
Ignore Bad request syntax or unsupported method retrying messages.
 If you encounter any error at the time of onboarding please rerun the script once again.
 9. Click on Connect.  
11. Click Skip waiting or wait for 24hrs to display the data.
 Below are the steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner
 3. Click on Public Clouds under Admin
 4. Click +Account
 5. Select GCP Provider
 306
6. Click on Cloud Shell
 7. Click on Log In 
The page is navigated to the GCP login page where the user needs to enter GCP credentials. After successful login into the GCP account, 
the user should come back to DigitalEx to follow the next steps.
 Below are the description of steps that need to be performed if a user onboarded other providers and Logged into the Application
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Admin > Public Clouds
 4. Click on +Account
 307
5. Select GCP Provider
 6. Click on Cloud Shell
 7. Click on the Login button as shown in the above image
 Page is navigated to the GCP login page where the user needs to enter GCP credentials. After successful login into the GCP 
account, the user should come back to DigitalEx to follow the next steps.
 308
Step-2: Enable Biling Export from GCP Console.
 If Billing Export is already Enabled continue with 
Step-3: Execute the script from the GCP Cloud Shell.  Otherwise Enable 
Billing Export from GCP Console, By clicking Show Instruction you will get the steps to follow.
 309
Step-3: Execute the script from the GCP Cloud Shel.
 Steps to Execute the Script from GCP Cloud Shell:
 1. Copy the script and Execute the command provided below from within the GCP CloudShell terminal window, which is shown at the 
bottom part of the GCP Console launched in the earlier step. 
2. Paste the copied Script and click Enter. 
3. Click on AUTHORIZE 
310
5. Enter 'y' to confirm the project. 
6.  Enter 'y' to confirm the billing export. 
7. Script will run automatically  
311
Ignore Bad request syntax or unsupported method retrying messages.
 If you encounter any error at the time of onboarding please rerun the script once again.
 8. Click on the Done button in DigitalEx , after script running is successfully completed. 
312
9. Click Data Ingestion to skip waiting 
10. You will see the ingestion in progress 
11. After completing the ingestion On-boarded Billing Account will be displayed in the List as shown below. 
12. Go to the Menu option and Click Cost 
313
13. Data will display immediately after successful ingestion.
 314
315
Update GCP Biling Account using Cloud Shel
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the Edit Button
 4. Click on the login button(GCP CloudShell will get opened)
 Note: Make sure you are logged in to GCP provider account
 316
5. Copy the script
 6. Paste the script into GCP CloudShell & Click Enter
 7. Click on Authorize
 8. Enter 'y' to confirm the project.
 9. Enter 'y' to confirm the billing export
 10. Come back to DigitalEx & click on Done
 11. GCP billing account will get Updated Successfully.
 317
GCP Projects Onboarding
 There are two ways to on-board GCP Usage accounts.
 1. Manual Onboarding
 GCP Project Usage Account Manual Onboarding 
2. Cloud Formation Based Onboarding (Automated)
 GCP Project Usage Account Cloud Shell 
Following fields are required to onboard-GCP usage Account
 Project ID
 Bucket Name
 Service Account JSON Key
 318
GCP Project Usage Account Manual Onboarding
 Manual Usage Account onboarding has different steps.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1: Enable APIs
 Step-2: Grant permissions at project scope
 319
Step-1: Enable APIs
 In order to execute the below steps, you need to have owner role. Enable the APIs for all the projects you wish to onboard
 Enable Cloud Resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box. 
3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below
 320
Enable Cloud Asset API
 1. Enter Cloud Asset API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
321
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
Stackdriver Monitoring API
 1. Enter Stackdriver Monitoring API in the Search bar and Select. 
322
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the search 
box. 
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
323
Enable Recommender API
 324
325
Step-2: Grant permissions at project scope
 Before proceeding with the steps below, select the project from the dropdown that you wish to onboard.
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 To Fetch your service account id follow steps outlined on this page 
Retrieve the Service Account Id  
3. Assign the Roles (Viewer, Cloud Asset Viewer & Monitoring viewer)
 4. Click Save 
5. Now Navigate to DigitalEx portal and Click on Connect button for GCP projects.
 326
327
GCP Project Usage Account Cloud Shel
 Cloud Shell Usage Account onboarding has different steps.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1 : Login to GCP Cloud Shell
 Step -2 : Execute the Script
 328
Step-1 : Login to GCP Cloud Shel
 NOTE:
 User should be Log In as Billing Admin or Project admin.
 If User is Onboarding the Account from the Setup page both Billing & Usage Account gets Onboarded.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 329
4. Click on Connect button of the specific project 
5. Connect Project page will get open
 330
6. Click on the Login button as shown in the above image
 Page is navigated to the GCP login page where the user needs to enter GCP credentials. After successful login into the GCP 
account, the user should come back to DigitalEx to follow the next steps.
 331
Step -2 : Execute the Script
 Steps to Execute the Script from GCP Cloud Shell:
 1. Copy the script and Execute the command provided below from within the GCP CloudShell terminal window, which is shown at the 
bottom part of the GCP Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 3. Enter 'y' to confirm the project. 
332
4. Script will run automatically. 
Ignore Bad request syntax or unsupported method retrying messages.
 If you encounter any error at the time of onboarding please rerun the script once again.
 5. Click on the Done button in DigitalEx, after the script running is successfully completed. 
6. You will be able to see the project is onboarded successfully.
 333
7. Go to the Menu option and Click Resources.
 334
8. Click on Resources (All the resource data will be displayed) 
335
336
GCP Organization Manual Onboarding
 Manual Usage Account onboarding has different steps.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1:Enable APIs
 Step-2:Grant permissions at organization scope
 337
Step-1:Enable APIs
 In order to execute the below steps, you need to have owner role.
 Select the project from the top drop down before enabling APIs
 Enable Cloud Resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box. 
3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below
 338
Enable Cloud Asset API
 1. Enter Cloud Asset API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
339
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
Stackdriver Monitoring API
 1. Enter Stackdriver Monitoring API in the Search bar and Select. 
340
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the search 
box. 
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
341
Enable Recommender API
 342
343
Step-2:Grant permissions at organization scope
 Before proceeding with the steps below, select the organization from the dropdown that you wish to onboard.
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 To Fetch your service account id follow steps outlined on this page 
Retrieve the Service Account Id  
3. Assign the Roles (Viewer, Cloud Asset Viewer, Monitoring viewer and Browser)
 4. Click Save 
5. Now Navigate to DigitalEx portal and Click on Connect button for GCP Organizations.
 344
345
GCP organization onboarding using Cloud Shel
 Cloud Shell Usage Account onboarding has different steps.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1: Login to GCP Cloud Shell
 Step -2: Execute the Script
 346
Step-1: Login to GCP Cloud Shel
 NOTE:
 User should be Log In as Billing Admin or Project admin.
 If User is Onboarding the Account from the Setup page both Billing & Usage Account gets Onboarded.
 Below are the steps to Login to DigitalEx
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 4. Click on Connect button of the specific Organizations.
 5. Connect Project page will get open
 347
6. Click on the Login button as shown in the above image
 Page is navigated to the GCP login page where the user needs to enter GCP credentials. After successful login into the GCP 
account, the user should come back to DigitalEx to follow the next steps.
 348
Step -2: Execute the Script
 Steps to Execute the Script from GCP Cloud Shell:
 1. Copy the script and execute the command provided below from within the GCP CloudShell terminal window, which is shown at the 
bottom part of the GCP Console launched in the earlier step.
 2. Paste the copied Script and click Enter.
 3. Enter 'y' to confirm the project. 
4. Script will run automatically. 
Ignore Bad request syntax or unsupported method retrying messages.
 If you encounter any error at the time of onboarding please rerun the script once again.
 5. Click on the Done button in DigitalEx, after the script running is successfully completed. 
349
6. You will be able to see the project is onboarded successfully.
 7. Go to the Menu option and Click Resources.
 350
8. Click on Resources (All the resource data will be displayed) 
351
352
Update GCP Project Manualy.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the GCP tab
 4. Go to Projects
 5. Click on the Edit button which projects you want to update
 6. Click on Manual tab 
7. Enter the new JSON Key
 353
7. Click on Update
 8. GCP Project will get Updated Successfully.
 354
Update GCP Project using Cloud Shel.
 1. Go to Menu
 2. Click on Public Clouds under Admin
 3. Click on the GCP tab
 4. Go to Projects
 5. Click on the Edit button which projects you want to update
 6. Click on the login button(GCP CloudShell will get opened)
 Note: Make sure you are logged in to GCP provider account
 355
7. Click on Authorize
 8. Click on y for Project
 9. Click on y for Billing Export
 10. Come back to DigitalEx & click on Done
 11. GCP Project will get Updated Successfully.
 356
GCP Account Onboarding Questionnaire
 To ensure a smooth and comprehensive onboarding experience, it's crucial that the DigitalEx team is prepared and informed. This 
questionnaire aims to understand your needs and expectations better, thereby ensuring an efficient and enriched onboarding process.
 Q1. What is your monthly spend on GCP?
 Understanding your monthly spending will help us provide better cost management and optimization strategies.
 Q2. Is GCP detailed usage cost Export enabled for your account?
 If GCP Billing Export is already enabled, DigitalEx can ingest historical cost data. If not, we can only obtain cost data for the current month 
and future months. We recommend using an detailed usage cost export for a seamless onboarding process.
 Q3. How many GCP projects do you have?
 To continuously discover resources and collect key metrics for insight and optimization, it is necessary to onboard each project individually.
 Q4. In what currency is your invoice generated?
 This information will help us better understand your billing structure.
 Q5. Do you have billing accounts using multiple currencies?
 Note: DigitalEx currently does not support mixed currency use cases due to the complexity of converting between currencies based on 
exchange rates.
 Q6. Did you purchase GCP solution directly from Google or through a reseller?
 We appreciate your cooperation in providing this information. It will significantly enhance the onboarding process, ensuring we can provide 
the best possible service.
 357
GCP Account Onboarding Security FAQs
 As part of our commitment to a smooth and secure onboarding process, we've prepared the following FAQs to help address any queries you 
might have about GCP account onboarding with DigitalEx.
 Q1. What is the process for onboarding an GCP account with DigitalEx?
 In GCP, there are two main types of organization entities:
 Billing Account
 Projects
 In DigitalEx, the Billing Account is onboarded as a billing account and Projects as usage accounts. These can be onboarded either using 
GCP Cloud shell templates or manually with a step-by-step guide.
 Q2. What is a billing account and why does DigitalEx need it?
 In DigitalEx, a "billing account" refers to the GCP Billing Account. It provides access to cost data, allowing the DigitalEx platform to perform 
analysis, waste identification, budget management, and more.
 Q3. What is a usage account and why does DigitalEx need it?
 A "usage account," a term used by DigitalEx, refers to GCP Projects. We recommend onboarding all of them as usage accounts in DigitalEx. 
This allows real-time resource inventory across all your accounts, cost analysis of resources over time, identification of unused resources, 
and more.
 Q4. How do I access the guide for onboarding my billing account?
 The guide for onboarding your billing account is available at this link: GCP Billing Account Onboarding Guide
 Q5 How do I access the guide for onboarding my usage account?
 The guide for onboarding your usage account can be found at this link: GCP Usage Account Onboarding Guide
 Q6. Is it secure to onboard my GCP account with DigitalEx? If so, why?
 Yes, DigitalEx has implemented strict measures to ensure the security of your account and data. We use Service accounts for access and 
grant our export only the minimum required read-only permissions. The service account  JSON are securely stored in a vault. For billing 
accounts, DigitalEx has read access only at the BigQuery dataset where cost exports are stored. For usage accounts, you can create a 
custom role with specific read permissions for asset tracking.
 Q7: How does GCP CLI onboarding for billing accounts work?
 Using GCP cloudshell for onboarding can improve efficiency and reduce the risk of mistakes. When you execute the onboarding command, 
the system will:
 Display a list of accessible projects for you to select the one, where are exports are stored.
 Check for cloud billing export to BigQuery enabled?
 Create a new IAM Role & Service account and grant it read-only access to the BigQuery dataset where the cost export is stored.
 Your understanding and cooperation will significantly improve the onboarding process, ensuring we can provide the best possible service.
 358
359
GCP Troubleshooting
 Select Organization Scope. 
In GCP Console, select the scope dropdown located in the top left navbar, next to Google Cloud logo. 
Choose “ALL” tab. 
Choose the top organization. 
Adding whitelist to Organization Policy. 
Go to “IAM and admin” 
From the left side menu, choose “Organization policies.” 
360
Search for: “Domain restricted sharing”, click on it. 
Click on “Manage Policy” 
361
Under “Rules”, 
you will see one of the existing rules, please expand it 
Under “Custom values”, there could be some existing values. 
Click “ADD VALUE”, and add following value without quotes: “principalSet://iam.googleapis.com/organizations/635452545508” 
Click on “SET POLICY” 
VPC Service Controls. 
Go to “Manage VPC Service Controls” 
Select the access policy. 
Select perimeter item (which is blocking access to services like cloud asset & storage) 
Click “EDIT” on the “Ingress policy” section. 
Add a new rule using “ADD RULE” 
For “FROM attributes of the API client”: 
For “Identity”, choose “Selected identities”, add service account id (To obtain the service account ID, please follow these steps 
e the Service Account Id )
 For “Source”, choose “All Sources.” 
For “TO attributes of GCP services/resources”: 
For “Project”, choose “All projects.” 
For “All services”, choose “All services.” 
Click on “SAVE”
'''

AccountManagementForICAgent = '''AWS STEPS -
Account Management for Indirect Customers
 Definition
 Partner is a DigitalEx’s partner with capability to onboard and manage their own customers.
 Target /End Customer is a customer created and managed by partner whose cloud accounts are onboarded in DigitalEx.
 Why Account Management for Indirect Customers?
 Partners and Target/End customers might not have the required permissions to perform essential actions, potentially causing a disconnect 
between partner firms and their target or end customers. To address this, we are introducing account management for Indirect Customers.
 How Account Management for Indirect Customers works
 Target /End Customer initiates the process by logging into their cloud provider's system. Following this, a series of steps are undertaken to 
prepare the Onboarding credentials for partner’s access to view their cost and resources for Due diligence. After completion of these steps, 
the Target Company generates and shares the necessary credentials with Partner
 The shared credentials facilitate Partner’s access to view their cost and resources, allowing them to onboard the Target Company's cloud 
account to the DigitalEx platform. This crucial onboarding process ensures seamless integration and operational functionality between the 
Target Company, Partner Company, and the DigitalEx platform."
 <<Previous ---------------------------------------------------------------------------------------------------------- Next>> 
429
AWS (Amazon Web Services)
 DigitalEx allows users to onboard AWS Billing and Usage Accounts. This process involves setting up the necessary accounts and 
permissions, configuring the billing and cost management settings, and integrating the billing data with DigitalEx. Onboarding the AWS 
billing account with DigitalEx allows users to track and manage their AWS costs and usage, and to optimize their use of AWS resources to 
reduce costs. It is important to carefully follow the steps in the onboarding process to ensure that the AWS billing account is set up correctly 
and able to accurately track and report on costs.
 Billing Account
 The billing account in an AWS organization is the management account that is used to manage the AWS accounts and pay for charges that 
are incurred by the member accounts. This account has the responsibilities of a payer account and cannot be changed, as it is the 
organization's management account. It is important to properly set up and manage the billing account in an AWS organization to ensure that 
charges are accurately tracked and paid in a timely manner.
 Usage Account
 A usage account in an AWS organization is a member account, which is any account that is not the management account. Member 
accounts make up all of the other accounts in the organization and can only be a member of one organization at a time. Policies can be 
attached to a usage account to apply controls specifically to that account. It is important to properly set up and manage member accounts in 
an AWS organization to ensure that resources are used effectively and in accordance with organizational policies and controls.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
430
AWS Biling Account Onboarding.
 There are 3 ways to onboard AWS Billing accounts.
 1. AWS Billing Manual UI Onboarding
 [UI]  AWS Billing Account Manual Onboarding 
2. AWS Billing Manual CLI Onboarding
 [CLI]  AWS Billing Account Manual Onboarding 
3. AWS Billing Automated Onboarding
 [Automation] AWS Billing Account Onboarding 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
431
[UI]  AWS Biling Account Manual Onboarding
 The process of manually onboarding AWS Billing accounts via the AWS Console involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1.
 [UI] AWS Billing Account Onboarding for Target 
2. 
AWS Connect Billing Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
432
[UI] AWS Biling Account Onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the AWS portal. Kindly access the AWS 
portal and adhere to the prescribed steps.
 To carry out below steps, Tenant ID is required. Please consult your partner company to share tenant id before moving forward.
 Step-1 : Enable CUR & Cost Explorer
 Step-2 : Enable Cost Allocation Tags
 Step-3 : Create Role / IAM User
 Step-4 : Retrieve AWS Billing Account ID.
 Step-5: Capture the details to onboard AWS account---------------------------------------------------------------------------------------------------------- Next>> 
433
Step-1 : Enable CUR & Cost Explorer
 If you have cost and usage reports already created follow Use already created report otherwise Create new report
 Use already created report
 1. Log into AWS Console and go to Billing service
 2. On the billing page, look for Cost & Usage Reports section
 3. Out of multiple available reports, choose the oldest and the one having following properties
 a. Time granularity : Daily / Hourly
 b. File format : text/csv
 4. Capture the S3 bucket, Report path prefix fields from the report details section for the report you chose in the previous step
 434
5. Go to 
Step-2 : Enable Cost Allocation Tags 
Creating New Report
 1. Log into AWS Console and go to Billing service
 2. On the billing page, select Cost & Usage Reports section from the sidebar and click Create Report
 3. Give the name of your choice and enable both
 a. Include Resource IDs
 b. Automatically refresh your Cost & Usage Report when charges are detected for previous months with closed bills
 435
4. Click Next
 a. configure bucket by choosing one of the existing or creating a new one
 b. set following properties
 i. Time granularity : Daily
 ii. Report versioning : overwrite existing report
 iii. Compression type : GZIP
 5. Click Next -> Review and complete
 436
6. Click on the Report created and Capture Bucket Name, Report Path.
 7. To enable cost explorer follow the steps mentioned here Enabling Cost Explorer - AWS Cost Management
 AWS takes up to 24 hours to create first report to the configured bucket.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
437
Step-2 : Enable Cost Alocation Tags
 Below are the steps to Enable Cost Allocation Tags:
 1. Log into AWS Console and go to Billing from the Services tab.
 2. On the Billing page, click on Cost Allocation Tags
 3. Click on AWS Generated cost Allocation tags.
 438
4. Select the tags you want to use as dimensions for grouping and filtering cost data and click on Activate to activate them.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
439
Step-3 : Create Role / IAM User
 To carry out role-based steps, a Tenant ID is required. Please consult your partner company to share tenant id before moving 
forward.
 DigitalEx supports both types of AWS authentications,
 1. Role Based
 2. Access/Secret Key Based
 Role-based access is generally considered to be more secure than user-based access, as it allows organizations to control access to 
resources and functions based on defined roles and responsibilities. We recommend using roles over individual users whenever possible
 Creating Role
 1. Go to IAM from the Services tab.
 2. Click on Roles from the left menu options and Click on 
Create Role
 3. Select 
AWS Accounts and select 
Another AWS Account from 
an AWS Account  tab
 440
a. specify 
Account ID as 
911403356698 (This is the Account Id of DigitalEx which is universal)
 b. Check on options 
Require external ID and enter the tenant id(Please ask your partner to share tenant-id)
 4. Click 
Next , don’t select any permissions
 5. Click 
Next
 6. Enter the Role Name of your choice and Click Create Role.
 7. New Role should be created and displayed in the list.
 441
8. Click on the newly created Role which is navigated to the below page
 9. Click on 
Add Permissions -> Create Inline Policy under 
Permissions Tab & Click on 
following JSON
 a. JSON
 1 { 
2   
3    
4        
5            
6            
7                
8                
9            
10            
11                
12                
13            
"Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Action": [
 "s3:GetObject",
 "s3:ListBucket"
 ],
 "Resource": [
 JSON tab & replace existing JSON with the 
"arn:aws:s3:::<BUCKET_NAME>",
 "arn:aws:s3:::<BUCKET_NAME>/*"
 ]
 442
443
 b. And replace <BUCKET_NAME> on lines 11 & 12 with the name of the bucket captured in Step-1 : Enable CUR & Cost Explorer 
c. Finally, your window should look like the following image. Note that, the bucket name in the image is for reference, it shouldn’t be 
copied as is, instead you should put your own bucket name
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31        },
 32        {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:GenerateCredentialReport",
 36                "iam:GenerateServiceLastAccessedDetails",
 37                "iam:Get*",
 38                "iam:List*",
 39                "iam:SimulateCustomPolicy",
 40                "iam:SimulatePrincipalPolicy"
 41            ],
 42            "Resource": "*"
 43        },
 44        {
 45     "Effect": "Allow",
 46     "Action": [
 47                "cur:Get*",
 48                "cur:ValidateReportDestination",
 49                "cur:Describe*"
 50      ],
 51     "Resource": "*"
 52 }
 53    ]
 54 }
10. Review Policy, Name it & Click 
11. Capture 
Create policy
 ARN of the role we created from the summary section for the next steps.
 444
Creating IAM User & Access/Secret Keys
 This step is not required if you have created a Role.
 1. Go to IAM from the Services tab & navigate to Users tab
 2. Click Add Users, enter name of your choice 
3. Skip permissions for now. Keep doing Next & finally Create User.
 4. Open the User you have created & click on Security credentials.
 445
5. Scroll down & click on Create access key
 6. Select Others  & click on next
 7. Click on Create Access Key 
8. Save Access key ID and Secret access key for later use. 
446
447
 9. Click Done
 10. Navigate to the details of the user we just created
 1. Click Add Inline Policy under Permissions Tab & Click on JSON tab & replace existing JSON with the following JSON
 a. JSON
 1 { 
2   "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31        },
 32        {
 33            "Effect": "Allow",
34            
35                
36                
37                
38                
39                
40                
41            
42            
43        
44        
45     
46     
47                
48                
49                
50      
51     
52 }
 53    
54 }
 b. And replace 
"Action": [
 "iam:GenerateCredentialReport",
 "iam:GenerateServiceLastAccessedDetails",
 "iam:Get*",
 "iam:List*",
 "iam:SimulateCustomPolicy",
 "iam:SimulatePrincipalPolicy"
 ],
 "Resource": "*"
 },
 {
 "Effect": "Allow",
 "Action": [
 ],
 "cur:Get*",
 "cur:ValidateReportDestination",
 "cur:Describe*"
 "Resource": "*"
 ]
 <BUCKET_NAME> on lines 11 & 12 with the name of the bucket captured in 
Step-1 : Enable CUR & Cost Explorer 
c. Finally, your window should look like the following image. Note that, the bucket name in the image is for reference, it shouldn’t be 
copied as is, instead you should put your own bucket name
 2. Review the policy & click create
 448
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
449
Step-4 : Retrieve AWS Biling Account ID.
 Below are the steps to Retrieve AWS Billing Account ID:
 1. Go to My Account page.
 2. On the My Account page, note the Account Id.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
450
Step-5: Capture the details to onboard AWS account
 Capture below details to share with your partner.
 1. Account ID Retrieve Account ID
 2. Role ARN or Access/Secret Key Retrieve Role ARN or Access/Secret Kay
 3. Bucket Name, Report Path Retrieve Bucket Name, Report Path
 <<Previous  ---------------------------------------------------------------------------------------------------------- 
451
[CLI]  AWS Biling Account Manual Onboarding
 The process of manually onboarding AWS Billing accounts via the AWS CLI interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1.
 [CLI] AWS Billing Account Onboarding for Target 
2.
 AWS Connect Billing Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
452
453
 [CLI] AWS Billing Account Onboarding for Target
 The Target Company is required to implement the following steps within the AWS Cloud Shell. Please sign in to the AWS console 
using the Admin account where billing has been set up, and then initiate the Cloud Shell from the navigation bar.
 Step-1:  Configure Cost Export
 1. Use existing report
 a. Check if the cost report exists with Time granularity : Daily / Hourly and File format : text/csv
 If above command returns only one cost record then capture S3Bucket, S3Prefix and Report Name
 If above command returns more than one report then choose oldest record from UI.
 Log into AWS Console and go to Billing service
 On the billing page, look for Cost & Usage Reports section
 Out of multiple available reports, choose the oldest and the one having following properties
 a. Time granularity : Daily / Hourly
 b. File format : text/csv
 Capture the S3 bucket, Report path prefix fields from the report details section for the report you
 2. Creating new report (This step is not required if you have a exiting report)
 a. Create new S3 bucket by entering <S3BucketName> (Skip this step if you want to use exiting S3 bucket)
 b. Apply policy to S3 bucket by entering <S3BucketName> and AWS billing account id (To get Tenant id execute this command : aws 
sts get-caller-identity --query Account --output text
 To carry out below steps, Tenant ID is required. Please consult your partner company to share tenant id before moving forward.
 1 aws cur --region us-east-1 describe-report-definitions --max-items 5 --query "ReportDefinitions[?
 TimeUnit=='DAILY'||TimeUnit=='HOURLY' && Format=='textORcsv'].{ReportName:ReportName, S3Bucket: S3Bucket, 
S3Prefix: S3Prefix}"
 1 aws s3 mb s3://<S3BucketName>
 1 aws s3api put-bucket-policy --bucket <S3BucketName> --policy '{
 2  "Statement": [
 3    {
 4      "Effect": "Allow",
 5      "Principal": {
 6        "Service": "billingreports.amazonaws.com"
 7      },
 8      "Action": [
 9        "s3:GetBucketAcl",
 10        "s3:GetBucketPolicy"
 11      ],
 12      "Resource": "arn:aws:s3:::<S3BucketName>",
 13      "Condition": {
 14        "StringEquals": {
 15          "aws:SourceArn": "arn:aws:cur:us-east-1:<AccountId>:definition/*",
 16          "aws:SourceAccount": "<AccountId>"
 17        }
 18      }
 19    },
 20    {
454
 c. Create new cost and usage report by entering <ReportName> of your choice, <S3BucketName> & <S3BucketPrefix> 
created/caputured in above steps 
Step-2: Enable Cost Allocation Tags
 1. List cost allocation tags and capture the tags you want to use as dimensions for grouping and filtering cost data.
 2.  Active cost allocation tags which you want from above tags by entering <"TagValue">
 Step-3: Create Role / IAM User
 1. Role Based 
21      "Sid": "Stmt1335892526596",
 22      "Effect": "Allow",
 23      "Principal": {
 24        "Service": "billingreports.amazonaws.com"
 25      },
 26      "Action": "s3:PutObject",
 27      "Resource": "arn:aws:s3:::<S3BucketName>/*",
 28      "Condition": {
 29        "StringEquals": {
 30          "aws:SourceArn": "arn:aws:cur:us-east-1:<AccountId>:definition/*",
 31          "aws:SourceAccount": "<AccountId>"
 32        }
 33      }
 34    }
 35  ]
 36 }'
 1 aws cur put-report-definition --region us-east-1 --report-definition '{
 2    "ReportName": "<ReportName>",
 3    "TimeUnit": "DAILY",
 4    "Format": "textORcsv",
 5    "Compression": "GZIP",
 6    "AdditionalSchemaElements": [
 7      "RESOURCES"
 8    ],
 9    "S3Bucket": "<S3BucketName>",
 10    "S3Prefix": "<S3BucketPrefix>",
 11    "S3Region": "us-east-1",
 12    "AdditionalArtifacts": [],
 13    "RefreshClosedReports": true,
 14    "ReportVersioning": "OVERWRITE_REPORT"
 15  }'
 AWS takes up to 24 hours to create first report to the configured bucket
 1 aws ce list-cost-allocation-tags
 1 aws ce update-cost-allocation-tags-status --cost-allocation-tags-status TagKey=<"TagValue">,Status=Active 
TagKey=<"TagValue">,Status=Active
455
 Role-based access is generally considered to be more secure than user-based access, as it allows organizations to control access to 
resources and functions based on defined roles and responsibilities. We recommend using roles over individual users whenever 
possible.
 a. Create Role by Entering RoleName of your choice and tenantid(provided by your partner) and capture role ARN from output
 b. Update role policy by entering <RoleName> created above, <PolicyName> of your choice. Enter <S3BucketName> captured from 
Step-1 while configuring Cost report
 1 aws iam create-role --role-name <RoleName> --assume-role-policy-document '{
 2    "Version": "2012-10-17",
 3    "Statement": [
 4      {
 5        "Effect": "Allow",
 6        "Principal": {
 7          "AWS": "arn:aws:iam::911403356698:root"
 8        },
 9        "Action": "sts:AssumeRole",
 10        "Condition": {
 11          "StringEquals": {
 12            "sts:ExternalId": "<tenantid>"
 13          }
 14        }
 15      }
 16    ]
 17  }'
 1 aws iam put-role-policy --role-name <RoleName> --policy-name <PolicyName>  --policy-document '{
 2  "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
 29            ],
 30            "Resource": "*"
 31            },
 32            {
456
 2. Access/Secret Key Based (This step is not required if you have created a Role)
 a. Create User by Entering <UserName> of your choice
 b. Update user policy by Entering <UserName> created above,Enter <PolicyName> of your choice. Enter <S3BucketName> captured 
from Step-1 while configuring Cost report
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:GenerateCredentialReport",
 36                "iam:GenerateServiceLastAccessedDetails",
 37                "iam:Get*",
 38                "iam:List*",
 39                "iam:SimulateCustomPolicy",
 40                "iam:SimulatePrincipalPolicy"
 41            ],
 42            "Resource": "*"
 43        }
 44        {
 45     "Effect": "Allow",
 46     "Action": [
 47                "cur:Get*",
 48                "cur:ValidateReportDestination",
 49                "cur:Describe*"
 50      ],
 51     "Resource": "*"
 52 }
 53    ]
 54 }'
 1 aws iam create-user --user-name <UserName>
 1 aws iam put-role-policy --role-name <RoleName> --policy-name <PolicyName>  --policy-document '{
 2  "Version": "2012-10-17",
 3    "Statement": [
 4        {
 5            "Effect": "Allow",
 6            "Action": [
 7                "s3:GetObject",
 8                "s3:ListBucket"
 9            ],
 10            "Resource": [
 11                "arn:aws:s3:::<BUCKET_NAME>",
 12                "arn:aws:s3:::<BUCKET_NAME>/*"
 13            ]
 14        },
 15        {
 16            "Effect": "Allow",
 17            "Action": [
 18                "organizations:ListAccounts",
 19                "organizations:DescribeAccount"
 20            ],
 21            "Resource": "*"
 22        },
 23        {
 24            "Effect": "Allow",
 25            "Action": [
 26                "ce:Get*",
 27                "ce:Desc*",
 28                "ce:List*"
457
 c. Create AccessKey and SecretAccessKey
 Step-4: Get Account ID 
1. Get your Account ID
 Step-5: Capture the below details from the above steps and share with your partner.
 1. Account ID
 2. Role ARN or Access/Secret Key
 3. Bucket Name
 4. Report Path Prefix
 
29            ],
 30            "Resource": "*"
 31            },
 32            {
 33            "Effect": "Allow",
 34            "Action": [
 35                "iam:GenerateCredentialReport",
 36                "iam:GenerateServiceLastAccessedDetails",
 37                "iam:Get*",
 38                "iam:List*",
 39                "iam:SimulateCustomPolicy",
 40                "iam:SimulatePrincipalPolicy"
 41            ],
 42            "Resource": "*"
 43        }
 44        {
 45     "Effect": "Allow",
 46     "Action": [
 47                "cur:Get*",
 48                "cur:ValidateReportDestination",
 49                "cur:Describe*"
 50      ],
 51     "Resource": "*"
 52 }
 53    ]
 54 }'
 1 aws iam create-access-key --user-name ${UserName}
 1 aws sts get-caller-identity --query Account --output text
[Automation] AWS Biling Account Onboarding
 The process of automated onboarding AWS Billing accounts via the AWS cloud shell involves below steps: The initial step must 
be carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
3. 
[Automation] AWS Billing Account Onboarding for Target 
AWS Billing Onboarding CloudFormation URL 
AWS Connect Billing Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
458
[Automation] AWS Biling Account Onboarding for Target
 Steps to perform by Target:
 To proceed with the following steps, you'll need a CloudFormation URL. Please consult your partner to obtain the URL.
 In order to run the URL you need to have admin role.
 Upon receiving the link from the partner company, perform below steps 
Login to AWS console where billing account is configured.
 Open the URL in the browser. You will be presented with below screen. 
Click Create at the bottom of page and Wait till the stack creation is completed
 Click on Outputs tab.
 459
Capture the below details and share them with your partner.
 1. Bucket Name
 2. Role ARN
 3. Account ID
 4. Report Path--------------------------------------------------------------------------------------------------------- Next>> 
460
AWS Biling Onboarding CloudFormation URL
 Share the below link with your target company.
 1 https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?
 templateURL=https://digitalex-assets.s3.amazonaws.com/cloudwiz-io/billing/main.yaml&stackName=<STACK
NAME>&param_host=https://api.digitalex.io&param_skipOnboarding=true&param_tenant=<TENANT-ID>
 Replace the <TENANT-ID> & <STACK-NAME>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id  
Replace stack name in below format.
 digitalex-io-billing-onboarding-<url-domain>
 E.g: digitalex-io-billing-onboarding-mindsnxt-cloud-uk
 461
AWS Connect Biling Account for Partner
 To link an account on DigitalEx, you'll require onboarding credentials generated Please reach out to your target company to 
obtain these credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link AWS Connect Billing Account for Partner  to onboard additional providers 
1. Click on AWS Provider
 2. Click on Connect manually
 462
3. Click on Connect Billing Account
 4. Enter the details shared by Target company.
 5. Click on connect & done.
 If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1. Navigate to Menu > Admin > Public Clouds > +Account.
 463
2. Click on AWS Provider & Click on Manual tab
 3. Enter the details shared by Target
 5. The onboarded Management Account will be displayed with the list of All linked Member accounts.
 4. Click Connect
 464
After adding a new account, it may take up to 30 minutes for the system to discover and process the data.
 6. Go to the Menu option and Click Cost.
 7. Data will display immediately after successful ingestion.
 465
The following are the steps you should take if you're unable to view cost data from the previous 13 months
 If the data for previous months isn't visible on cost dashboard due to missing historical Cost and Usage Report (CUR) files, there are a 
couple of solutions to retrieve the data:
 1. Request the missing month's CUR from AWS Support. Ensure to designate the same bucket you used during the onboarding process 
and request them to upload the CUR file into that specific bucket.
 2. Leverage AWS Explorer APIs, which charge based on the usage account. This cost is a one-time fee. If you choose this route, follow the 
steps outlined below.
 Click on Menu > Admin > Public Clouds
 Click on AWS Tab > Edit Icon > Configure
 Enable the Toggle, Click Ok & Done
 Click on Data Ingestion and wait till its completed.
 466
--------------------------------------------------------------------------------------------------------- Next>> 
467
AWS Members Account Onboarding
 There are two ways to onboard AWS Billing accounts.
 1. AWS Member Manual UI Onboarding
 [UI]AWS Member Account Onboarding 
2. AWS Member Automated Onboarding
 [Automation]AWS Members Account Onboarding 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
468
[UI] AWS Member Account Onboarding
 The process of manually onboarding AWS Member accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[UI] AWS Member Account Onboarding for Target 
AWS Connect Member Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
469
[UI] AWS Member Account Onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the AWS portal. Kindly access the AWS 
portal and adhere to the prescribed steps. 
To carry out below steps, a Tenant ID is required. Please consult your partner company to share tenant id before moving forward.
 Step-1: Enable Compute Optimizer
 Step-2 : Create an IAM role for DigitalEx
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
470
Step-1: Enable Compute Optimizer
 This step should be carried out for every individual member account.
 1. Login to your AWS Member account as Administrator
 2. Then search for AWS Compute Optimizer in a search bar & select it. You will land on the home page of Compute Optimizer Service
 3. Click on Get started
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
471
Step-2 : Create an IAM role for DigitalEx
 This steps only provides illustrations on creating a role but a user with access/secret key is also supported. If you wish to create a 
user, please assign similar permissions as documented for a role below. We encourage a use of a Role over a User as its more 
secure.
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Roles from the left menu, and click 
IAM service using 
Create role . One the create role screen please select the 
configuration as follows
 a. Trusted entity type: AWS Account
 b. An AWS account: Choose 
Another AWS account and fill in the account number as 
911403356698
 c. External ID: In this field, Enter the tenant id shared by your partner company.
 d. Finally click 
Next
 472
3. Click 
Next , on next screen for permissions, please choose 'All Types' in the filter and select the listed policies below.
 ReadOnlyAccess
 ViewOnlyAccess
 IAMReadOnlyAccess
 CloudWatchReadOnlyAccess
 ComputeOptimizerReadOnlyAccess
 AWSOrganizationsReadOnlyAccess
 473
4. Click 
Next again & on a final page, give a name to the role & click 
Create role
 5. Open the newly created role 
6. Click on Add permissions → Create inline policy.
 7. Search for Cost Explorer Service
 8. Click on Write → 
StartSavingsPlansPurchaseRecommendationGeneration →
 9. Enter the policy name. 
10. Click on
 Create policy .
 Next
 11. Once the role is created, please note the ARN of a role, which will be required in the next step.
 474
If you still wish to prefer using access/secret access key. Follow below steps
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Users from the left menu
 3. Click on Create User
 4. Enter the Username & click Next.
 IAM service using 
5. Select Attach policies directly, on next screen for permissions, please choose 'All Types' in the filter and select the listed policies below.
 ReadOnlyAccess
 ViewOnlyAccess
 475
IAMReadOnlyAccess
 CloudWatchReadOnlyAccess
 ComputeOptimizerReadOnlyAccess
 AWSOrganizationsReadOnlyAccess
 6. Click 
Next again & on a final page, give a name to the role & click 
Create user
 7. Once the user is created, please click on the user to create a Secret Key
 8. Go to Security Credentials tab & Click on Create Access Key
 9. Select Application running outside AWS & Click on Next
 476
10. Click on Create access key.
 11. Secret Key will get generated.
 12. Copy the Access Key & Secret Key which will be required in the next step.
 13. Open newly created user
 14. Click on Add permissions → Create inline policy.
 15. Search for Cost Explorer Service
 16. Click on Write → 
StartSavingsPlansPurchaseRecommendationGeneration →
 Next
 477
17. Enter the policy name. 
18. Click on
 Create policy .
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
478
[Automation] AWS Members Account Onboarding
 There are 3 steps to onboard AWS Members Account through automation:
 1. 
2. 
3. 
[Automation] AWS Members Account Onboarding for Target 
AWS Member Onboarding CloudFormation URL 
AWS Connect Member Account for Partner 
479
[Automation] AWS Members Account Onboarding for Target
 Steps to perform by Target:
 To proceed with the following steps, you'll need a CloudFormation URL. Please consult your partner to obtain the URL.
 In order to run the URL you need to have admin role.
 Upon receiving the link from the partner company, perform below steps.
 Login to AWS console where member account is configured.
 Open the link in the browser. You will be presented with below screen.
 Click Create at the bottom of page
 Click on Outputs tab, after successful creation of stack.
 Capture your Role ARN and share with your partner company ---------------------------------------------------------------------------------------------------------- Next>> 
480
AWS Member Onboarding CloudFormation URL
 Share the below link with your target company.
 1 https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?
 templateURL=https://digitalex-assets.s3.amazonaws.com/cloudwiz-io/usage/v3/template.yaml&stackName=
 <STACK_NAME>&param_token=<TENANT_ID>
 Replace the <TENANT-ID> & <STACK-NAME>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id 
Replace stack name in below format.
 digitalex-io-usage-onboarding-<url-domain>
 E.g: digitalex-io-usage-onboarding-mindsnxt-cloud-uk
 481
AWS Connect Member Account for Partner
 To link an account on DigitalEx, you'll require onboarding credentials. Please reach out to your target company to obtain these 
credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 Below are the steps to Connect member account:
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 482
4. Below Page will be displayed with the list of All linked Member accounts. 
5. Click on 
Connect , and switch to 
Manual tab, and fill up the details as follows,
 483
a. Role ARN: Fill in the Role ARN captured in last step. Please note if you have chose to create a user instead of a role, check the box 
named Use access / secret keys and fill in related details.
 b. Bucket Name: this parameter takes a list of buckets you used to setup your AWS Config regional service. This can very well be also 
just one bucket in case you used same bucket for all the region.
 c. To get the Account id follow instructions outlined in this page 
Step- 4 : Retrieve AWS Account Id 
6. After filling in all the details, click 
Connect your account should get onboarded successfully.
 The values depicted in the images are merely provided as sample values for the purpose of illustration, and they may vary in your 
specific situation.
 7. On-boarded Member Account will be displayed on the list of member account
 8. Click the Resource from the Menu option.
 484
9. A Resource takes up to 2hrs to discover in DigitalEx and will be displayed as shown below.
 485
---------------------------------------------------------------------------------------------------------- Next>> 
486
Depreciate.
 487
[Automation]AWS Members Account Onboarding
 The process of automatically onboarding AWS Member accounts via the AWS Cloud shell involves 3 steps.
 1. 
2. 
3. 
[Automation] AWS Members Account Onboarding for Target. 
AWS Member Onboarding CloudFormation URL. 
AWS Connect Member Account for Partner. 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
488
[Automation] AWS Members Account Onboarding for Target.
 Steps to perform by Target:
 To proceed with the following steps, you'll need a CloudFormation URL. Please consult your partner to obtain the URL.
 In order to run the URL you need to have admin role.
 Enable Compute Optimizer from AWS Console, by following the instruction provided 
imizer - AWS Compute Optimizer 
Upon receiving the link from the partner company, perform below steps.
 Login to AWS console where member account is configured.
 Open the link in the browser. You will be presented with below screen.
 Getting started with AWS Compute Opt
 Click Create at the bottom of page
 Click on Outputs tab, after successful creation of stack.
 489
Capture the below details and share them with your partner.
 1. Bucket Name
 2. Role ARN---------------------------------------------------------------------------------------------------------- Next>> 
490
AWS Member Onboarding CloudFormation URL.
 Share the below link with your target company.
 1 https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?
 templateURL=https://digitalex-assets.s3.amazonaws.com/cloudwiz-io/usage/v2/template.yaml&stackName=<STACK
NAME>&param_tenant=<TENANT-ID>
 Replace the <TENANT-ID> & <STACK-NAME>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id 
Replace stack name in below format.
 digitalex-io-usage-onboarding-<url-domain>
 E.g: digitalex-io-usage-onboarding-mindsnxt-cloud-uk
 491
[UI]AWS Member Account Onboarding
 The process of manually onboarding AWS Member accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1.
 [UI] AWS Member Account Onboarding for Target. 
2.
 AWS Connect Member Account for Partner. 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
492
[UI] AWS Member Account Onboarding for Target.
 The Target Company is required to execute the subsequent onboarding process through the AWS portal. Kindly access the AWS 
portal and adhere to the prescribed steps. 
To carry out below steps, a Tenant ID is required. Please consult your partner company to share tenant id before moving forward.
 Step-1 : Enable Compute Optimizer
 Step-2 : Enable AWS Config & Setup SNS
 Step-3 : Create an IAM role for DigitalEx
 Step- 4 : Retrieve AWS Account Id
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
493
Step-1 : Enable Compute Optimizer
 This step should be carried out for every individual member account.
 1. Login to your AWS Member account as Administrator 
2. Then search for AWS Compute Optimizer in a search bar & select it. You will land on the home page of Compute Optimizer Service 
3. Click on Get started 
494
Step-2 : Enable AWS Config & Setup SNS
 This step has to be performed for every region you want to onboard to DigitalEx.
 1. Login to your AWS Member account as Administrator and switch to a region you want to onboard.
 2. Then search for 
Config service in a search bar & select it. You will land on the home page of config service
 4. Select 
Get started option and on the next page choose following settings,
 495
a. General settings
 i. Recording strategy : Record all current and future resource types supported in this region
 ii. Include globally recorded resource types : Yes (please select the check box)
 iii. AWS Config role : Use an existing AWS Config service-linked role
 b. Delivery method
 i. Amazon S3 bucket : Either select an option to create a new bucket or choose one of the existing buckets. Please make a note of 
the bucket, it will be needed in some of the following steps.
 ii. Amazon SNS topic (please select a check box):
 1. Amazon SNS topic : Create a new topic
 2. SNS topic name : config-topic
 5. After selecting all the options as suggested, Click 
Next → 
Next & 
6. Once 
Confirm
 AWS Config is setup, navigate to `Simple Notification Service` using a search bar and select 
Topics from the sidebar. You will 
see the topic named config-topic created as part of AWS Config setup in last step
 7. Select the config-topic subscription to navigate to its details. On the details page, click 
Create subcription and select following 
configuration.
 a. Protocol : HTTPS
 b. Endpoint : 
496
1 https://webhook.digitalex.io/<TENANT-ID>/aws/ingest
 Use above URL as an Endpoint. Please note that 
<TENANT-ID> part in the URL has to be replaced with your own tenant id. Please 
consult your partner company to share tenant id before moving forward.
 c. After filling all the required fields, click 
Create subscription
 8. Navigate back to the SNS home page & select 
Subscriptions from left menu this time, & you will see the newly created subscription. 
Please note that a subscription might take 2-3 minutes before it shows 
Confirmed .
 497
9. Please repeat this Enable Config & Setup SNS section for every region you want DigitalEx to discover resources from and keep noting 
down the s3 bucket names used for configuring the delivery method during AWS Config setup.
 498
Step-3 : Create an IAM role for DigitalEx
 This step only provides illustrations on creating a role but a user with access/secret key is also supported. If you wish to create a 
user, please assign similar permissions as documented for a role below. We encourage a use of a Role over a User as its more 
secure.
 1. Login to AWS Member account you’re trying to onboard as an Administrator if not already logged in. And navigate to 
AWS search bar.
 2. On a 
IAM Console, Select 
Roles from the left menu, and click 
IAM service using 
Create role . One the create role screen please select the 
configuration as follows,
 a. Trusted entity type: AWS Account
 b. An AWS account: Choose 
Another AWS account and fill in the account number as 
911403356698
 Next
 c. External ID: In this field, please put the Tenant ID for your DigitalEx account. Please consult your partner company to share tenant id 
before moving forward.
 d. Finally click 
499
e. Click 
Next , on next screen for permissions, please select the aws managed policy called 
ReadOnlyAccess
 500
f. Click 
Next again & on a final page, give a name to the role & click 
Create role
 g. Once the role is created, please note the ARN of a role, which will be required in the next step.
 501
Step- 4 : Retrieve AWS Account Id
 Below are the steps to Retrieve AWS Account Id:
 1. Go to the My Account page.
 2. On the My Account page, note the Account Id. 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
502
AWS Connect Member Account for Partner.
 To link an account on DigitalEx, you'll require onboarding credentials. Please reach out to your target company to obtain these 
credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 Below are the steps to Connect member account:
 1. Login to DigitalEx
 2. Click on Menu Icon at the top left corner 
3. Click on Public Clouds under Admin
 503
4. Below Page will be displayed with the list of All linked Member accounts. 
5. Click on 
Connect , and switch to 
Manual tab, and fill up the details as follows,
 504
a. Role ARN: Fill in the Role ARN captured in last step. Please note if you have chose to create a user instead of a role, check the box 
named Use access / secret keys and fill in related details.
 b. Bucket Name: this parameter takes a list of buckets you used to setup your AWS Config regional service. This can very well be also 
just one bucket in case you used same bucket for all the region.
 c. To get the Account id follow instructions outlined in this page 
Step- 4 : Retrieve AWS Account Id 
6. After filling in all the details, click 
Connect your account should get onboarded successfully.
 The values depicted in the images are merely provided as sample values for the purpose of illustration, and they may vary in your 
specific situation.
 7.. On-boarded Member Account will be displayed on the list of member account
 8. Click the Resource from the Menu option.
 505
9. A Resource takes up to 2hrs to discover in DigitalEx and will be displayed as shown below.

AZURE STEPS -
Microsoft  Azure
 DigitalEx enables users to onboard their Azure billing account. This process involves setting up the necessary accounts and permissions, 
configuring the billing and cost management settings, and integrating the billing data with DigitalEx. Onboarding the Azure billing account 
with DigitalEx allows users to track and manage their Azure costs and usage, and to optimize their use of Azure resources to reduce costs. 
It is important to carefully follow the steps in the onboarding process to ensure that the Azure billing account is set up correctly and able to 
accurately track and report on costs.
 Billing Account
 The billing accounts feature in DigitalEx allows users to view the cost of resources from their Azure accounts and regions in a single 
interface. With this feature, users can search and view the cost of resources across all regions and all accounts and see where resources 
are located. The cost dashboard provides a snapshot of costs, enabling users to quickly understand overall trends and gain visibility into 
their spending across all their public and private cloud providers. This feature can be helpful for organizations looking to optimize their Azure 
usage and reduce costs.
 DigitalEx supports three different types of accounts:
 1. Customer Agreement billing account: This billing account is managed by the organization itself, and the billing ID is used in the billing 
level scope for onboarding.
 2. Partner Agreement billing account: This billing account is managed by a third-party seller and the end user has subscription level access. 
Users can onboard both the billing and subscription levels.
 3. Direct Enterprise Agreement customers: This account is similar to a direct Customer Agreement billing account.
 These different account types allow DigitalEx to support a variety of billing and payment arrangements, and to provide users with the tools 
and features they need to manage their cloud resources and costs effectively.
 Usage Account
 A usage account in an Azure organization is a subscription account, which is any account that is not the management account. Policies can 
be attached to a usage account to apply controls specifically to that account. It is important to properly set up and manage subscription 
accounts in an Azure organization to ensure that resources are used effectively and in accordance with organizational policies and controls.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
508
Microsoft Azure Bi ling Account Onboarding
 There are 3 ways to onboard Azure Billing account:
 1. Azure Billing Manual UI Onboarding
 [UI]  Azure Billing Account Manual Onboarding 
2. Azure Billing Manual CLI Onboarding
 [CLI]  Azure Billing Account Manual Onboarding
 3. Azure Billing Automated Onboarding
 [Automation] Azure Billing Account Onboarding 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
509
[UI]  Azure Biling Account Manual Onboarding
 The process of manually onboarding Azure Billing accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1.
 [UI] Azure Billing Account Onboarding for Target 
2.
 Azure Connect Billing Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
510
[UI] Azure Bi ling Account Onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the Azure portal. Kindly access the 
Azure portal and adhere to the prescribed steps
 Step -1 : Create Azure Active Directory app
 Step -2: Assign permissions to the app
 Step -3 : Retrieve Account ID
 Step -4 : Capture the details to onboard Azure account---------------------------------------------------------------------------------------------------------- Next>> 
511
Step -1 : Create Azure Active Directory app
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Click on Menu
 2. Go to Azure Active directory 
3. Click on App Registration 
512
4. Click on New Registration 
5. Enter Name of Application
 6. Supported account type is selected automatically.
 7. Click on Register 
513
8. App will get created as shown below.
 Capture the Application ID & Directory ID to share with your partner
 Steps to add client’s secret
 1. Click on Certificates & Secrets 
2. Click on New Client Secret 
514
3. Enter Description
 4. Select Expires as 24 months maximum
 5. Click Add
 6. Applied client secret will be displayed as shown below 
515
Capture the Value(not Secret ID) to share with your partner
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
516
Step -2: Assign permissions to the app
 In order to grant permissions to an app, the owner role is required.
 If you choose to onboard the Billing Account , you will need to add the Billing Account Reader role, but if you choose to onboard the 
Subscription as Billing Account , you must add the Cost Management Reader role.
 Assign permission as Billing Account
 1. Click on Menu 
2. Go to Cost Management + Billing
 3. Click on Access Control (IAM) which is under left menu
 4. Click on Add (Add role assignment page will get opened)
 5. Select the Billing account reader
 6. Search the App created in Step 1
 7. Click on Add Button
 517
Assign permission to the app if onboarding subscription as Billing Account
 1. Perform a search within the search box to locate subscriptions and then proceed to open it.
 2. Select the subscription to which you wish to assign permissions.
 3.  Click on Access Control (IAM) which is under left menu
 4. Click on Add (Add role assignment page will get opened
 518
5. Search & Select Cost Management Reader 
6. Click on Next
 7. Click on +Select members.
 8. Search & Select the App created in Step 1
 9. Click on Select Button
 10. Click on Next
 11. Click on Review+assign
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
519
520
Step -3 : Retrieve Account ID
 Steps to Retrieve Account ID:
 1. Click on Menu
 2. Click on Cost Management + Billing.
 4. Click on Properties
 5. Copy the Account ID
 521
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
522
Step -4 : Capture the details to onboard Azure account
 Capture below details to share with your partner.
 1. Billing Account ID Retrieve Account Id 
2. Tenant ID Retrieve Tenant Id
 3. Client ID Retrieve Client ID
 4. Client Secret Retrieve Client Secret 
<<Previous  ----------------------------------------------------------------------------------------------------------  
523
[CLI]  Azure Biling Account Manual Onboarding
 There are two steps to onboard Azure Billing accounts manually through CLI:
 1.
 [CLI] Azure Billing Account Onboarding for Target 
2.
 Azure Connect Billing Account for Partner 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
524
[CLI] Azure Bi ling Account Onboarding for Target
 The Target Company is required to implement the following steps within the Azure Cloud Shell. Please sign in to the Azure 
console using the Admin account where billing has been set up, and then initiate the Cloud Shell from the navigation bar.
 To create the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can have both the 
Contributor and User Access Administrator role.
 Step-1:  Create AD Application
 Execute the following command to create AD App
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME> : AD app name of your choice
 After executing the command, capture the App id, Password(secret) & Tenant to share with the partner.
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Step-2:  Assign permission to the app
 If you are onboarding billing scope as billing Follow the below steps for assigning permission to the app   
a. Login to Azure console > Click on Menu > Cost Management + Billing > Access Control (IAM)
 b. Click Add > Select the Billing account reader > Enter the app created in Step-1 above. 
Follow this link to get detailed steps  
Step -2: Assign permissions to the app  
If you are onboarding subscription scope as billing. Execute the following command to assign permission to the app.
 1 az role assignment create --assignee "<APP_ID>" --role "Cost Management Reader" --scope 
/subscriptions/<SUBSCRIPTION_ID>
 <APP-ID> : AD app id captured in Step-1
 <SUBSCRIPTION_ID> : Your subscription id you wish to onboard
 Step-3:  Capture the below details from the above steps and share them with your partner.
 1. Account ID: Follow this to get Acc id Retrieve Account ID  (This is required if you are onboarding Billing scope)
 2. Application (Client) ID
 3. Active Directory (Tenant) ID
 4. Application (Client) Secret
 5. Subscription Id
 525
[Automation] Azure Bi ling Account Onboarding
 There are 3 steps to onboard Azure Billing accounts through automation:
 1. 
2. 
3. 
[Automation] Azure Billing Account Onboarding for Target 
Azure Billing Onboarding Command 
Azure Connect Billing Account for Partner 
526
[Automation] Azure Bi ling Account Onboarding for Target
 Steps to perform by Target:
 To create the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can have both the 
Contributor and User Access Administrator roles.
 To proceed with the following steps, you'll need a command. Please consult your partner to obtain the command
 Upon receiving the command from the partner company, please execute in the azure cloud shell.
 After execution you need to share the creds with your partner company
 Capture the below details and share them with your partner.
 1. Account ID
 2. Tenant ID
 3. App ID
 4. Client Secret------------------------------------------------------------------------------------------------------ Next>> 
527
Azure Biling Onboarding Command
 Share the below command with your target company.
 1 curl -sO "https://storage.googleapis.com/cloudwiz-io-assets/azure-onboarding.pyz" && python3 azure
onboarding.pyz onboard-billing-account <TENANT-ID>
 Replace the <TENANT-ID>    
To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id 
528
Azure Connect Biling Account for Partner
 To link an account on DigitalEx, you'll require onboarding credentials. Please reach out to your target company to obtain these 
credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link Azure Connect Billing Account for Partner to onboard additional providers.
 1. Click on Azure Provider
 2. Click on Connect manually.
 529
3. Enter the details shared by Target company.
 4. Click on connect & done.
 If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1.  Otherwise, you can navigate to Menu > Admin > Public Clouds > +Account
 2. Select Azure Provider & Click on Manual tab
 530
3. Enter the details shared by Target.
 4. Click Connect
 5. The onboarded Billing Account will be displayed with the list of All linked Member accounts.
 531
After adding a new account, it may take up to 30 minutes for the system to discover and process the data.
 6. Go to the Menu option and Click Cost.
 7. Data will display immediately after successful ingestion.--------
532
Microsoft Azure Subscriptions Account Onboarding
 There are 3 ways to onboard Azure Billing account:
 1. Azure Subscriptions Manual UI Onboarding
 [UI] Azure Subscriptions Account Manual Onboarding 
2. Azure Subscriptions Manual CLI Onboarding
 [CLI] Azure Subscriptions Account Manual Onboarding 
3. Azure Subscriptions Automated Onboarding
 [Automation] Azure Subscriptions Account Onboarding 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
533
[UI] Azure Subscriptions Account Manual Onboarding
 The process of manually onboarding Azure Subscriptions accounts via the user interface involves two steps: The initial step must 
be carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[UI] Azure Subscriptions Account Onboarding for Target 
Azure Connect Subscriptions Account for Partner 
534
[UI] Azure Subscriptions Account Onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the Azure portal. Kindly access the 
Azure portal and adhere to the prescribed steps.
 Step-1: Create Azure Active Directory app.
 Step-2: Assign Permissions to an app.
 Step-3: Capture the details to onboard Azure Subscriptions account.---------------------------------------------------------------------------------------------------------- Next>> 
535
Step-1: Create Azure Active Directory app.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Steps to Create an Application
 1. Click on Menu
 2. Go to Azure Active directory
 3. Click on App Registration 
536
4. Click on New Registration 
5. Enter Name of Application
 6. Supported account type is selected automatically.
 7. Click on Register
 537
8. App will get created as shown below.
 Capture the Application ID & Directory ID to share with your partner
 Steps to add client secret
 1. Click on Certificates & Secrets
 538
2. Click on New Client Secret 
3. Enter Description
 4. Select Expires as 24 months maximum
 5. Click Add
 6. Applied client secret will be displayed as shown below
 539
Capture the Value(not Secret ID) to share with your partner
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
540
Step-2: Assign Permissions to an app.
 In order to grant permissions to an app, the owner role is required.
 1. Click on Subscriptions
 2. Click on your subscription.
 3. Click on Access Control (IAM)
 4. Click on Add → Add role assignment.
 541
5. Click on the search box & enter the role name as Reader role
 6. Select the role & click next 
7. Click on Select Members
 542
8. Enter the App name (which you have created in 
Step-1 : Create Azure Active Directory app ) & Click Select
 9. Click Next 
543
10. Click Review + assign
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
544
Step-3: Capture the details to onboard Azure Subscriptions account.
 Capture below details to share with your partner.
 1. Active Directory (Tenant) ID Retrieve Azure Active Directory app. 
2. Application (Client) ID Retrieve Azure Active Directory app. 
3. Application (Client) Secret Retrieve Azure Active Directory app. 
<<Previous  ---------------------------------------------------------------------------------------------------------- 
545
[CLI] Azure Subscriptions Account Manual Onboarding
 The process of manually onboarding Azure Subscriptions accounts via the user interface involves two steps: The initial step must 
be carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[CLI] Azure Subscriptions Account Onboarding for Target 
Azure Connect Subscriptions Account for Partner 
546
[CLI] Azure Subscriptions Account Onboarding for Target
 The Target is required to implement the following steps within the Azure Cloud Shell. Please sign into the Azure console using the 
admin account where billing has been set up, and then initiate the Cloud Shell from the navigation bar.
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required
 Step-1 : Create AAD & Secret
 1 az ad sp create-for-rbac --display-name "<APP_NAME>" --years=2 -o table
 <APP_NAME> : AD app name of your choice
 After executing the command, capture App Id, Password(Secret) and Tenant id and share it with the partner company
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 Step-2 : Assign Permissions to the App
 1 az role assignment create --assignee "<APP_ID>" --role "Reader" --scope "/subscriptions/<SUBSCRIPTION_ID>" -o 
table
 <APP_ID> : AD app id captured in Step-1
 <SUBSCRIPTION_ID> : Enter your subscription id. Follow this link to capture id 
re portal 
Get subscription and tenant IDs in the Azure portal - Azu
 Capture the below details and share them with your partner.
 1. Active Directory (Tenant) ID
 2. Application (Client) ID
 3. Application (Client) Secret
 547
[Automation] Azure Subscriptions Account Onboarding
 The process of automated onboarding Azure Subscription accounts involves below steps: The initial step must be carried out by 
the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
3. 
[Automation] Azure Subscription Account Onboarding for Target 
Azure Subscription Onboarding Command 
Azure Connect Subscriptions Account for Partner 
548
[Automation] Azure Subscription Account Onboarding for Target
 Steps to perform by Target:
 To manage an Azure Active Directory (AAD) app and create a client secret, the Active Directory administrator role is required.
 To assign permissions to the Azure Active Directory (AAD) app, it is recommended to have the Owner role. Alternatively, you can 
have both the Contributor and User Access Administrator roles.
 To proceed with the following steps, you'll need a command. Please consult your partner to obtain the command
 Upon receiving the command from the partner company, run the command in azure cli
 After successful onboarding of usage account, you need to share the creds with your partner company.
 Capture the below details and share them with your partner.
 1. Subscription ID
 2. Active Directory (Tenant) ID
 3. Application (Client) ID
 4. Application (Client) Secret---------------------------------------------------------------------------------------------------------- Next>> 
549
Azure Subscription Onboarding Command
 Share the below command with your target company.
 1 curl -sO "https://storage.googleapis.com/cloudwiz-io-assets/azure-onboarding.pyz" && python3 azure
onboarding.pyz onboard-usage-account <TENANT-ID>
 Replace the <TENANT-ID>    
To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id 
550
Azure Connect Subscriptions Account for Partner
 To link an account on DigitalEx, you'll require onboarding credentials. Please reach out to your target company to obtain these 
credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 Below are the steps to onboard subscriptions account:
 1. Navigate to Menu > Admin > Public Clouds > Azure.
 2. Click on the Subscriptions tab.
 3. Click on the Connect button of the Subscription you wish to onboard
 551
4. Fill in the following details provided by the Target Company. 
5. Click Connect

GCP STEPS -
GCP (Google Cloud Platform)
 DigitalEx allows users to onboard GCP Billing and Usage Accounts.
 Billing Account
 Billing Accounts enable users to view costs from GCP accounts and regions in a single interface. Users can search and view the costs of 
resources across all regions and accounts, and visualize where resources are located. The Cost dashboard allows users to gain insight into 
their spending across all their public and private cloud providers. It provides a quick snapshot of costs, allowing users to easily understand 
overall trends.
 Usage Account
 A Usage Account is a project in a GCP organization. Projects are all the other accounts in an organization. An account can only be a project 
of one organization at a time
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
553
GCP Biling Account Onboarding.
 There are 3 ways to onboard GCP Billing account 
1. GCP Billing Manual UI Onboarding
 [UI]  GCP Billing Account Manual Onboarding 
2. GCP Billing Manual CLI Onboarding
 [CLI] GCP Billing Account Manual Onboarding 
3. GCP Billing Automated Onboarding
 [Automation] GCP Billing Account Onboarding 
554
[UI]  GCP Biling Account Manual Onboarding
 The process of manually onboarding GCP Billing accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[UI] GCP Billing  Onboarding for Target 
GCP Connect Billing Account for Partner 
555
[UI] GCP Biling  Onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the GCP portal. Kindly access the GCP 
portal and adhere to the prescribed steps.
 To carry out below steps, Service account id & Tenant Id is required. Please consult your partner company to share before moving 
forward.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1 : Enable Billing Export.
 Step-2 : Enable Cloud Resource Manager API.
 Step-3 : Grant permissions at project scope
 Step-4 : Grant permissions at Organization scope
 Step-5 : Retrieve Billing Account Id and Project Id.
 Step-6: Capture the details to onboard GCP account---------------------------------------------------------------------------------------------------------- Next>> 
556
Step-1 : Enable Biling Export.
 If the standard report is already enabled, use the same dataset of the standard report else create a new dataset to be enabled & 
follow the below steps.
 In order to execute the below steps, you need to have owner role.
 Steps to create Dataset and Enable Billing Export
 1. Click on Billing from Dashboard.
 2. Click on Billing Export.
 3. Clicking on Billing export navigates to the below page. Click on Edit settings.
 4. Click on Edit Settings for Detailed usage cost
 5. Clicking on Edit navigates to the below page.
 557
6. Select the project or it automatically gets selected if there is a single project.
 7. Click Create Dataset & click Save. 
8. After saving Detailed usage cost is enabled. (Capture the Dataset name as its used in later steps)
 558
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
559
Step-2 : Enable Cloud Resource Manager API.
 Steps to Enable cloud resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select.
 2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box.
 3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below.
 560
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
561
Step-3 : Grant permissions at project scope
 Prior to proceeding with the following steps, make sure to choose the project from the top dropdown menu that you had previously 
selected in 
Step-1: Enable Billing Export. or if you have an existing export, locate the project where the export is saved and 
choose that project from the top dropdown menu.
 1. Go to IAM
 2. Click on Grant Access
 3. Enter service account id under the new principals.(To get the Service account id follow instructions outlined in this page 
Service Account Id )
 4. Add Viewer Role
 5. Click on Save
 Retrieve the 
562
563
Step-4 : Grant permissions at Organization scope
 Prior to proceeding with the following steps, make sure to choose the organization from top drown down.
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 To Fetch your service account id follow steps outlined on this page 
Retrieve the Service Account Id
 3. Assign the Roles (Viewer, Organization Viewer, Browser, Billing Account Viewer)
 4. Click Save
 564
Step-5 : Retrieve Bi ling Account Id and Project Id.
 Steps to Retrieve Billing Account Id and Project Id
 1. Click on Billing.
 2. Click on Manage Billing Accounts.
 3. Click on My Projects. Make a note of Project Id and Billing Account Id
 565
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
566
Step-6:  Capture the details to onboard GCP account
 Capture below details to share with your partner
 1. Account Id 
2. Project Id 
Step-5 : Retrieve Billing Account Id and Project Id.
 Step-5 : Retrieve Billing Account Id and Project Id.
 3. Dataset Name 
Step-1 : Enable Billing Export.
 <<Previous  ---------------------------------------------------------------------------------------------------------- 
567
[CLI] GCP Biling Account Manual Onboarding
 The process of manually onboarding GCP Billing accounts via the GCP CLI interface involves 2 steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company. 
1. 
2. 
[CLI] GCP Billing Account Onboarding for Target 
GCP Connect Billing Account for Partner 
568
[CLI] GCP Biling Account Onboarding for Target
 The Target Company is required to implement the following steps within the GCP Cloud Shell. Please sign in to the GCP console 
using the Admin account where billing has been set up, and then initiate the Cloud Shell from the navigation bar.
 To carry out below steps, Service account id is required. Please consult your partner company to share service account id before 
moving forward.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 In order to execute the below steps, you need to have owner role.
 Step-1: Enable Billing Export
 Unfortunately, activating billing export via CLI is not feasible. We recommend adhering to the manual steps provided in the referenced guide 
Enable Billing Export 
Step-2: Create a custom BigQuery Role
 1 gcloud iam roles create billingaccess --project=PROJECT_ID --title="billingaccess" -
permissions=bigquery.jobs.create,resourcemanager.projects.get
 Replace 
PROJECT_ID with your actual GCP project ID. (Follow this instructions to get project id 
urce Manager Documentation  |  Google Cloud 
Step-3: Grant service account Access to the custom BigQuery role
 Assign the custom role to the Service Account 
Creating and managing projects  |  Reso
 1 gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_ID" -
role="projects/PROJECT_ID/roles/billingaccess" --condition=None
 Replace 
SERVICE_ACCOUNT_ID with Service Account Id shared by your partner, and 
PROJECT_ID with your actual GCP project ID.
 Step-4: Grant service account access to the dataset
 1 gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_ID" -
role=roles/bigquery.dataViewer --condition=None
 Replace 
SERVICE_ACCOUNT_ID with Service Account Id shared by your partner
 Step-5: Enable Cloud Resource Manager API
 1 gcloud services enable cloudresourcemanager.googleapis.com
 Step-6: Retrieve the Billing Account Id and Project Id
 1 gcloud beta billing projects describe PROJECT_ID --format="value(billingAccountName.basename())"
 PROJECT_ID with your actual GCP project ID
 569
Step-2: Capture the below details and share with your partner.
 1. Account Id
 2. Project Id
 3. Dataset Name: Captured while performing in this step Enable Billing Export.  
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
570
[Automation] GCP Biling Account Onboarding
 There are 3 steps to onboard GCP Billing accounts through automation:
 1. 
2. 
3. 
[Automation] GCP Billing Account Onboarding for Target 
GCP Billing Onboarding Command 
GCP Connect Billing Account for Partner 
571
[Automation] GCP Biling Account Onboarding for Target
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 To execute the below command, it is recommended to have the Owner role.
 To proceed with the following steps, you'll need a command. Please consult your partner to obtain the command
 Upon receiving the command from the partner company, please execute in the GCP cloud shell.
 After execution you need to share the creds with your partner company
 Capture the below details and share them with your partner.
 1. Account ID
 2. Project ID
 3. Dataset Name
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
572
GCP Biling Onboarding Command
 Share the below command with your target company.
 1 curl -sO "https://storage.googleapis.com/cloudwiz-io-assets/gcp-onboarding.pyz" && python3 gcp-onboarding.pyz 
onboard-billing-account <TENANT-ID> <SERVICE-AC-ID>
 Replace the <TENANT-ID> & <SERVICE-AC-ID> by following below steps.
 To get the Service account id follow instructions outlined in this page 
To get the Tenant id follow instructions outlined in this page  
Retrieve the Service Account Id  
Retrieve the Tenant Id 
573
GCP Connect Biling Account for Partner
 To link an account on DigitalEx, you'll require onboarding credentials. Please reach out to your target company to obtain these 
credentials.
 Upon receipt of the onboarding credentials from the Target Company, please adhere to the following procedure to incorporate the provider 
through the DigitalEx platform.
 If none of the providers is onboarded, follow the below steps.
 If one of the providers is onboarded, follow the link GCP Connect Billing Account for Partner to onboard additional providers.
 1. Click on GCP Provider
 2. Click on Connect manually.
 574
3. Click on Connect Billing Account
 4. Enter the details shared by Target company.
 5. Click on connect & done.
 575
If one of the providers is onboarded, follow the steps below to onboard additional providers.
 1.  Navigate to Menu > Admin > Public Clouds > +Account.
 2. Select the GCP provider & Click on Manual tab
 3. Enter the details shared by Target
 576
4. Click Connect
 5. The onboarded Billing Account will be displayed with the list of all linked Projects.
 6.  Go to the Menu option and Click Cost.
 577
7.  Data will display immediately after successful ingestion.
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
578
GCP Projects Onboarding.
 There are 2 ways to onboard GCP Projects account
 GCP Project UI Onboarding
 [UI] GCP Project  Manual Onboarding 
GCP Project Automated Onboarding
 [Automation] GCP Project Onboarding 
579
[UI] GCP Project  Manual Onboarding
 The process of manually onboarding GCP Project accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[UI] GCP project onboarding for Target 
GCP Connect Project Onboarding Partner 
580
[UI] GCP project onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the GCP portal. Kindly access the Azure 
portal and adhere to the prescribed steps.
 To carry out below steps, Service Account Id is required. Please consult your partner company to share before moving forward.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1 : Enable APIs
 Step-2 : Grant access to Service account--------------------------------------------------------------------------------------------------------- Next>> 
581
Step-1 : Enable APIs
 In order to execute the below steps, you need to have owner role.
 Enable Cloud Resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box. 
3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below
 582
Enable Cloud Asset API
 1. Enter Cloud Asset API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
583
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
Stackdriver Monitoring API
 1. Enter Stackdriver Monitoring API in the Search bar and Select. 
584
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
585
Step-2 : Grant access to Service account
 To Execute the below steps, you need service account id. Please consult your partner company
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 3. Assign the Roles (Viewer, Cloud Asset Viewer & Monitoring viewer)
 4. Click Save
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
586
587
[Automation] GCP Project Onboarding
 There are 3 steps to onboard GCP Projects through automation:
 1. 
2. 
3. 
[Automation] GCP Projects Onboarding for Target 
GCP Projects Onboarding Command 
GCP Connect Project Onboarding Partner 
588
[Automation] GCP Projects Onboarding for Target
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 To proceed with the following steps, you'll need a command. Please consult your partner to obtain the command.
 To execute the below command, it is recommended to have the Owner role.
 Upon receiving the command from the partner company, please execute in the GCP cloud shell.
 589
GCP Projects Onboarding Command
 Share the below command with your target company.
 1 curl -sO "https://storage.googleapis.com/cloudwiz-io-assets/gcp-onboarding.pyz" && python3 gcp-onboarding.pyz 
onboard-usage-account <TENANT-ID> <SERVICE-ACCOUNT-ID> https://api.digitalex.io
 Replace the <TENANT-ID>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id  
Replace the <SERVICE-ACCOUNT-ID>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Service Account Id  
590
GCP Connect Project Onboarding Partner
 After target company completes his part, please adhere to the following procedure to incorporate the provider through the DigitalEx platform.
 1. Login to DigitalEx
 2. Click on Menu > Admin > Public Clouds
 3. Below Page will be displayed with the list of All linked Projects.
 4. Click on Connect button of the specific project.
 5. Click on Manual > Connect
 591
6. On-boarded projects will be displayed on the list of projects. It takes up to 30 minutes to discover the data
 592
9. Click the Resource from the Menu option.
 593
10. Resources will get discovered in DigitalEx
 594
---------------------------------------------------------------------------------------------------------- Next>> 
595
[UI] GCP Organization Manual Onboarding
 The process of manually onboarding GCP Project accounts via the user interface involves two steps: The initial step must be 
carried out by the Target Company, while the following step is the responsibility of the partner company.
 1. 
2. 
[UI] GCP Organization onboarding for Target 
GCP Connect Organization Onboarding Partner 
596
[UI] GCP Organization onboarding for Target
 The Target Company is required to execute the subsequent onboarding process through the GCP portal. Kindly access the Azure 
portal and adhere to the prescribed steps.
 To carry out below steps, Service Account Id is required. Please consult your partner company to share before moving forward.
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 Step-1 :Enable APIs
 Step-2 :Grant access to Service account--------------------------------------------------------------------------------------------------------- Next>> 
597
Step-1 :Enable APIs
 In order to execute the below steps, you need to have owner role.
 Enable Cloud Resource Manager API
 1. Enter Cloud Resource Manager API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Resource Manager API 
from the search box. 
3. Click Enable.
 4. Resource manager API gets enabled successfully as shown below
 Enable Cloud Asset API
 1. Enter Cloud Asset API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
598
Stackdriver Monitoring API
 1. Enter Stackdriver Monitoring API in the Search bar and Select. 
2. If there are multiple projects, it asks you to select a project, or the below page is displayed after selecting Cloud Asset API from the 
search box. 
3. Click Enable.
 4. Cloud Asset API gets enabled successfully as shown below. 
<<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
599
Step-2 :Grant access to Service account
 To Execute the below steps, you need service account id. Please consult your partner company
 1. Go to IAM & Click Grant Access
 2. Under Add Principals. Enter service account id of DigitalEx
 3. Assign the Roles (Viewer, Cloud Asset Viewer & Monitoring viewer)
 4. Click Save
 <<Previous  ---------------------------------------------------------------------------------------------------------- Next>> 
600
[Automation] GCP Organization Manual Onboarding
 There are 3 steps to onboard GCP Projects through automation:
 1. 
2. 
3. 
[Automation] GCP Organization Onboarding for Target 
GCP Organization Onboarding Command 
GCP Connect Organization Onboarding Partner 
601
[Automation] GCP Organization Onboarding for Target
 Please go through 
GCP Troubleshooting to determine its applicability before beginning the onboarding process.
 To proceed with the following steps, you'll need a command. Please consult your partner to obtain the command.
 To execute the below command, it is recommended to have the Owner role.
 Upon receiving the command from the partner company, please execute in the GCP cloud shell.
 602
GCP Organization Onboarding Command
 Share the below command with your target company.
 1 curl -sO "https://storage.googleapis.com/cloudwiz-io-assets/gcp-onboarding.pyz" && python3 gcp-onboarding.pyz 
onboard-usage-account <TENANT-ID> <SERVICE-ACCOUNT-ID> https://api.digitalex.io
 Replace the <TENANT-ID>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Tenant Id  
Replace the <SERVICE-ACCOUNT-ID>
 To get the tenant id follow instructions outlined in this page 
Retrieve the Service Account Id  
603
GCP Connect Organization Onboarding Partner
 After target company completes his part, please adhere to the following procedure to incorporate the provider through the DigitalEx platform.
 1. Login to DigitalEx
 2. Click on Menu > Admin > Public Clouds
 3. Below Page will be displayed with the list of All linked Organizations.
 4. Click on Connect button of the specific organizations
 5. Click on Manual > Connect
 604
6. On-boarded projects will be displayed on the list of projects. It takes up to 30 minutes to discover the data
 9. Click the Resource from the Menu option.
 605
10. Resources will get discovered in DigitalEx---------------------------------------------------------------------------------------------------------- Next>> 
606
Retrieve the Tenant Id
 Retrieve the Tenant Id from Setup Page
 1. Login to DigitalEx
 2. Click on Setup from Header
 3. Click on API
 4. Capture and share the Tenant id with the Target Company.
 Retrieve the Tenant Id from Menu
 1. Login to DigitalEx
 2. Click on Menu
 3. Click on API under the Admin
 607
4. Capture & share the Tenant id with the Target Company. 
608
Retrieve the Service Account Id
 Retrieve the Service Account Id from Setup Page
 1. Login to DigitalEx
 2. Click GCP Provider 
3. Click on Connect Manually link.
 4. Click on Connect Billing Account button. 
609
5. Capture and share Service Account id with the Target Company. 
Retrieve the Service Account Id from Menu
 1. Login to DigitalEx
 2. Click on the side menu.
 3. Click on Public Clouds under the Admin 
610
4. Click on +Account. 
5. Go to GCP & Click on Manual Tab 
611
6. Capture and share the Service Account id with Target Company.
'''

def rag(query):
    try:
        
        QDRANT_API_KEY = "IhyblpSTqHUICu2hXDXQbSTw1yNRdvQj1BXmmKkI0VCb_Na4B-ImxA"
        QDRANT_URL = "https://f60408b9-0739-40b1-885d-56e57ef88ee5.us-east4-0.gcp.cloud.qdrant.io"
        GEMINI_API_KEY = "AIzaSyCtO7jsR7sT-riZYuCJa69-qdjblR0qez0"
        COLLECTION_NAME = "digitalex_vectors"
        # Initialize embeddings model
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GEMINI_API_KEY
        )
        embedding = embeddings.embed_query(query)
        
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding,
            limit=11  # Adjust limit as necessary
        )

        if not search_result:
            return "No results found for your query."

        # Combine the page content from the search result
        retriever = "".join([hit.payload['page_content'] for hit in search_result])
        return retriever
    
    except Exception as e:
        return f"An error occurred: {str(e)}"