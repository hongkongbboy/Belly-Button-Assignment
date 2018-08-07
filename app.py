# import necessary libraries
import pandas as pd
import numpy as np
import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import (
    Flask,
    render_template,
    jsonify,
    request)
from flask_sqlalchemy import SQLAlchemy

#Set up Flask
app = Flask(__name__)

#Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)

#Bring out table
tableGraph = automap_base()
tableGraph.prepare(db, reflect=True)

table_Metadata = tableGraph.classes.tables_metadata
OTU = tableGraph.classes.otu
table = tableGraph.classes.tables

session = Session(db)

#Set up route
@app.route("/")
def home():
    return """Return the dashboard homepage."""

#Return a list of name
@app.route('/names')
def names():
    name_list = session.query(table).statement
    dataframe = pd.read_sql_query()
    dataframe.set_index('otu_id', inplace=True)
    return jsonify(list(dataframe.columns))

#Return a list of OTU descriptions
@app.route('/otu')
def otu():
    responses = session.query(OTU.list_of_item).all()
    otu_list = list(np.ravel(responses))
    return jsonify(otu_list)

#Return a json dictorary of sample metadata
@app.route('/metadata/<sample>')
def sample_metadata(sample):
    appendList = [table_Metadata.AGE, table_Metadata.BBTYPE, table_Metadata.ETHNICITY, table_Metadata.GENDER, table_Metadata.LOCATION, table_Metadata.SAMPLEID]
    responses = session.query(*appendList).\
        filter(table_Metadata.SAMPLEID == sample[3:]).all()
    
    tables_metadata = {}
    for response in responses:
        tables_metadata['AGE'] = result[0]
        tables_metadata['BBTYPE'] = result[1]
        tables_metadata['ETHNICITY'] = result[2]
        tables_metadata['GENDER'] = result[3]
        tables_metadata['LOCATION'] = result[4]
        tables_metadata['SAMPLEID'] = result[5]

    return jsonify(tables_metadata)

#Return an integer value for the weekly washing frequency 'WFREQ'
@app.route('/wfreq/<sample')
def sample_wfreq(table):
    responses = session.query(table_Metadata.WFREQ).\
        filter(table_Metadata.SAMPLEID == table[3:]).all()
    wfreq = np.ravel(responses)
    return jsonify(int(wfreq[0]))

#Return a list of dictionaries containing sorted lists
@app.route('/samples/<sample>')
    def tables(sample):
        name_list = session.query(table).statement
        df = pd.read_sql_query(stmt, session.bind)

        if sample not in df.columns:
            return jsonify(f"Not working. Please check the code."), 400
        df = df[df[samle] > 1]
        df = df.sort_values(by=sample, ascending = 0)

        data = [{
            "otu_ids": df[sample].index.values.tolist(),
            "sample_values": df[sample].values.tolist()
        }]
        return jsonify(data)



if __name__ == "__main__":
    app.run()