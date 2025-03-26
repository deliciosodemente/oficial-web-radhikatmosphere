# Menú 3D Inmersivo con Fondo de Nubes Animadas

Este documento explica cómo funciona el menú 3D inmersivo implementado en la aplicación y cómo personalizarlo según tus necesidades.

## Componentes principales

El menú 3D inmersivo está compuesto por tres componentes principales:

1. **ImmersiveScene**: Componente principal que integra todo el sistema 3D
2. **CloudBackground**: Genera y anima las nubes en el fondo
3. **ImmersiveMenu**: Implementa el menú interactivo con animaciones

## Características

- Menú 3D completamente interactivo con animaciones suaves
- Fondo de nubes animadas en tiempo real
- Optimizaciones de rendimiento adaptativas
- Soporte para dispositivos móviles y de escritorio
- Efectos visuales avanzados (bloom, viñeta, etc.)
- Sistema de carga asíncrona con pantalla de carga

## Personalización

### Modificar elementos del menú

Para modificar los elementos del menú, edita el array `menuItems` en `src/components/ImmersiveMenu.js`:

```javascript
const menuItems = [
  { id: 'inicio', label: 'Inicio', position: [-3, 2, 0] },
  { id: 'servicios', label: 'Servicios', position: [-1, 2, 0] },
  { id: 'proyectos', label: 'Proyectos', position: [1, 2, 0] },
  { id: 'contacto', label: 'Contacto', position: [3, 2, 0] },
];
```

### Modificar apariencia de las nubes

Para modificar la apariencia de las nubes, puedes ajustar los parámetros en `src/components/CloudBackground.js`:

```javascript
// Crear múltiples nubes con posiciones aleatorias
for (let p = 0; p < 50; p++) {  // Cambiar número de nubes
  const cloud = new THREE.Mesh(cloudGeo, cloudMaterial);
  cloud.position.set(
    Math.random() * 800 - 400,  // Rango X
    500,                        // Altura inicial
    Math.random() * 500 - 500   // Rango Z
  );
  cloud.rotation.x = 1.16;
  cloud.rotation.y = -0.12;
  cloud.rotation.z = Math.random() * 2 * Math.PI;
  cloud.material.opacity = 0.55;  // Transparencia
  cloudParticlesRef.current.push(cloud);
  scene.add(cloud);
}
```

### Ajustar la cámara

Para ajustar la cámara y los controles, modifica las propiedades en `src/components/ImmersiveScene.js`:

```javascript
<PerspectiveCamera makeDefault position={[0, 0, 10]} fov={60} />
<OrbitControls 
  enableZoom={true}
  enablePan={false}
  minPolarAngle={Math.PI / 6}
  maxPolarAngle={Math.PI - Math.PI / 6}
  dampingFactor={0.1}
  rotateSpeed={0.5}
  zoomSpeed={0.7}
/>
```

### Personalizar efectos visuales

Para ajustar los efectos visuales, modifica la configuración en `AdaptiveQuality`:

```javascript
<EffectComposer multisampling={4}>
  <Bloom luminanceThreshold={0.2} intensity={1.0} />
  <Vignette eskil={false} offset={0.1} darkness={0.8} />
</EffectComposer>
```

## Optimizaciones

El menú está optimizado para un rendimiento óptimo mediante las siguientes técnicas:

1. **Culling de frustum**: Los objetos fuera de la vista no se renderizan
2. **Calidad adaptativa**: Se reduce la calidad en dispositivos de bajo rendimiento
3. **LOD (Level of Detail)**: Los objetos lejanos tienen menor detalle
4. **Carga diferida**: Las texturas y modelos se cargan solo cuando son necesarios

## Ejemplos de uso

### Vinculación con navegación

```javascript
const handleSelect = (id) => {
  setSelectedItem(id);
  
  // Navegar a la sección correspondiente
  switch(id) {
    case 'inicio':
      // Navegar a inicio
      break;
    case 'servicios':
      // Navegar a servicios
      break;
    // ... etc
  }
};
```

### Agregar nuevo elemento al menú

```javascript
// Agregar a menuItems
{ id: 'galeria', label: 'Galería', position: [5, 2, 0] }
```

## Solución de problemas

Si encuentras problemas de rendimiento:

1. Reduce el número de nubes (`CloudBackground.js`)
2. Disminuye la calidad de los efectos de postprocesamiento
3. Reduce la complejidad geométrica de los elementos del menú

## Requisitos del sistema

- Navegadores modernos con soporte WebGL2
- Dispositivos con GPU dedicada para mejor rendimiento
- Mínimo 4GB de RAM recomendado 