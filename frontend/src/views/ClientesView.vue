<template>
  <section>
    <h2>Clientes</h2>
    <AlertMessage :message="mensaje" :type="tipoMensaje" />

    <form class="card form-grid" @submit.prevent="guardar">
      <BaseInput v-model="form.nombre" label="Nombre" :required="true" />
      <BaseInput v-model="form.correo" label="Correo" type="email" :required="true" />
      <BaseInput v-model="form.telefono" label="Teléfono" />

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="cancelar">Cancelar</BaseButton>
      </div>
    </form>

    <DataTable :rows="clientes" :columns="columns">
      <template #actions="{ row }">
        <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const clientes = ref([])
const mensaje = ref('')
const tipoMensaje = ref('error')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'correo', label: 'Correo' },
  { key: 'telefono', label: 'Teléfono' },
]

const form = reactive({ nombre: '', correo: '', telefono: '' })

function mostrar(texto, tipo = 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
}

function limpiar() {
  Object.assign(form, { nombre: '', correo: '', telefono: '' })
  editando.value = false
  idEditando.value = null
}

function validar() {
  if (!form.nombre.trim()) return 'El nombre es obligatorio'
  if (!form.correo.trim() || !form.correo.includes('@')) return 'Ingrese un correo válido'
  return ''
}

async function cargar() {
  try {
    clientes.value = (await clientesApi.listar()).data
  } catch (err) {
    mostrar(err.message)
  }
}

async function guardar() {
  const validacion = validar()
  if (validacion) return mostrar(validacion)

  mensaje.value = ''
  guardando.value = true
  try {
    if (editando.value) {
      await clientesApi.actualizar(idEditando.value, form)
      mostrar('Cliente actualizado correctamente', 'success')
    } else {
      await clientesApi.crear(form)
      mostrar('Cliente creado correctamente', 'success')
    }
    limpiar()
    await cargar()
  } catch (err) {
    mostrar(err.message)
  } finally {
    guardando.value = false
  }
}

function editar(cliente) {
  Object.assign(form, cliente)
  editando.value = true
  idEditando.value = cliente.id
  mensaje.value = ''
}

function cancelar() {
  limpiar()
  mensaje.value = ''
}

async function eliminar(cliente) {
  if (!window.confirm(`¿Eliminar a ${cliente.nombre}?`)) return
  try {
    await clientesApi.eliminar(cliente.id)
    mostrar('Cliente eliminado correctamente', 'success')
    await cargar()
  } catch (err) {
    mostrar(err.message)
  }
}

onMounted(cargar)
</script>
