from prometheus_client.core import Metric

from taz.consumers.core.database.mongodb import MongodbMixin


class MetricsCollector(MongodbMixin):

    def collect(self):

        metric_values = self.get_collection('metrics').find({})
        for metric_row in metric_values:
            metric_row.pop('_id')

            metric = Metric(metric_row['type'], metric_row['type'], 'summary')

            metric.add_sample(
                name='taz_{}'.format(metric_row['type']),
                value=int(metric_row['value']),
                labels={}
            )
            yield metric
