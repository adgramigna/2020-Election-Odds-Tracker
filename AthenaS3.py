
import boto3
import pandas as pd
import time
import s3fs

class s3_from_athena:

	@classmethod
	def athena_query(self, client, params):
		'''Querying Athena'''
		response = client.start_query_execution(
	        QueryString=params['query'],
	        QueryExecutionContext={
	            'Database': params['database']
	        },
	        ResultConfiguration={
	            'OutputLocation': 's3://' + params['bucket'] + '/' + params['path'],
	        },
	        
	    )
		return response

	@classmethod
	def make_public(self, s3, params, query_result, sleep_time):
		'''Makes result public'''
		time.sleep(sleep_time)
		object_acl = s3.ObjectAcl(params['bucket'],params['path']+'/'+query_result)
		object_acl.put(ACL='public-read')

	@classmethod
	def cleanup(self, s3, params, query_result):
		'''Deletes Result query from s3'''
		s3.Object(params['bucket'],params['path']+'/'+query_result).delete()
		s3.Object(params['bucket'],params['path']+'/'+query_result+'.metadata').delete()

	@classmethod
	def get_result(self, session, params, sleep_time=10):
		'''Obtains result of Athena query in dataframe form'''
		client = session.client('athena', region_name=params['region'])
		s3 = session.resource('s3')

		execution = self.athena_query(client, params)
		query_result = '{0}.csv'.format(execution['QueryExecutionId'])
		self.make_public(s3, params, query_result, sleep_time)
		df = pd.read_csv('s3://{0}/{1}/{2}'.format(params['bucket'], params['path'], query_result))
		self.cleanup(s3, params, query_result)
		return df
