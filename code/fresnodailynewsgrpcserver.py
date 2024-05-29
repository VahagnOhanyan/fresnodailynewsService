from concurrent import futures

import grpc

from services import FresnoDailyNews_pb2, FresnoDailyNewsGetVerbs_pb2, FresnoDailyNewsGetVerbsStartWith_pb2
from services import FresnoDailyNewsGetVerbsStartWith_pb2_grpc, FresnoDailyNews_pb2_grpc, \
    FresnoDailyNewsGetVerbs_pb2_grpc
from code.pythonrpcmethods import extract_keywords, get_verb_forms, get_verbs_start_with


class FresnoDailyNews(FresnoDailyNews_pb2_grpc.FresnoDailyNewsServicer):
    def ExtractKeyword(self, request, context):
        print("Got request " + str(request))
        return FresnoDailyNews_pb2.ExtractKeywordsResponse(reply=extract_keywords(request.message))


class FresnoDailyNewsGetVerbForms(FresnoDailyNewsGetVerbs_pb2_grpc.FresnoDailyNewsGetVerbsServicer):
    def GetVerbForms(self, request, context):
        print("Got request " + str(request))
        return FresnoDailyNewsGetVerbs_pb2.GetVerbFormsResponse(reply=get_verb_forms(request.message))


class FresnoDailyNewsGetVerbsStartWith(
    FresnoDailyNewsGetVerbsStartWith_pb2_grpc.FresnoDailyNewsGetVerbsStartWithServicer):
    def GetVerbsStartWith(self, request, context):
        print("Got request " + str(request))
        return FresnoDailyNewsGetVerbsStartWith_pb2.GetVerbsStartWithResponse(
            reply=get_verbs_start_with(request.message))


def server():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    FresnoDailyNews_pb2_grpc.add_FresnoDailyNewsServicer_to_server(FresnoDailyNews(), grpc_server)
    FresnoDailyNewsGetVerbs_pb2_grpc.add_FresnoDailyNewsGetVerbsServicer_to_server(FresnoDailyNewsGetVerbForms(),
                                                                                   grpc_server)
    FresnoDailyNewsGetVerbsStartWith_pb2_grpc.add_FresnoDailyNewsGetVerbsStartWithServicer_to_server(
        FresnoDailyNewsGetVerbsStartWith(),
        grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    print("Listening on port 50051...")
    grpc_server.start()
    grpc_server.wait_for_termination()
