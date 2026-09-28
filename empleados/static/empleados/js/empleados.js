let busquedaActual = "";

document.getElementById("buscar").addEventListener("input", function () {

    const busquedaActual = this.value;

    cargarEmpleados(busquedaActual, 1);

});


function crearPaginacion(paginaActual, totalPaginas, tieneAnterior, tieneSiguiente, buscar) {

    const paginacion = document.getElementById("paginacion");

    let html = `
                    <div class="d-flex justify-content-center">
                        <div class="btn-group">
                `;

    // Botón anterior
    if (tieneAnterior) {

        html += `
            <button
                class="btn btn-outline-primary"
                onclick="cargarEmpleados('${buscar}', ${paginaActual - 1})"
            >
                ← Anterior
            </button>
        `;
    }

    // Números de página
    for (let pagina = 1; pagina <= totalPaginas; pagina++) {

        if (pagina === paginaActual) {

            html += `
                <button
                    class="btn btn-primary"
                    onclick="cargarEmpleados('${buscar}', ${pagina})"
                >
                    ${pagina}
                </button>
            `;

        } else {

            html += `
                <button
                    class="btn btn-outline-primary"
                    onclick="cargarEmpleados('${buscar}', ${pagina})"
                >
                    ${pagina}
                </button>
            `;
        }
    }

    // Botón siguiente
    if (tieneSiguiente) {

        html += `
            <button
                class="btn btn-outline-primary"
                onclick="cargarEmpleados('${buscar}', ${paginaActual + 1})"
            >
                Siguiente →
            </button>
        `;
    }

    html += `
            </div>
        </div>
    `;

    paginacion.innerHTML = html;
}

cargarEmpleados();

async function cerrarSesion() {
    const response = await fetch("/api/empleados/logout/", {
        method: "POST",
    });

    if (response.ok) {
        window.location.href = "/empleados/login/";
    }
}


function validarTexto(nombreCampo, elemento) {

    const valor = elemento.value.trim();

    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/.test(valor)) {
        elemento.classList.add("is-invalid");
        return false;
    }

    elemento.classList.remove("is-invalid");
    return true;
}

//modal crear empleado

const modalCrearEmpleado = document.getElementById("modalCrearEmpleado");

modalCrearEmpleado.addEventListener("hidden.bs.modal", function () {

    const form = document.getElementById("formCrearEmpleado");

    form.reset();

    form.querySelectorAll(".is-invalid").forEach(function (campo) {
        campo.classList.remove("is-invalid");
    });
});

async function crearEmpleado() {

    const form = document.getElementById("formCrearEmpleado");

    const datos = {
        nombre: document.getElementById("crear_nombre").value,
        apellido: document.getElementById("crear_apellido").value,
        documento: document.getElementById("crear_documento").value,
        correo: document.getElementById("crear_correo").value,
        telefono: document.getElementById("crear_telefono").value
    }

    const botonGuardar = document.querySelector("#modalCrearEmpleado .btn-success");

    botonGuardar.disabled = true;
    botonGuardar.textContent = "Guardando...";

    const response = await fetch("/api/empleados/crear/", {
        method: "POST",
        headers: {
                    "Content-Type": "application/json"
        },
        body: JSON.stringify(datos)
    });
    
    const resultado = await response.json();

    botonGuardar.disabled = false;
    botonGuardar.textContent = "Guardar";

    if(!response.ok) {
        mostrarMensaje(resultado.error || "No se pudo crear el empleado.", "danger");
        return;
    }

    const modalElement = document.getElementById("modalCrearEmpleado");

    const modal = bootstrap.Modal.getInstance(modalElement);
    
    modal.hide();

    form.reset();

    mostrarMensaje("Empleado creado correctamente.", "success");

    cargarEmpleados();

}

const nombre = document.getElementById("crear_nombre");

nombre.addEventListener("input", function () {

    if (!this.checkValidity() || !/^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/.test(this.value.trim())) {
        this.classList.add("is-invalid");
        return;
    }

    this.classList.remove("is-invalid");
});

const apellido = document.getElementById("crear_apellido");

apellido.addEventListener("input", function () {

    if (!this.checkValidity() || !/^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/.test(this.value.trim())) {
        this.classList.add("is-invalid");
        return;
    }

    this.classList.remove("is-invalid");
});

const documento = document.getElementById("crear_documento");

documento.addEventListener("input", function () {
    if (!this.checkValidity() || !/^\d+$/.test(this.value.trim())){
        this.classList.add("is-invalid");
        return;
    }
    this.classList.remove("is-invalid");
});

const correo = document.getElementById("crear_correo");

correo.addEventListener("input", function () {

    if (!this.checkValidity()) {
        this.classList.add("is-invalid");
        return;
    }

    this.classList.remove("is-invalid");
});

const telefono= document.getElementById("crear_telefono");

telefono.addEventListener("input", function () {

    if (!this.checkValidity() || !/^\d{10}$/.test(this.value.trim())) {
        this.classList.add("is-invalid");
        return;
    }

    this.classList.remove("is-invalid");
});

async function abrirModalEditar(id) {

    const response = await fetch(
        `/api/empleados/${id}/`
    );

    if (!response.ok) {
        mostrarMensaje("No fue posible obtener el empleado.", "danger");
        return;
    }

    const empleado = await response.json();

    document.getElementById("editar_nombre").value = empleado.nombre;
    document.getElementById("editar_apellido").value = empleado.apellido;
    document.getElementById("editar_documento").value = empleado.documento;
    document.getElementById("editar_correo").value = empleado.correo;
    document.getElementById("editar_telefono").value = empleado.telefono;

    document.getElementById("formEditarEmpleado").dataset.id = id;

    const modal = new bootstrap.Modal(document.getElementById("modalEditarEmpleado"));

    modal.show();
}

async function guardarEdicion () {

    const form = document.getElementById("formEditarEmpleado");

    const id = form.dataset.id;

    const datos = {
        nombre: document.getElementById("editar_nombre").value,
        apellido: document.getElementById("editar_apellido").value,
        documento: document.getElementById("editar_documento").value,
        correo: document.getElementById("editar_correo").value,
        telefono: document.getElementById("editar_telefono").value
    };

    const botonGuardar = document.querySelector("#modalEditarEmpleado .btn-primary");

    botonGuardar.disabled = true;
    botonGuardar.textContent = "Guardando...";

    const response = await fetch(

        `/api/empleados/${id}/`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        }
    );

    const resultado = await response.json();
    
    botonGuardar.disabled = false;
    botonGuardar.textContent = "Guardar cambios";

    if (!response.ok) {
        mostrarMensaje( resultado.error || "No fue posible actualizar el empleado.", "danger");
        return;
    }

    const modalElement = document.getElementById("modalEditarEmpleado");

    const modal = bootstrap.Modal.getInstance(modalElement);

    modal.hide();

    form.reset();

    mostrarMensaje("Empleado actualizado correctamente.", "success");

    document.getElementById("buscar").value = busquedaActual;

    cargarEmpleados(busquedaActual, 1);
}



async function eliminarEmpleado(id) {

    const modalElement = document.getElementById("modalConfirmarEliminar");

    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);

    const botonConfirmar = document.getElementById("btnConfirmarEliminar");

    botonConfirmar.onclick = async function () {

        botonConfirmar.disabled = true;
        botonConfirmar.textContent = "Eliminando...";

        const response = await fetch(
            `/api/empleados/${id}/`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            botonConfirmar.disabled = false;
            botonConfirmar.textContent = "Eliminar";

            mostrarMensaje("No fue posible eliminar el empleado.", "danger");
            return;
        }

        modal.hide();

        mostrarMensaje("Empleado eliminado correctamente.", "success");

        cargarEmpleados(busquedaActual, 1);
    };

    modal.show();
}

async function abrirModalVer(id) { 
    
    const response = await fetch( `/api/empleados/${id}/` ); 
    
    if (!response.ok) { 
        mostrarMensaje("No fue posible obtener el empleado.", "danger"); 
    
    return;
    } 

    const empleado = await response.json(); 
    document.getElementById("ver_id").textContent = empleado.id; 
    document.getElementById("ver_nombre").textContent = empleado.nombre; 
    document.getElementById("ver_apellido").textContent = empleado.apellido; 
    document.getElementById("ver_documento").textContent = empleado.documento; 
    document.getElementById("ver_correo").textContent = empleado.correo; 
    document.getElementById("ver_telefono").textContent = empleado.telefono; 

    const modal = new bootstrap.Modal( document.getElementById("modalVerEmpleado") ); 

    modal.show(); 

}

function mostrarMensaje(mensaje, tipo = "success") {

    const toastElement = document.getElementById("toastMensaje");

    const toastText = document.getElementById("toastText");

    toastTexto.textContent = mensaje;

    toastElement.classList.remove(
        "text-bg-success",
        "text-bg.danger"
    );

    toastElement.classList.add(
        `text-bg-${tipo}`
    );

    const toast = bootstrap.Toast.getOrCreateInstance(toastElement);

    toast.show();
}

async function cargarEmpleados(buscar = "", pagina = 1) {

    const tbody = document.getElementById("tabla-empleados");
    const mensaje = document.getElementById("mensaje");
    const paginacion = document.getElementById("paginacion");
    
    tbody.innerHTML = `
                        <tr>
                            <td colspan="7" class="text-center">
                                Cargando empleados...
                            </td>
                        </tr>
                    `;

    const response = await fetch(
        `/api/empleados/?buscar=${encodeURIComponent(buscar)}&pagina=${pagina}`
    );

    if (!response.ok) {
        console.error("Error al cargar empleados");
        return;
    }

    const resultado = await response.json();

    tbody.innerHTML = "";

    try {

        let url = `/api/empleados/?pagina=${pagina}`;

        if (buscar.trim() !== "") {
            url += `&buscar=${encodeURIComponent(buscar)}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("No se pudieron cargar los empleados.");
        }

        const resultado = await response.json();
        
        const empleados = resultado.empleados;

        if (empleados.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center">
                        No se encontraron empleados.
                    </td>
                </tr>
            `;
            paginacion.innerHTML = "";

            return;
        }

        tbody.innerHTML = "";

        resultado.empleados.forEach(empleado => {

            tbody.innerHTML += `
                <tr>
                <td>${empleado.id}</td>
                <td>${empleado.nombre}</td>
                <td>${empleado.apellido}</td>
                <td>${empleado.documento}</td>
                <td>${empleado.correo}</td>
                <td>${empleado.telefono}</td>
                <td>
                    <button
                        type="button"
                        class="btn btn-sm btn-primary"
                        onclick="abrirModalVer(${empleado.id})">
                        Ver
                    </button>
                    <button
                        type="button"
                        class="btn btn-sm btn-warning"
                        onclick="abrirModalEditar(${empleado.id})">
                        Editar
                    </button>
                    <button
                        type="button"
                        class="btn btn-sm btn-danger"
                        onclick="eliminarEmpleado(${empleado.id})">
                        Eliminar
                    </button>
                </td>
            </tr>
        `;
        });

        crearPaginacion(
            resultado.pagina_actual,
            resultado.total_paginas,
            resultado.tiene_anterior,
            resultado.tiene_siguiente,
            buscar  
        );

    } catch (error) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                ${error.message}
            </div>
        `;
    }
}

