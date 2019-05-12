#!/usr/bin/python

import boto3
import requests


def test_public_elb(test_input, test_runner):
    session = boto3.Session(region_name=test_input["RegionName"])
    client = session.client("elb")
    elbName = test_input["PublicELBName"]

    # Get LB Details
    response = client.describe_load_balancers(
        LoadBalancerNames=[elbName]
    )
    if (not "LoadBalancerDescriptions" in response.keys()
            or len(response["LoadBalancerDescriptions"]) < 1
    ):
        test_runner.reportFailedTestResult(
            testName="test_public_elb",
            testDescription="Verify is AWS API: describe_load_balancers succeeded and load balancer exists",
            testOutput="Load balancer not found"
        )
        return

    instances = response["LoadBalancerDescriptions"][0]["Instances"]
    expectedInstancesMin = int(test_input["ExpectedInstancesMin"])
    expectedInstancesMax = int(test_input["ExpectedInstancesMax"])
    if expectedInstancesMin > len(instances) > expectedInstancesMax:
        test_runner.reportFailedTestResult(
            testName="test_public_elb",
            testDescription="Verify instances are attached to ELB",
            testOutput="Expected {0} but found {1} instances".format(
                str(expectedInstancesMin) + "-" + str(expectedInstancesMax),
                len(instances)
            )
        )
        return

    # Get LB instance health
    response = client.describe_instance_health(
        LoadBalancerName=elbName,
        Instances=instances
    )
    if not "InstanceStates" in response.keys() or len(response["InstanceStates"]) < 1:
        test_runner.reportFailedTestResult(
            testName="test_public_elb",
            testDescription="Verify AWS API: describe_instance_health succeeded",
            testOutput="No instances found"
        )
        return

    # Determine healthy instances
    instanceStates = response["InstanceStates"]
    healthyInstances = 0
    for instanceState in instanceStates:
        if instanceState["State"] == "InService":
            healthyInstances += 1

    if expectedInstancesMin > healthyInstances > expectedInstancesMax:
        test_runner.reportFailedTestResult(
            testName="test_public_elb",
            testDescription="Verify instances are healthy",
            testOutput="Expected {0} but found {1} healthy instances".format(
                str(expectedInstancesMin) + "-" + str(expectedInstancesMax),
                healthyInstances
            )
        )
        return

    # Report successful test
    test_runner.reportSuccessfulTestResult(
        testName="test_public_elb",
        testDescription="Verify instances are healthy",
        testOutput="{0} healthy instances found".format(healthyInstances)
    )
