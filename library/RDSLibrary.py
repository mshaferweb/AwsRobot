import boto3
import time

class RDSLibrary:

    def __init__(self):
        self.rds = boto3.client('rds')
        self.DBName = 'books'
        self.MasterUsername = 'dbadmin'
        self.MasterUserPassword = 'abcdefg123456789'
        self.DBInstanceClass = 'db.t2.micro'
        self.Engine = 'postgres'

    def build_postgres_url(self,instance_identifier):
        # postgresql://dbadmin:abcdefg123456789@hello4.cqa6jc4nxqdn.us-east-2.rds.amazonaws.com/books
        hostname = self.get_public_host_address(instance_identifier)
        url = "postgresql://" + self.MasterUsername + ":"  + self.MasterUserPassword + "@" + hostname + "/" + self.DBName
        return url

    def create(self,instance_identifier):
        try:
            response = self.rds.create_db_instance(
                DBName=self.DBName,
                DBInstanceIdentifier=instance_identifier,
                MasterUsername=self.MasterUsername,
                MasterUserPassword=self.MasterUserPassword,
                DBInstanceClass=self.DBInstanceClass,
                Engine=self.Engine,
                AllocatedStorage=5)
            print(response)
        except Exception as error:
            print("Got exception: ", error)
            error
        self.wait_for_instance_to_be_running(instance_identifier)
        return response

    def create_snapshot(self, instance_identifier, snapshot_name):
        try:
            response = self.rds.create_db_snapshot(
                DBInstanceIdentifier=instance_identifier,
                DBSnapshotIdentifier=snapshot_name)
            print(response)
            return response
        except Exception as error:
            print("Got exception: ", error)
            error

    def restore_snapshot(self, instance_identifier, snapshot_name):
        try:
            response = self.rds.restore_db_instance_from_db_snapshot(
                DBInstanceIdentifier=instance_identifier,
                DBSnapshotIdentifier=snapshot_name)
            print(response)
            return response
        except Exception as error:
            print("Got exception: ", error)
            error

    def delete(self,instance_identifier):
        try:
            response = self.rds.delete_db_instance(
                DBInstanceIdentifier=instance_identifier,
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True)
            print(response)
            print("Deleting ", response["DBInstance"]["DBInstanceIdentifier"])
        except Exception as error:
            print("Got exception: ", error)
            error

    def start(self,instance_identifier,tries=25):
        if self.check_if_instance_is_running(instance_identifier):
            return True
        else:
            try:
                response = self.rds.start_db_instance(
                    DBInstanceIdentifier=instance_identifier)
                print(response)
            except Exception as error:
                print("Got exception: ", error)
                error
        return self.wait_for_instance_to_be_running(instance_identifier)

    def stop(self,instance_identifier):
        if not self.check_if_instance_is_running(instance_identifier):
            return True
        else:
            try:
                response = self.rds.stop_db_instance(
                    DBInstanceIdentifier=instance_identifier)
                print(response)
            except Exception as error:
                print("Got exception: ", error)
                error
        return True

    def get_public_host_address(self,instance_identifier):
        instance_list = []
        try:
            response = self.rds.describe_db_instances()
            for instance in response["DBInstances"]:
                if instance['DBInstanceIdentifier'] == instance_identifier:
                    return instance['Endpoint']['Address']
        except Exception as error:
            print("Got exception: ", error)
            return error

    def list(self):
        instance_list = []
        try:
            response = self.rds.describe_db_instances()
            for instance in response["DBInstances"]:
                instance_list.append(instance['DBInstanceIdentifier'])
            return instance_list
        except Exception as error:
            print("Got exception: ", error)
            return error


    def check_if_instance_is_running(self,instance_identifier):
        try:
            response = self.rds.describe_db_instances()
            print(response)
        except Exception as error:
            print("Got exception: ", error)
            error
        for instance in response["DBInstances"]:
            if instance['DBInstanceIdentifier'] == instance_identifier:
                if instance['DBInstanceStatus'] == 'available':
                    return True
        return False


    def modify_instance_name(self,instance_identifier,new_instance_identifier):
        try:
            response = self.rds.modify_db_instance(
                DBInstanceIdentifier = instance_identifier,
                NewDBInstanceIdentifier = new_instance_identifier,
                ApplyImmediately=True
            )
            print(response)
        except Exception as error:
            print("Got exception: ", error)
            error
        return False

    def wait_for_instance_to_be_running(self,instance_identifier,tries=50):
        instance_running = False
        print("Starting at: ", time.localtime())

        while tries > 0 and not instance_running:
            if self.check_if_instance_is_running(instance_identifier):
                print("Running at: ",time.localtime())
                return ("Running at: ",time.localtime())
            time.sleep(30)
            tries -= 1
            print("Waiting for :", instance_identifier,"Tries :",tries)

#rds = RDSLibrary()
# # rds.list()
# print(rds.build_postgres_url('hello4'))
# # rds.create_snapshot('hello4','hello4-snapshot1')
# rds.restore_snapshot('hello5','hello4-snapshot')
# #rds.modify_instance_name('hello5','hello4')
#rds.delete("robotdemo2")

