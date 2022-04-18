# About
This Python script creates in-region or cross region replicas of existing AWS DMS tasks.

# Overview

In many situations you may require to create copy of existing DMS, for example, spliting large database migration into multiple small tasks or taking cross region backup DMS tasks. With this python script, you can easily create multiple copies of existing task with same DMS task settings & table mapping rules. 

# Prerequisites 

 Python3 https://www.python.org/downloads/
 
 Boto3 https://aws.amazon.com/sdk-for-python/
 
 AWS profile https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

# How to run  

At minimum, this script will take DMS task name & AWS region as an input.  

Syntax:
  python create_dms_task_replicas.py --task_name <task-name> --region <region>
  
example:
  $python3 create_dms_task_replicas.py --task_name ora-apg --region us-east-2
  
  Script will create new DMS tasks with same DMS task name suffix with numeric counters. Above commands will create new DMS task 'ora-apg1' in same AWS region and on same DMS repication instance.
  
  
<img width="627" alt="image" src="https://user-images.githubusercontent.com/82545117/163751862-fd379de0-d1a3-435d-8f2b-f7d50f2060fc.png">

  
# Examples
  
  [1] Create replica of existing DMS task on same DMS replication instance with in same AWS region:
  
     $python create_dms_task_replicas.py --task_name ora-apg --region us-east-2 
  
  [2] Create two replicas of existing DMS task on new DMS replication instance with in same AWS region:
  
       $python create_dms_task_replicas.py --task_name ora-apg --region us-east-2 --copies 2 --counter 10 --target_dms_instance <ARN of DMS instance>
  
    Note: With paramter 'counter' script will use specified number as starting prefix. In above example, script will create tasks 'ora-apg10', 'ora-apg11'.

  [3] Create one replica of existing DMS task on new DMS replication instance with in same AWS region but with new source & target endpoints:
  
       $python create_dms_task_replicas.py --task_name ora-apg --region us-east-2 --target_dms_instance <ARN of DMS instance> --target_source_endpoint <ARN of source endpoint> --target_target_endpoint <ARN of target endpoint>

  [4] Create one replica of existing DMS task in another AWS region:
  
    $python create_dms_task_replicas.py --task_name ora-apg --region us-east-2 --target_dms_instance <ARN of DMS instance> --target_source_endpoint <ARN of source endpoint> --target_target_endpoint <ARN of target endpoint> --target_region us-east-1

  Note - When creating cross region replica, make sure to specifify accurate 'target_region' parameter otherwise creation of task may fail.
  
  
  
  
  
  
 
  
  
  
