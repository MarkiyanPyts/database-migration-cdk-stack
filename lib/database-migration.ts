
import { Construct } from 'constructs';
import {
  Stack,
  StackProps,
  aws_sqs,
  aws_apigateway,
  aws_lambda,
  aws_lambda_nodejs,
  RemovalPolicy,
  Duration,
  aws_events,
  aws_events_targets
} from "aws-cdk-lib";
import {PythonFunction, PythonLayerVersion, } from "@aws-cdk/aws-lambda-python-alpha"
import path = require('path');
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class DatabaseMigrationCdkStackStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    const usersDLQ = new aws_sqs.Queue(this, 'dm_users_dl_queue', {
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const usersQueue = new aws_sqs.Queue(this, 'dm_users_queue', {
      removalPolicy: RemovalPolicy.DESTROY,
      visibilityTimeout: Duration.minutes(15),
      deadLetterQueue: {
        maxReceiveCount: 1,
        queue: usersDLQ
      }
    });

    const usersQueueConsumer = new PythonFunction(this, 'dm_users_queue_consumer', {
      entry: path.join(__dirname, './functions/usersQueueConsumer/code'),
      runtime: aws_lambda.Runtime.PYTHON_3_12, // required
      handler: 'handler',
      timeout: Duration.minutes(5),
    });

    const pollUsersFromQueue = new PythonFunction(this, 'dm_poll_users_from_queue', {
      entry: path.join(__dirname, './functions/pollUsersFromQueue/code'),
      runtime: aws_lambda.Runtime.PYTHON_3_12,
      handler: 'handler',
      timeout: Duration.minutes(5),
    });


    const userProcessorJobLayers = new PythonLayerVersion(this, 'dm_user_processor_job_layer', {
      compatibleRuntimes: [aws_lambda.Runtime.PYTHON_3_12],
      entry: path.join(__dirname, './functions/userProcessorJob/layers'), // point this to your library's directory
    })

    const userProcessorJob = new PythonFunction(this, 'dm_user_processor_job', {
      entry: path.join(__dirname, './functions/usersQueueConsumer/code'),
      runtime: aws_lambda.Runtime.PYTHON_3_12, // required
      handler: 'handler', // optional, defaults to 'handler'
      layers: [userProcessorJobLayers],
      timeout: Duration.minutes(15),
    });

    const apiAuthorizer = new PythonFunction(this, 'dm_api_authorizer', {
      entry: path.join(__dirname, './functions/authorizer/code'),
      runtime: aws_lambda.Runtime.PYTHON_3_12, // required
      handler: 'handler',
    });

    const auth = new aws_apigateway.RequestAuthorizer(this, "dm_authorizer", {
      handler: apiAuthorizer,
      identitySources: [aws_apigateway.IdentitySource.header("Authorization")],
      resultsCacheTtl: Duration.seconds(0),
    });

    const api = new aws_apigateway.RestApi(this, 'dm_migration_api', {
      defaultMethodOptions: {
        authorizer: auth,
      },
    });

    const usersQueueConsumerAPI = api.root.addResource("users_queue_consumer");

    usersQueueConsumerAPI.addMethod(
      "POST",
      new aws_apigateway.LambdaIntegration(usersQueueConsumer)
    );

    const pollUsersFromQueueAPI = api.root.addResource("poll_users_from_queue");

    pollUsersFromQueueAPI.addMethod(
      "POST",
      new aws_apigateway.LambdaIntegration(pollUsersFromQueue)
    );

    const JobsTriggerEventBus = new aws_events.EventBus(this, 'dm_job-trigger-event-bus', {
      eventBusName: 'dm_job-trigger-event-bus',
    });

    new aws_events.Rule(this, "dm_trigger-user-processor-job", {
      eventBus: JobsTriggerEventBus,
      eventPattern: {
        source: ["trigger-user-processor-job"],
      },
    }).addTarget(new aws_events_targets.LambdaFunction(userProcessorJob));


    //usersQueue give permission to pollUsersFromQueue
    usersQueue.grantConsumeMessages(pollUsersFromQueue);
    usersQueue.grantPurge(userProcessorJob);
    
    //userProcessorJob give permission to usersQueueConsumer

    
  }
}
