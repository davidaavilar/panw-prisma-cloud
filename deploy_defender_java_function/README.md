# Deploy Defender on a Java Function


### Pre-requisites 📋

# Requirements
- [Java 8 runtime environment (SE JRE)](https://www.oracle.com/java/technologies/javase-downloads.html)
- [Gradle](https://gradle.org/releases/) or [Maven](https://maven.apache.org/docs/history.html)
- The Bash shell. For Linux and macOS, this is included by default. In Windows 10, you can install the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to get a Windows-integrated version of Ubuntu and Bash.
- [The AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) v1.17 or newer.

If you use the AWS CLI v2, add the following to your [configuration file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) (`~/.aws/config`):

```
cli_binary_format=raw-in-base64-out
```

This setting enables the AWS CLI v2 to load JSON events from a file, matching the v1 behavior.

### Setup 🔧

You can use this Java function on AWS as example, and follow these steps to deploy the Lambda Function. [Click here to go the repo](https://github.com/awsdocs/aws-lambda-developer-guide/tree/main/sample-apps/java-basic)

Before creating your artifact (.jar function), you have to make some changes. Given this Java Function example:

```
package example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.LambdaLogger;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.Map;

// Handler value: example.Handler
public class Handler implements RequestHandler<Map<String,String>, String>{
  Gson gson = new GsonBuilder().setPrettyPrinting().create();
  @Override
  public String handleRequest(Map<String,String> event, Context context)
  {
    LambdaLogger logger = context.getLogger();
    String response = "200 OK";
    // log execution details
    logger.log("ENVIRONMENT VARIABLES: " + gson.toJson(System.getenv()));
    logger.log("CONTEXT: " + gson.toJson(context));
    // process event
    logger.log("EVENT: " + gson.toJson(event));
    logger.log("EVENT TYPE: " + event.getClass());
    return response;
  }
}
```

```
package example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.LambdaLogger;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.Map;

import com.twistlock.serverless.Twistlock;                                          // ADD THIS

// Handler value: example.Handler
public class Handler implements RequestHandler<Map<String,String>, String>{
  Gson gson = new GsonBuilder().setPrettyPrinting().create();
  @Override
  public String handleRequest(Map<String,String> event, Context context)
  {
    LambdaLogger logger = context.getLogger();
    String response = "200 OK";
    // log execution details
    logger.log("ENVIRONMENT VARIABLES: " + gson.toJson(System.getenv()));
    logger.log("CONTEXT: " + gson.toJson(context));
    // process event
    logger.log("EVENT: " + gson.toJson(event));
    logger.log("EVENT TYPE: " + event.getClass());
    return response;
  }
  public String protectedHandler(Map<String,String> event, Context context) {       // ADD THIS
      return Twistlock.Handler(this, event, context);                               // ADD THIS
  }                                                                                 // ADD THIS
}
```

and follow your Prisma Cloud instructions.

When they ask you to "Change the Lambda handler setting from handleRequest to protectedHandler"

You have to configure your handler from `example.Handler` to `example.Handler::protectedHandler`

PD: If your Prisma Cloud documentation says to modify your build.gradle (just if you are using Gradle) on `dependencies.compile`, just change `compile` for `implementation`. Note that the `compile`, `runtime`, `testCompile`, and `testRuntime` configurations introduced by the Java plugin have been deprecated since Gradle 4.10 (Aug 27, 2018), and were finally removed in Gradle 7.0 (Apr 9, 2021).

The aforementioned configurations should be replaced by `implementation`, `runtimeOnly`, `testImplementation`, and `testRuntimeOnly`, respectively.
