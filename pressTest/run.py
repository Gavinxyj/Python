from modules.Scheduler import Scheduler
from modules.KafkaImpl import KafkaImpl

if __name__ == '__main__':
	scheduler = Scheduler()
	params = {'url':'192.168.103.61:9092', 'topic': 'doron_test1'}
	kafka = KafkaImpl(params)

	scheduler.do_scheduler(kafka)


	print 'main thread exit!'