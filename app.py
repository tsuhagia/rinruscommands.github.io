from flask import Flask, render_template, request, redirect, send_from_directory
import os
import input_processing  # Assuming your script is named input_processing.py

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        driver_input = request.form['driver_input']
        output = input_processing.process_input(driver_input)
        with open("output.txt", "w") as f:
            f.write(output)

        return send_from_directory('.', 'output.txt', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
