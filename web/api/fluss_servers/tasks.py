from django_app.celery import app

@app.task
def send_span_email():
    print("hi")