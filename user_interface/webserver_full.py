import cherrypy
import sqlite3
import csv

DB_FILE = 'mydatabase.db'
columns = ['id', 'date', 'time', 'operator', 'shift', 'planned_time']

class MyWebApp(object):
    @cherrypy.expose
    def index(self):
        # Connect to the database and get a list of primary keys
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id FROM mytable")
        rows = c.fetchall()
        conn.close()

        # Build the HTML page with a dropdown list of primary keys
        html = """
        <html>
            <head>
                <title>AMCO</title>
            </head>
            <body>
                <h1>Equipment Utilization Dashboard</h1>
                <br>
                <br>
                <h2> Select Equipment </h2>
                <form action="/showtable">
                    <select name="id">
        """
        for row in rows:
            html += '<option value="%s">Equipment-%s</option>' % (row[0], row[0])
        html += """
                    </select>
                    <input type="submit" value="Go">
                </form>
                <p><a href="/add_index" target="_blank">Add Record</a></p>
                <p><a href="/update_index" target="_blank">Update Records</a></p>
                <p><a href="/show_all" target="_blank">All Records</a></p>
            </body>
        </html>
        """
        return html




    @cherrypy.expose
    def showtable(self, id):
        # Connect to the database and fetch the data for the selected primary key
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM mytable WHERE id=?", (id,))
        rows = c.fetchall()
        conn.close()

        # Build the HTML page with the table of data and a button to save as CSV
        html = """
        <html>
            <head>
                <title>Eq- %s Info.</title>
            </head>
            <body>
                <h1>Equipment- %s Dashboard</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Eq. ID</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Operator</th>
                            <th>Shift</th>
                            <th>Planned Time</th>
                            <th>Planned Stop</th>
                            
                        </tr>
                    </thead>
                    <tbody>
        """ % (id, id)
        for row in rows:
            html += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        html += """
                    </tbody>
                </table>
                <form action="/savetable">
                    <input type="hidden" name="id" value="%s">
                    <input type="submit" value="Save as CSV">
                </form>
                <p><a href="/">Go back to the main page</a></p>
            </body>
        </html>
        """ % id
        return html




    @cherrypy.expose
    def savetable(self, id):
        # Connect to the database and fetch the data for the selected primary key
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM mytable WHERE id=?", (id,))
        rows = c.fetchall()
        conn.close()

        # Build the CSV file
        filename = 'data_eqipment_%s.csv' % id
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            for row in rows:
                writer.writerow(row)

        # Return the CSV file as a download
        cherrypy.response.headers['Content-Type'] = 'text/csv'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % filename
        # return open
        raise cherrypy.HTTPRedirect('/')




    @cherrypy.expose
    def savetableall(self):
        # Connect to the database and fetch the data for the selected primary key
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM mytable")
        rows = c.fetchall()
        conn.close()

        # Build the CSV file
        filename = 'data_all.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columns)
            for row in rows:
                writer.writerow(row)

        # Return the CSV file as a download
        cherrypy.response.headers['Content-Type'] = 'text/csv'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="%s"' % filename
        # return open
        raise cherrypy.HTTPRedirect('/')






    @cherrypy.expose
    def update_index(self, id=None, date=None, time=None, operator=None, shift=None, planned_time=None):
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Handle form submission
        if cherrypy.request.method == 'POST':
            id = cherrypy.request.params['id']
            date = cherrypy.request.params['date']
            time = cherrypy.request.params['time']
            operator = cherrypy.request.params['operator']
            shift = cherrypy.request.params['shift']
            planned_time = cherrypy.request.params['planned_time']

            # Update the record in the database
            sql = "UPDATE mytable SET date=?, time=?, operator=?, shift=?, planned_time=? WHERE id=?"
            c.execute(sql, (date, time, operator, shift, planned_time, id))
            conn.commit()

        # Construct the HTML form
        html = "<form method='post'>"
        html += "<label for='id'>ID:</label>"
        html += "<input type='text' id='id' name='id'>"
        html += "<br>"
        html += "<label for='date'>Date:</label>"
        html += "<input type='date' id='date' name='date'>"
        html += "<br>"
        html += "<label for='time'>Time:</label>"
        html += "<input type='time' id='time' name='time'>"
        html += "<br>"
        html += "<label for='operator'>Operator:</label>"
        html += "<input type='text' id='operator' name='operator'>"
        html += "<br>"
        html += "<label for='shift'>Shift:</label>"
        html += "<input type='text' id='shift' name='shift'>"
        html += "<br>"
        html += "<label for='planned_time'>Planned Time:</label>"
        html += "<input type='text' id='planned_time' name='planned_time'>"
        html += "<br>"
        html += "<input type='submit' value='Update'>"
        html += "</form>"

        # Close the database connection
        conn.close()

        return html
        # Redirect the user back to the main page
        # raise cherrypy.HTTPRedirect('/')


    @cherrypy.expose
    def add_index(self):
        return '''
            <html>
            <head></head>
            <body>
                <form method="post" action="new_record">
                    <label for="date">Date:</label>
                    <input type="date" id="date" name="date"><br>

                    <label for="time">Time:</label>
                    <input type="time" id="time" name="time"><br>

                    <label for="operator">Operator:</label>
                    <input type="text" id="operator" name="operator"><br>

                    <label for="shift">Shift:</label>
                    <select id="shift" name="shift">
                        <option value="morning">Morning</option>
                        <option value="afternoon">Afternoon</option>
                        <option value="night">Night</option>
                    </select><br>

                    <label for="planned_time">Planned Time:</label>
                    <input type="text" id="planned_time" name="planned_time"><br>

                    <input type="submit">
                </form>
            </body>
            </html>
        '''

    @cherrypy.expose
    def new_record(self, date, time, operator, shift, planned_time):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO mytable (date, time, operator, shift, planned_time) VALUES (?, ?, ?, ?, ?)", (date, time, operator, shift, planned_time))
        conn.commit()
        conn.close()

        return "Record added successfully!"



    @cherrypy.expose
    def show_all(self, field=None):
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Get all the field names in the database
        c.execute("PRAGMA table_info(mytable)")
        field_names = [row[1] for row in c.fetchall()]

        # If a field was specified, filter the results by that field
        if field is not None and field in field_names:
            c.execute(f"SELECT * FROM mytable WHERE {field}=?", (field,))
        else:
            c.execute("SELECT * FROM mytable")

        # Generate the HTML table
        html = "<body> <table>"
        html += "<tr>"
        for name in field_names:
            html += f"<th>{name}</th>"
        html += "</tr>"
        for row in c.fetchall():
            html += "<tr>"
            for value in row:
                html += f"<td>{value}</td>"
            html += "</tr>"
        html += "<button onclick='downloadCSV()'>Download CSV</button>"
        html += "</table></body>"

        # Close the database connection
        conn.close()

        # Generate the HTML form for filtering
        # filter_form = "<form method='get' action='/'>"
        # filter_form += "Filter by field: "
        # filter_form += "<select name='field'>"
        # filter_form += "<option value=''>--Select a field--</option>"
        # for name in field_names:
        #     filter_form += f"<option value='{name}'>{name}</option>"
        # filter_form += "</select>"
        # filter_form += "<input type='submit' value='Filter'>"
        # filter_form += "</form>"

        # filter_form += "<form action='/savetableall'>"
        # filter_form += "<input type='submit' value='Save as CSV'>"
        # filter_form += "</form>"

        # Combine the HTML table and filter form
        filter_form = "<head>"
        filter_form += "<script>"
        filter_form += "function downloadCSV() {"
        filter_form += "var csv = '';"
        filter_form += "var rows = document.querySelectorAll('table tr');"
        filter_form += "for (var i = 0; i < rows.length; i++) {"
        filter_form += "var row = rows[i];"
        filter_form += "var cols = row.querySelectorAll('td, th');"
        filter_form += "for (var j = 0; j < cols.length; j++) {"
        filter_form += "var col = cols[j];"
        filter_form += "csv += col.textContent.trim() + ',';"
        filter_form += "}"
        filter_form += "csv += '\\n';"
        filter_form += "}"
        filter_form += "var link = document.createElement('a');"
        filter_form += "link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));"
        filter_form += "link.setAttribute('download', 'table.csv');"
        filter_form += "link.click();"
        filter_form += "}"
        filter_form += "</script>"
        filter_form += "</head>"

        html = filter_form + html

        return html
    



if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 9000
    })
    cherrypy.quickstart(MyWebApp())