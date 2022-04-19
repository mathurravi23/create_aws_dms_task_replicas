import json
import boto3
from boto3 import Session
from botocore.config import Config
import os
import sys
import argparse

parser = argparse.ArgumentParser(description = 'Create local or cross region copies of AWS DMS task with same task settings & table mapping rules')
parser.add_argument('--task_name',required=True, type=str, help = 'Specify DMS task name')
parser.add_argument('--region',required=True, type=str, help = 'Specify AWS region for current DMS task')
parser.add_argument('--copies', default=1,type=int, help = 'Number of copies required for current DMS task. By default, script will create one copy in same AWS region.')
parser.add_argument('--target_region', type=str, help = 'Specify Target DMS task region')
parser.add_argument('--target_dms_instance', type=str, help = 'Specify ARN of DMS instance ARN in target region. For cross region move,make sure to specify target_region argument.')
parser.add_argument('--target_source_endpoint', type=str, help = 'Specify ARN of Source endpoint in target region. For cross region move,make sure to specify target_region argument.')
parser.add_argument('--target_target_endpoint', type=str, help = 'Specify ARN of target endpoint in target region. For cross region move,make sure to specify target_region argument.')
parser.add_argument('--migration_type', type=str, help = 'Specify new migration type for new dms task. Valid values: full-load OR cdc OR full-load-and-cdc')
parser.add_argument('--counter', type=int, help = 'Specify START counter for new tasks')

args = parser.parse_args()

def main():
   try:

      client = boto3.setup_default_session(region_name=args.region)
      client = boto3.client('dms')

      response = client.describe_replication_tasks(Filters=[ { 'Name': 'replication-task-id', 'Values': [args.task_name] }])

      with open("tmp_dms_task_settings.json",'w') as f:
            f.write(response["ReplicationTasks"][0]["ReplicationTaskSettings"])

      with open('tmp_dms_task_settings.json') as f:
            data = json.load(f)
      

      newjson= '{'
      newjson= newjson + '"TargetMetadata":'+str(data["TargetMetadata"])
      newjson= newjson + ',"FullLoadSettings":'+str(data["FullLoadSettings"])
      newjson= newjson + ',"Logging": { "EnableLogging": true }'
      newjson= newjson + ',"ControlTablesSettings":'+str(data["ControlTablesSettings"])
      newjson= newjson + ',"StreamBufferSettings":'+str(data["StreamBufferSettings"])
      newjson= newjson + ',"ChangeProcessingDdlHandlingPolicy":'+str(data["ChangeProcessingDdlHandlingPolicy"])
      newjson= newjson + ',"ErrorBehavior":'+str(data["ErrorBehavior"])
      newjson= newjson + ',"ChangeProcessingTuning":'+str(data["ChangeProcessingTuning"])
      newjson= newjson +'}'


      with open("new_dms_tasksettings.json", 'w') as f:
                   f.write(newjson)  

      if(args.target_dms_instance !=None):  
        dms_instance=args.target_dms_instance
      else:
        dms_instance=response["ReplicationTasks"][0]["ReplicationInstanceArn"]

      if(args.target_source_endpoint !=None):
        source_endpoint=args.target_source_endpoint
      else:
        source_endpoint=response["ReplicationTasks"][0]["SourceEndpointArn"]

      if(args.target_target_endpoint !=None):
        target_endpoint=args.target_target_endpoint
      else:
        target_endpoint=response["ReplicationTasks"][0]["TargetEndpointArn"]

      if(args.migration_type !=None):
        migration_type=args.migration_type
      else:
        migration_type=response["ReplicationTasks"][0]["MigrationType"]



      if(args.counter !=None):
        i=args.counter
      else:
        i=1

      icopy = args.copies

      j=0

      if (args.region != args.target_region):
        trg_client= boto3.client('dms',region_name=args.target_region)
      else:
        trg_client= boto3.client('dms',region_name=args.region)
     

      while j < icopy :
        j+=1
        newtask=args.task_name+str(i)  
        createresponse=trg_client.create_replication_task(
                                  ReplicationTaskIdentifier=newtask,
                                  SourceEndpointArn=source_endpoint,
                                  TargetEndpointArn=target_endpoint,
                                  ReplicationInstanceArn=dms_instance,
                                  MigrationType=migration_type,
                                  TableMappings=response["ReplicationTasks"][0]["TableMappings"],
                                  ReplicationTaskSettings=newjson
                                  )
        i+=1

        print(createresponse)
      print ('')
      print ('')
      print('Script Completed !')
      
      print('Starting Cleanup of temp files..')

      if os.path.exists("tmp_dms_task_settings.json"):
        os.remove("tmp_dms_task_settings.json")

      if os.path.exists("new_dms_tasksettings.json"):
        os.remove("new_dms_tasksettings.json")
      
      print('')
      print('Cleanup complete!')


   except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
