from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField,DateField,TimeField
from datetime import date
import datetime
import google_api
import google_api_insert
from dateutil.parser import parse
import json

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class EventForm(Form):
    eventTitle = TextField(validators=[validators.required()])
    eventDate = DateField(validators=[validators.required()])
    eventTime = TimeField(validators=[validators.required()])

def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(eventTitle, eventDate, eventTime):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, eventTitle={},eventDate={}, eventTime={} \n'.format(timestamp, eventTitle, eventDate, eventTime))
    data.close()
@app.template_filter('dateonly')
def _jinja2_filter_datetime(date, fmt='%b %d, %Y'):
    date = parse(date)
    native = date.replace(tzinfo=None)
    return native.strftime(fmt)

@app.template_filter('timeonly')
def _jinja2_filter_datetime(date, fmt="%H:%M"):
    dateObj = parse(date)
    #timeonly = "{}:{}:{}".format(dateObj.hour, dateObj.minute, dateObj.second)
    #return timeonly
    native = dateObj.replace(tzinfo=None)
    return native.strftime(fmt)

@app.route('/event/<event_id>',methods=['GET', 'POST'])
def edit_event(event_id):
    event = None;
    events = google_api.get_events()
    for i in events:
        if i["id"] == event_id:
            event = i
    return redirect(url_for('event_data', event=event["id"]))

@app.route('/event-edit/<event_id>',methods=['GET', 'POST'])
def edit_save_event(event_id):
    event_id =request.args.get('event_id')
    eventTitle = request.form['eventTitle']
    eventDate = request.form['eventDate']
    eventTime = request.form['eventTime']
    final_event = google_api.update_event(event_id,eventTitle,eventDate,eventTime)
    return redirect(url_for('event_data'))

@app.route('/event-delete/<event_id>',methods=['GET', 'POST'])
def delete_event(event_id):
    print(request.method)
    dlt_event=google_api_insert.delete_event(event_id)
    return redirect(url_for('event_data'))

@app.route("/", methods=['GET', 'POST'])
def event_data(event=None):
    form = EventForm(request.form)
    event_for_edit = request.args.get('event')
    final_event= None

    if event_for_edit is not None:
        print(event_for_edit)
        final_event = google_api.get_event_by_id(event_for_edit)
    #print(form.errors)
    if request.method == 'POST':
        eventTitle=request.form['eventTitle']
        eventDate=request.form['eventDate']
        eventTime=request.form['eventTime']

        if form.validate():
            if request.form['submit_button'] == '' :
                print("NEW EVENT Inserted")
                new_events=google_api_insert.create_event(eventTitle,eventDate,eventTime)
                flash('Event Created : {} {} {}'.format(eventTitle, eventDate,eventTime))
            else:
                print(" EVENT Updated")
                event_id = request.form['submit_button']
                eventTitle = request.form['eventTitle']
                eventDate = request.form['eventDate']
                eventTime = request.form['eventTime']
                google_api.update_event(event_id, eventTitle, eventDate, eventTime)
                flash('Event Updated : {} {} {}'.format(eventTitle, eventDate, eventTime))
                return redirect(url_for('event_data'))
        else:
            flash('Error: All Fields are Required')

    events = google_api.get_events()

    return render_template('events.html', form=form,events=events, event=final_event)

if __name__ == "__main__":
    app.run()