from rest_framework.views import APIView

from fluss_streams.models import Streams
from fluss_pipelines.models import Pipelines


class GetPipelinesListView(APIView):
    def post(self, request, *args, **kwargs):
        stream_name = self.request.POST.get("stream_name")
        pipeline_name = self.request.POST.get("pipeline_name")
        pipeline = Pipelines.objects.get(name=pipeline_name)
        servers = pipeline.fluss_servers.all()
        archives = [server.get_dvrs() for server in servers]
        print(archives)
