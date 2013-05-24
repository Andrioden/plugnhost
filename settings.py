""" TCP port to be used for twisted communication """
COMMUNICATION_PORT = 7999

""" Created services, each item represent one service and the master and worker
class contains business logic for the specific services.

"""
SERVICES = {
    'http': {
        'MasterClass': "master.services.http.nginx_master_service.NginxMasterService",
        'WorkerClass': "worker.services.http.nodejs_worker_service.NodejsWorkerService",
    },
}