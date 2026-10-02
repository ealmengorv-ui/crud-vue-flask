<template>
  <section>
    <h2>Productos</h2>
    <AlertMessage :message="mensaje" :type="tipoMensaje" />

    <form class="card form-grid" @submit.prevent="guardar">
      <BaseInput v-model="form.nombre" label="Nombre" :required="true" />
      <BaseInput v-model="form.descripcion" label="Descripción" />
      <BaseInput v-model="form.precio" label="Precio" type="number" min="0" step="0.01" :required="true" />
      <BaseInput v-model="form.stock" label="Stock" type="number" min="0" step="1" :required="true" />

      <label class="checkbox-field">
        <input v-model="form.activo" type="checkbox" />
        Producto activo
      </label>

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">
          {{ editando ? 'Actualizar' : 'Crear' }}
        </BaseButton>
        <BaseButton v-if="editando" variant="secondary" @click="cancelar">Cancelar</BaseButton>
      </div>
    </form>

    <DataTable :rows="productos" :columns="columns">
      <template #cell-precio="{ value }">Q{{ Number(value).toFixed(2) }}</template>
      <template #cell-activo="{ value }">{{ value ? 'Sí' : 'No' }}</template>
      <template #actions="{ row }">
        <BaseButton variant="secondary" @click="editar(row)">Editar</BaseButton>
        <BaseButton variant="danger" @click="eliminar(row)">Eliminar</BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const productos = ref([])
const mensaje = ref('')
const tipoMensaje = ref('error')
const guardando = ref(false)
const editando = ref(false)
const idEditando = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'precio', label: 'Precio' },
  { key: 'stock', label: 'Stock' },
  { key: 'activo', label: 'Activo' },
]

const form = reactive({ nombre: '', descripcion: '', precio: 0, stock: 0, activo: true })

function mostrar(texto, tipo = 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
}

function limpiar() {
  Object.assign(form, { nombre: '', descripcion: '', precio: 0, stock: 0, activo: true })
  editando.value = false
  idEditando.value = null
}

function validar() {
  if (!form.nombre.trim()) return 'El nombre es obligatorio'
  if (Number(form.precio) < 0) return 'El precio no puede ser negativo'
  if (Number(form.stock) < 0) return 'El stock no puede ser negativo'
  return ''
}

function payload() {
  return {
    nombre: form.nombre,
    descripcion: form.descripcion,
    precio: Number(form.precio),
    stock: Number(form.stock),
    activo: Boolean(form.activo),
  }
}

async function cargar() {
  try {
    productos.value = (await productosApi.listar()).data
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
      await productosApi.actualizar(idEditando.value, payload())
      mostrar('Producto actualizado correctamente', 'success')
    } else {
      await productosApi.crear(payload())
      mostrar('Producto creado correctamente', 'success')
    }
    limpiar()
    await cargar()
  } catch (err) {
    mostrar(err.message)
  } finally {
    guardando.value = false
  }
}

function editar(producto) {
  Object.assign(form, producto)
  editando.value = true
  idEditando.value = producto.id
  mensaje.value = ''
}

function cancelar() {
  limpiar()
  mensaje.value = ''
}

async function eliminar(producto) {
  if (!window.confirm(`¿Eliminar ${producto.nombre}?`)) return
  try {
    await productosApi.eliminar(producto.id)
    mostrar('Producto eliminado correctamente', 'success')
    await cargar()
  } catch (err) {
    mostrar(err.message)
  }
}

onMounted(cargar)
</script>
