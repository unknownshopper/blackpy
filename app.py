from flask import Flask, render_template, request, redirect, url_for, flash, session
from directorio_empleados import DirectorioEmpleados
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para las sesiones y mensajes flash

# Inicializar el directorio de empleados
directorio = DirectorioEmpleados()

@app.route('/')
def index():
    """Página principal que redirige al login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión"""
    if request.method == 'POST':
        tipo_usuario = request.form.get('tipo_usuario')
        
        if tipo_usuario == 'admin':
            password = request.form.get('password')
            if password == 'admin123':
                session['es_admin'] = True
                flash('Inicio de sesión como administrador exitoso', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta', 'danger')
        elif tipo_usuario == 'usuario':
            session['es_admin'] = False
            flash('Inicio de sesión como usuario regular exitoso', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    session.pop('es_admin', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Muestra el panel principal según el tipo de usuario"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', es_admin=session['es_admin'])

@app.route('/empleados')
def listar_empleados():
    """Muestra la lista completa de empleados (solo para administradores)"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if not session['es_admin']:
        flash('No tiene permisos para ver la lista completa', 'danger')
        return redirect(url_for('dashboard'))
    
    empleados = directorio.listar_todos()
    return render_template('empleados.html', empleados=empleados)

@app.route('/empleados/agregar', methods=['GET', 'POST'])
def agregar_empleado():
    """Permite agregar un nuevo empleado (solo para administradores)"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if not session['es_admin']:
        flash('No tiene permisos para agregar empleados', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cargo = request.form.get('cargo')
        departamento = request.form.get('departamento')
        
        if nombre and apellido and cargo and departamento:
            empleado = directorio.agregar_empleado(nombre, apellido, cargo, departamento)
            flash(f'Empleado agregado exitosamente con ID: {empleado["id"]}', 'success')
            return redirect(url_for('listar_empleados'))
        else:
            flash('Todos los campos son obligatorios', 'danger')
    
    return render_template('agregar_empleado.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_empleados():
    """Permite buscar empleados por diferentes criterios"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    resultados = []
    criterio = None
    valor = None
    
    if request.method == 'POST':
        criterio = request.form.get('criterio')
        valor = request.form.get('valor')
        
        if criterio and valor:
            if criterio == 'nombre':
                resultados = directorio.buscar_por_nombre(valor)
            elif criterio == 'departamento':
                resultados = directorio.buscar_por_departamento(valor)
            elif criterio == 'cargo':
                resultados = directorio.buscar_por_cargo(valor)
    
    return render_template('buscar.html', resultados=resultados, criterio=criterio, valor=valor)

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    """Permite editar un empleado existente (solo para administradores)"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if not session['es_admin']:
        flash('No tiene permisos para editar empleados', 'danger')
        return redirect(url_for('dashboard'))
    
    empleado = directorio.buscar_por_id(id)
    if not empleado:
        flash('Empleado no encontrado', 'danger')
        return redirect(url_for('listar_empleados'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cargo = request.form.get('cargo')
        departamento = request.form.get('departamento')
        fecha_ingreso = request.form.get('fecha_ingreso')
        
        # Actualizar campos básicos
        if nombre and apellido and cargo and departamento and fecha_ingreso:
            empleado['nombre'] = nombre
            empleado['apellido'] = apellido
            empleado['cargo'] = cargo
            empleado['departamento'] = departamento
            empleado['fecha_ingreso'] = fecha_ingreso
            
            # Actualizar campos de despido si existen
            if 'fecha_despido' in request.form and request.form.get('fecha_despido'):
                empleado['fecha_despido'] = request.form.get('fecha_despido')
                
            if 'motivo_despido' in request.form:
                empleado['motivo_despido'] = request.form.get('motivo_despido')
            
            directorio.guardar_datos()
            flash('Empleado actualizado exitosamente', 'success')
            return redirect(url_for('listar_empleados'))
        else:
            flash('Todos los campos son obligatorios', 'danger')
    
    return render_template('editar_empleado.html', empleado=empleado)

@app.route('/empleados/eliminar/<int:id>')
def eliminar_empleado(id):
    """Permite eliminar un empleado (solo para administradores)"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if not session['es_admin']:
        flash('No tiene permisos para eliminar empleados', 'danger')
        return redirect(url_for('dashboard'))
    
    if directorio.eliminar_empleado(id):
        flash('Empleado eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el empleado', 'danger')
    
    return redirect(url_for('listar_empleados'))

@app.route('/empleados/despido/<int:id>', methods=['GET', 'POST'])
def registrar_despido(id):
    """Permite registrar el despido de un empleado (solo para administradores)"""
    if 'es_admin' not in session:
        flash('Debe iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    
    if not session['es_admin']:
        flash('No tiene permisos para registrar despidos', 'danger')
        return redirect(url_for('dashboard'))
    
    empleado = directorio.buscar_por_id(id)
    if not empleado:
        flash('Empleado no encontrado', 'danger')
        return redirect(url_for('listar_empleados'))
    
    if empleado.get('fecha_despido'):
        flash('Este empleado ya ha sido despedido', 'warning')
        return redirect(url_for('listar_empleados'))
    
    if request.method == 'POST':
        fecha_despido = request.form.get('fecha_despido')
        motivo_despido = request.form.get('motivo_despido')
        
        if motivo_despido == 'Otro':
            otro_motivo = request.form.get('otro_motivo')
            if otro_motivo:
                motivo_despido = otro_motivo
        
        if fecha_despido and motivo_despido:
            if directorio.registrar_despido(id, fecha_despido, motivo_despido):
                flash('Despido registrado exitosamente', 'success')
                return redirect(url_for('listar_empleados'))
        else:
            flash('Todos los campos son obligatorios', 'danger')
    
    return render_template('registrar_despido.html', empleado=empleado)

if __name__ == '__main__':
    app.run(debug=True)