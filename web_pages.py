from flask import session, render_template, url_for, redirect, Flask, escape, request
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'Scooby_Doo'

@app.route('/', methods=['POST','GET'])
def main():
    if request.method == 'POST':
        return render_template('homepage.html')
    else:
        return render_template('homepage.html')

@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        password = request.form['pswd']
        war = None
        print(user)

        if user == "":
            message = "Insira o nome de usuário"
            return render_template('login.html', war=message)
        if password == "":
            message = "Insira sua senha"
            return render_template('login.html', war=message)

        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT PSWD FROM CLIENTS WHERE NAME = ?", (user,))
        userdata =cur.fetchone()
        print(userdata)
        con.close()

        if userdata == None:
            message = "Usuário ainda não cadastrado"
            return render_template('login.html', war=message)

        if password == userdata[0]:
            session['username'] = user
            return redirect('/login/')
        else:
            message = "Senha errada"
            return render_template('login.html', war=message)

    else:
        if 'username' in session:
            username = session['username']
            message = "Usuário " + username + " conectado"
            return render_template('homepage.html', war=message)
        else:
            return render_template('login.html')

@app.route('/nice_guys/')
def bio():
    return render_template('nice_guys.html')

@app.route('/newplate/', methods=['POST','GET'])
def new_plate():
    username = session['username']
    war = None;
    if username == None:
        message = "Nenhum usuário logado"
        return render_template('homepage.html', war=message)
    if request.method == 'POST':
        newplate = request.form['newplate']
        newplate = newplate.upper()
        autent = request.form['master_pswd']

        if autent != "sel373#":
            message = "Autenticação falhou - Procure nossa assitência"
            return render_template('form_newplate.html', war=message)

        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM PLATES WHERE PLATE = ?", (newplate,))
        platedata = cur.fetchone()

        if len(newplate) != 7:
            message = "Placa inválida"
            return render_template('form_newplate.html', war=message)

        letras = newplate[0:3]
        numeros = newplate[3:7]

        print(letras)
        print(numeros)

        #testa de os 3 primeiros são letras e os 4 últimos são números
        if not letras.isalpha() or not numeros.isdigit():
            message = "Placa inválida"
            return render_template('form_newplate.html', war=message)            

        if platedata == None:
            cur.execute("INSERT INTO PLATES (PLATE, NAME) VALUES (?,?)", (newplate, username))
            con.commit()
            con.close()

            message = "Placa " + newplate + " associada a " + username
            return render_template('form_newplate.html', war=message)

        else:
            con.rollback()
            con.close()
            message = "Placa " + newplate + " já cadastrada"
            return render_template('homepage.html', war=message)

    else:
        return render_template('form_newplate.html')

@app.route('/lista/')
def lista():
    username = session['username']
    if username == None:
        message = "Nenhum usuário conectado"
        return render_template('homepage.html', war=message)
    else:
        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM PLATES WHERE NAME = ?", (username,))
        platedata = cur.fetchall()
        con.close()

        if platedata == None:
            message = "Nenhuma placa registrada para o usuário " + username
            return render_template('listar.html', war=message)

        return render_template('listar.html', platedata=platedata)

@app.route('/logout/')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return render_template('homepage.html')

    message = "Ninguém estava logado"
    return render_template('homepage.html', war=message)

@app.route('/cadastrar/', methods=['POST','GET'])
def cadastrar():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pswd']
        conf_pass = request.form['pswd2']

        if password != conf_pass:
            message = "As senhas estão diferentes"
            return render_template('cadastrar.html', war=message)

        if not username.isalpha():
            message = "Nome de usuário inválido"
            return render_template('cadastrar.html', war=message)

        con = sql.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM CLIENTS WHERE NAME = ?", (username,))
        userdata = cur.fetchone()

        if userdata == None:
            cur.execute("INSERT INTO CLIENTS (NAME, PSWD) VALUES (?,?)", (username,password))
            con.commit()
            con.close()
            message = "Registro efetuado com sucesso!"
            return render_template('cadastrar.html', war=message)
        else:
            con.rollback()
            con.close()
            message = "Usuário já existe"
            return render_template('cadastrar.html',war=message)

    else:
        return render_template('cadastrar.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
