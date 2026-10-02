<template>
  <section>
    <h2>Pedidos</h2>
    <AlertMessage :message="mensaje" :type="tipoMensaje" />

    <form class="card form-grid" @submit.prevent="crear">
      <label class="field">
        <span>Cliente</span>
        <select v-model.number="form.cliente_id" required>
          <option disabled value="">Seleccione un cliente</option>
          <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
            {{ cliente.nombre }}
          </option>
        </select>
      </label>

      <label class="field">
        <span>Producto</span>
        <select v-model.number="form.producto_id" required>
          <option disabled value="">Seleccione un producto</option>
          <option
            v-for="producto in productosActivos"
            :key="producto.id"
            :value="producto.id"
          >
            {{ producto.nombre }} — Q{{ Number(producto.precio).toFixed(2) }} — stock {{ producto.stock }}
          </option>
        </select>
      </label>

      <BaseInput v-model="form.cantidad" label="Cantidad" type="number" min="1" step="1" :required="true" />

      <div class="form-actions">
        <BaseButton type="submit" :disabled="guardando">Crear pedido</BaseButton>
      </div>
    </form>

    <DataTable :rows="pedidos" :columns="columns">
      <template #cell-total="{ value }">Q{{ Number(value).toFixed(2) }}</template>
      <template #cell-estado="{ row }">
        <select :value="row.estado" @change="cambiarEstado(row, $event.target.value)">
          <option value="pendiente">Pendiente</option>
          <option value="pagado">Pagado</option>
          <option value="enviado">Enviado</option>
          <option value="cancelado">Cancelado</option>
        </select>
      </template>
      <template #actions="{ row }">
        <BaseButton variant="danger" :disabled="row.estado !== 'cancelado'" @click="eliminar(row)">
          Eliminar
        </BaseButton>
      </template>
    </DataTable>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { clientesApi } from '../api/clientes'
import { pedidosApi } from '../api/pedidos'
import { productosApi } from '../api/productos'
import AlertMessage from '../components/AlertMessage.vue'
import BaseButton from '../components/BaseButton.vue'
import BaseInput from '../components/BaseInput.vue'
import DataTable from '../components/DataTable.vue'

const clientes = ref([])
const productos = ref([])
const pedidos = ref([])
const mensaje = ref('')
const tipoMensaje = ref('error')
const guardando = ref(false)

const form = reactive({ cliente_id: '', producto_id: '', cantidad: 1 })
const productosActivos = computed(() => productos.value.filter((p) => p.activo && p.stock > 0))

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'cliente', label: 'Cliente' },
  { key: 'producto', label: 'Producto' },
  { key: 'cantidad', label: 'Cantidad' },
  { key: 'total', label: 'Total' },
  { key: 'estado', label: 'Estado' },
]

function mostrar(texto, tipo = 'error') {
  mensaje.value = texto
  tipoMensaje.value = tipo
}

async function cargar() {
  try {
    const [clientesRes, productosRes, pedidosRes] = await Promise.all([
      clientesApi.listar(),
      productosApi.listar(),
      pedidosApi.listar(),
    ])
    clientes.value = clientesRes.data
    productos.value = productosRes.data
    pedidos.value = pedidosRes.data
  } catch (err) {
    mostrar(err.message)
  }
}

async function crear() {
  if (!form.cliente_id || !form.producto_id) return mostrar('Seleccione cliente y producto')
  if (Number(form.cantidad) <= 0) return mostrar('La cantidad debe ser mayor que cero')

  guardando.value = true
  try {
    await pedidosApi.crear({
      cliente_id: Number(form.cliente_id),
      producto_id: Number(form.producto_id),
      cantidad: Number(form.cantidad),
    })
    Object.assign(form, { cliente_id: '', producto_id: '', cantidad: 1 })
    mostrar('Pedido creado correctamente', 'success')
    await cargar()
  } catch (err) {
    mostrar(err.message)
  } finally {
    guardando.value = false
  }
}

async function cambiarEstado(pedido, estado) {
  try {
    await pedidosApi.actualizar(pedido.id, { estado })
    mostrar('Estado actualizado', 'success')
    await cargar()
  } catch (err) {
    mostrar(err.message)
  }
}

async function eliminar(pedido) {
  if (!window.confirm(`¿Eliminar el pedido #${pedido.id}?`)) return
  try {
    await pedidosApi.eliminar(pedido.id)
    mostrar('Pedido eliminado correctamente', 'success')
    await cargar()
  } catch (err) {
    mostrar(err.message)
  }
}

onMounted(cargar)
</script>
