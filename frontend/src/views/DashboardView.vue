<template>
  <section>
    <h2>Panel principal</h2>
    <p>Administra clientes, productos y pedidos desde las opciones superiores.</p>

    <div class="dashboard-grid">
      <RouterLink class="card dashboard-card" to="/clientes">
        <strong>Clientes</strong>
        <span>Crear, editar y eliminar clientes.</span>
      </RouterLink>
      <RouterLink class="card dashboard-card" to="/productos">
        <strong>Productos</strong>
        <span>Gestionar precios, stock y estado.</span>
      </RouterLink>
      <RouterLink class="card dashboard-card" to="/pedidos">
        <strong>Pedidos</strong>
        <span>Registrar pedidos y cambiar su estado.</span>
      </RouterLink>
    </div>
  </section>
</template>
