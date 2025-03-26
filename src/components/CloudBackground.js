import React, { useRef, useMemo, useEffect } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import { useTexture } from '@react-three/drei';
import * as THREE from 'three';

function CloudBackground() {
  const { scene } = useThree();
  const cloudParticlesRef = useRef([]);
  const cloudMaterialRef = useRef();
  
  // Cargar la textura de nubes
  const cloudTexture = useTexture('/assets/textures/cloud.svg');
  
  useEffect(() => {
    // Configurar escena para un aspecto atmosférico
    scene.fog = new THREE.FogExp2(0x87ceeb, 0.0005);
    
    // Crear partículas de nubes
    const cloudGeo = new THREE.PlaneGeometry(500, 500);
    const cloudMaterial = new THREE.MeshLambertMaterial({
      map: cloudTexture,
      transparent: true,
      opacity: 0.6
    });
    
    cloudMaterialRef.current = cloudMaterial;
    
    // Crear múltiples nubes con posiciones aleatorias
    for (let p = 0; p < 50; p++) {
      const cloud = new THREE.Mesh(cloudGeo, cloudMaterial);
      cloud.position.set(
        Math.random() * 800 - 400,
        500,
        Math.random() * 500 - 500
      );
      cloud.rotation.x = 1.16;
      cloud.rotation.y = -0.12;
      cloud.rotation.z = Math.random() * 2 * Math.PI;
      cloud.material.opacity = 0.55;
      cloudParticlesRef.current.push(cloud);
      scene.add(cloud);
    }
    
    // Limpieza al desmontar
    return () => {
      cloudParticlesRef.current.forEach(cloud => {
        scene.remove(cloud);
      });
      scene.fog = null;
    };
  }, [scene, cloudTexture]);
  
  // Animar las nubes
  useFrame(() => {
    cloudParticlesRef.current.forEach(cloud => {
      cloud.rotation.z += 0.001;
      // Mover las nubes lentamente
      cloud.position.y -= 0.1;
      // Si la nube ha bajado demasiado, reubicarla arriba
      if (cloud.position.y < -100) {
        cloud.position.y = 500;
      }
    });
  });
  
  return null; // Este componente solo maneja efectos visuales, no renderiza nada directamente
}

export default CloudBackground; 