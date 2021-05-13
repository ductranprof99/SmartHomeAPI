from celery import Celery

app = Celery('SmartHomeAPI',
             include=['SmartHomeAPI.tasks'])
            #  broker='amqp://',
            #  backend='rpc://',

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()