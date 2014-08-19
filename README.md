Rester
========
Framework for testing RESTful APIs
----------------------------------
Rester allows you to test your APIs using a non-programatic or non-GUI based approach (which are some of the more conventional ways of testing RESTFul APIs). *Rester* is inspired by various unit testing frameworks like JUnit, 'unittest' (python) etc and is conceptually organized like those frameworks but is geared towards testing RESTful API endpoints. With *Rester*, all tests are specified in JSON, so it can also be used by non-programmers as well.

#So, why Rester?
Testing RESTful APIs generally involves two prediticable steps -

- Invoke the API end point
- Validate the response - headers, payload etc

Most testing tools available for testing RESTful APIs use some sort of a GUI based approach which doesn't lend itself towards re-use, better code organization, abstraction etc and some of the other benefits that are generally available with more programmatic frameworks like JUnit. Programmatically building test cases provides the highest level of flexibility and sophistication, but the downside to this approach is that it ends up with lots of fairly tedious and repetitive code. Conceptually, Rester is similar to existing unit testing frameworks, but it uses JSON (instead of a programming language) to implement/specify the actual tests. It can be used by programmers and non-programmers alike, but reap all the benefits of a unittesting framework.


Note: As of now Rester only supports APIs that don't require explicit authentication of calls, but future versions will support OAuth. The Rester was mainly created to test internal RESTful APIs that generally bypass the need for authentication of the calls. Also, Rester only supports validation of JSON responses.

#Practical uses of Rester
- Perform "integration" testing of internal and external RESTful API endpoints
- Examine and test complex response payloads
- You can simply use Rester to dump and analyze API responses - headers, payload etc.

#Assumptions
- Rester does not manage the life-cycle of the container or the server that exposes the API endpoints, but assumes the API endpoints (to be tested) are up and avaliable.
- Unlike other unittesting frameworks however, Rester does guarantee the order of execution of the **TestSteps** within a **TestCase**. For a better understanding of TestSteps and TestCases see the "General Concepts" section below. The **ordering** will come in handy if you want to test a series of API end-points (invoked in succession) that modify system state in a particular way.


#General Concepts

* **TestSuite**:
 A *TestSuite* is collection of *TestCases*. The idea is to group related 'test cases' together.

```
{
   "test_cases":[
                 "test_case_1.json",
                 "test_case_2.json"
                ]
}
```

* **TestCase**:
 A *TestCase* contains one or more *TestSteps*. You can declare **globals** variables to be re-used across test steps. For a more complete list of all the options, please see -


```
{
   "name":"Test Case X",
   "globals":{
      "variables":{
        "base_api_url":"https://example/api/v1",
        "api_key":"xxxx"
      }
   },
   "testSteps":[
      {
         ... each TestStep is specified in here
      },
      {
         ...  each TestStep is specified in here
      }
    ]
 ```

* **TestStep**:
  All of the action takes place in a **TestStep**.
For a more complete list of all the options, please see.

A TestStep contains the following -

- **API end point invocation** - As part of the API endpoint invocation, you can provide the following params -
  - URL
  - HTTP headers
  - URL params
  - HTTP method - get, put, post, delete ('get' is used by default)

  URL is the only mandatory param.

- A series of assert statements specified as part of an **AssertMap**
- Post step assignments

Example of a TestStep:

  ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
       "assertMap":{
             "headers":{
                 "content-type":"application/json; charset=utf-8"
             }
             "payLoad":{
                "message":"Hello World!"
             }
       }
    }
  ]
  ```

#Installation
pip install rester

#Rester command line options
- Run the default test case -

  `apirunner`

  This will look for the default test case, ***test_case.json in the current directory***
- Run a specific test case
  use the command line option ***--tc=<file_name>***

  e.g. invoke a test case specified in the file "./rester/examples/test_case.json"

  `apirunner --tc=./rester/examples/test_case.json`

- Run a specific test suite
  use the command line option ***--ts=<file_name>***

  e.g. invoke a test suite specified in the file "./rester/examples/test_suite.json"

  `apirunner --ts=./rester/examples/test_suite.json`

#Other command line options
- Adjust the log output or details
  Rester support varying levels of logs - DEBUG, INFO, WARN, ERROR. You can
  specify the level using the command line option ***--log=<LEVEL>***

  e.g. run the API with INFO level

  `apirunner  --log=INFO`

- Just dump the JSON output

#TestCase options
- **Skipping tests**

#TestStep options

#Examples of API request invocations
- Specify the HTTP headers as part of an API request
 ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
  		   "headers":{
            "content-type":"application/json;"
       },
       ....
    }
  ]
  ```

- Specify the URL params as part of an API request.
  There are two ways to specific URL params, which are mentioned below -

  ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
  		   "headers":{
  		      ...
       },
       "params":{
            "param_1":"value1",
            "param_2":"value2"
       },
       ....
    }
  ]
  ```


   ```
  testSteps: [
    {
      "name":"Name of TestStep",
  		"apiUrl":"http://example/api/v1/helloworld/print?param_1=value1&param_2=value2",
       ....
    }
  ]
  ```

- Perform an HTTP POST
  ```
  testSteps: [
    {
        "name":"Name of TestStep",
        "apiUrl":"http://example/api/v1/helloworld/print",
        "headers":{
            ...
        },
        "method":"post"
        "params":{
            "param_1":"value1",
            "param_2":"value2"
        },
       ....
    }
  ]
  ```

#Examples of assert statements
As mentioned previously, all of the assert statements are specified within an **assertMap** element

- Assert "content-type" HTTP header
 ```
  testSteps: [
    {
      "name":"Name of TestStep",
      "apiUrl":"http://example/api/v1/helloworld/print?param_1=value1&param_2=value2",
       ....
    }

    "assertMap":{

        "headers":{
          "content-type":"application/json; charset=utf-8"
        },

        ....

    }
  ]

- Assert specific payload elements -
  "output.level" is 2
  "output.result" is eqal to "Message Success"
  "output.status" is greater than 3

 ```
  testSteps: [
    {
      "name":"Name of TestStep",
      "apiUrl":"http://example/api/v1/helloworld/print?param_1=value1&param_2=value2",
       ....
    }

    "assertMap":{
        "headers": {
           ....
        },

        "payLoad":{
            "output.level":2,
            "output.result":"Message Success",
            "output.status":"-gt 3",
        },
        ....

    }
  ]
  ```

# Assert logical operators:

- **-gt** - greater than

  ```

  e.g. parent.child > 3

      "payLoad":{
            "parent.child":"-gt 3",
      }
  ```

- **-ge** - greater than eqal to

  ```
  e.g. parent.child >= 3

      "payLoad":{
            "parent.child":"-ge 3",
      }
  ```

- **-lt** - lesser than

  ```

  e.g. parent.child < 2

      "payLoad":{
            "parent.child":"-lt 2",
      }
  ```

- **-le** - lesser than eqal to

  ```

  e.g. parent.child <= 2

      "payLoad":{
            "parent.child":"-le 2",
      }
  ```

- **-ne**  - not eqal to

  ```

  e.g. parent.child.message != "success"

      "payLoad":{
            "parent.child.message":"-ne success",
      }
  ```

- **-eq**  -  eqal to

```
  e.g. parent.child.message == "error"
      "payLoad":{
            "parent.child.message":"-eq success",  # either will work
            "parent.child.message":"success",
      }
  ```

# Basic JSON Type checking
## The following JSON types are supported - Integer, Float, String, Array, Boolean

  ```
  e.g. check if parent.child.message is a String

      "payLoad":{
            "parent.child.message":"String",
      }

e.g. check if parent.child.version is an Integer

      "payLoad":{
            "parent.child.version":"Integer",
      }

e.g. check if parent.child is an Object

      "payLoad":{
            "parent.child":"Object",
      }


  ```


# Using variables declarations
- Variables are declared in the "globals" section of the TestSuite

  ```
   "globals":{
      "variables":{
        "baseApiUrl":"https://example.com",
        "api_key":"YOUR_KEY",
        "rule_key":"CONFIG_KEY"
      }
   },
   ...
  testSteps: [
    {
      "name":"Name of TestStep",
      "apiUrl":"http://{baseApiUrl}/api/v1/helloworld/print?param_1=value1
      ....
    }
  ]
  ```



#TODO
- Unit Tests
- Plenty of refactoring :-). Make it more pythonic for starters
- Cleaner test results summary (Tabular?)
- Better support for assert expressions
- Support for enums
- Support for OAuth
- Experiment with YAML format for specifying the tests
