import React, { useRef, useState, useEffect } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Text, Html, useTexture } from '@react-three/drei';
import * as THREE from 'three';
import { gsap } from 'gsap';

// Opciones del menú
const menuItems = [
  { id: 'inicio', label: 'Inicio', position: [-3, 2, 0] },
  { id: 'servicios', label: 'Servicios', position: [-1, 2, 0] },
  { id: 'proyectos', label: 'Proyectos', position: [1, 2, 0] },
  { id: 'contacto', label: 'Contacto', position: [3, 2, 0] },
];

function MenuItem({ item, selected, onSelect, index }) {
  const ref = useRef();
  const [hovered, setHovered] = useState(false);
  const { camera } = useThree();
  
  // Efecto de hover
  useEffect(() => {
    if (hovered) {
      gsap.to(ref.current.position, {
        y: item.position[1] + 0.3,
        duration: 0.5,
        ease: 'power2.out'
      });
      gsap.to(ref.current.scale, {
        x: 1.2,
        y: 1.2,
        z: 1.2,
        duration: 0.3,
        ease: 'back.out'
      });
    } else {
      gsap.to(ref.current.position, {
        y: item.position[1],
        duration: 0.5,
        ease: 'power2.out'
      });
      gsap.to(ref.current.scale, {
        x: 1,
        y: 1,
        z: 1,
        duration: 0.3,
        ease: 'power2.out'
      });
    }
  }, [hovered, item.position]);
  
  // Efecto de selección
  useEffect(() => {
    if (selected) {
      gsap.to(ref.current.rotation, {
        y: Math.PI * 2,
        duration: 1,
        ease: 'elastic.out(1, 0.3)'
      });
      
      // Mover la cámara para enfocar el elemento seleccionado
      gsap.to(camera.position, {
        x: item.position[0] * 0.8,
        y: item.position[1] * 0.8,
        z: 5,
        duration: 1.5,
        ease: 'power2.inOut'
      });
    }
  }, [selected, camera, item.position]);

  // Animación de aparición inicial
  useEffect(() => {
    ref.current.position.y = item.position[1] - 10;
    ref.current.scale.set(0.5, 0.5, 0.5);
    
    gsap.to(ref.current.position, {
      y: item.position[1],
      duration: 1,
      delay: index * 0.2,
      ease: 'elastic.out(1, 0.5)'
    });
    
    gsap.to(ref.current.scale, {
      x: 1,
      y: 1,
      z: 1,
      duration: 0.8,
      delay: index * 0.2,
      ease: 'back.out(1.7)'
    });
  }, [index, item.position]);

  return (
    <group
      ref={ref}
      position={[item.position[0], item.position[1], item.position[2]]}
      onClick={() => onSelect(item.id)}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <mesh>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial 
          color={selected ? '#ffaa00' : hovered ? '#2196f3' : '#ffffff'} 
          roughness={0.3}
          metalness={0.7}
          emissive={selected ? '#ff8800' : hovered ? '#0066cc' : '#000000'}
          emissiveIntensity={selected ? 0.5 : hovered ? 0.3 : 0}
        />
      </mesh>
      <Text
        position={[0, -0.8, 0]}
        fontSize={0.3}
        color={selected ? '#ffaa00' : hovered ? '#2196f3' : '#ffffff'}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        {item.label}
      </Text>
    </group>
  );
}

function ImmersiveMenu() {
  const [selectedItem, setSelectedItem] = useState(null);
  const groupRef = useRef();
  
  // Animación de flotación del menú
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.position.y = Math.sin(state.clock.getElapsedTime() * 0.5) * 0.1;
    }
  });
  
  const handleSelect = (id) => {
    setSelectedItem(id);
    // Aquí podrías implementar la navegación o carga de contenido
    console.log(`Seleccionado: ${id}`);
  };
  
  return (
    <group ref={groupRef} position={[0, 0, -2]}>
      {menuItems.map((item, index) => (
        <MenuItem 
          key={item.id}
          item={item}
          index={index}
          selected={selectedItem === item.id}
          onSelect={handleSelect}
        />
      ))}
    </group>
  );
}

export default ImmersiveMenu; 