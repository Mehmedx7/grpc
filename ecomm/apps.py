from django.apps import AppConfig
import os
import sys
import grpc
from concurrent import futures

class EcommConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecomm'

    def ready(self):
        if os.environ.get('RUN_MAIN') or not sys.argv[0].endswith('manage.py'):
            return

        from .grpc_services import CustomerServicer
        from .protos import ecomm_pb2_grpc

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ecomm_pb2_grpc.add_CustomerServiceServicer_to_server(
            CustomerServicer(), server
        )
        server.add_insecure_port('[::]:50051')

        import threading
        grpc_thread = threading.Thread(target=server.start)
        grpc_thread.daemon = True
        grpc_thread.start()