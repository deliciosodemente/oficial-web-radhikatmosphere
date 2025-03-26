import React, { Suspense, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  OrbitControls, 
  PerspectiveCamera, 
  Environment, 
  useGLTF, 
  useTexture,
  Sky,
  Effects,
  PerformanceMonitor
} from '@react-three/drei';
import { EffectComposer, Bloom, Vignette } from '@react-three/postprocessing';
import CloudBackground from './CloudBackground';
import ImmersiveMenu from './ImmersiveMenu';
import * as THREE from 'three';

// Componente para el suelo reflectante
function Floor() {
  const floorRef = useRef();
  
  return (
    <mesh 
      ref={floorRef} 
      rotation={[-Math.PI / 2, 0, 0]} 
      position={[0, -2, 0]}
      receiveShadow
    >
      <planeGeometry args={[100, 100]} />
      <meshStandardMaterial 
        color="#87CEEB" 
        metalness={0.4}
        roughness={0.1}
        transparent
        opacity={0.6}
      />
    </mesh>
  );
}

// Componente para optimizar la escena
function SceneOptimizer() {
  const { gl, scene, camera } = useThree();
  
  useEffect(() => {
    // Habilitar manejo de sombras
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
    
    // Configurar renderización adaptativa
    gl.setPixelRatio(window.devicePixelRatio);
    
    // Configurar el fondo
    scene.background = new THREE.Color('#87CEEB');
    
    // Optimizar físicas
    scene.matrixAutoUpdate = false;
    
    return () => {
      gl.shadowMap.enabled = false;
    };
  }, [gl, scene]);
  
  // Implementar frustum culling
  useFrame(() => {
    scene.traverse(object => {
      if (object.isMesh) {
        object.frustumCulled = true;
      }
    });
  });
  
  return null;
}

// Componente para manejo adaptativo de calidad
function AdaptiveQuality() {
  const [degraded, degrade] = React.useState(false);
  
  return (
    <PerformanceMonitor 
      onDecline={() => degrade(true)}
      onIncline={() => degrade(false)}
    >
      {degraded && (
        <EffectComposer multisampling={0}>
          <Bloom luminanceThreshold={0.2} intensity={0.5} />
        </EffectComposer>
      )}
      {!degraded && (
        <EffectComposer multisampling={4}>
          <Bloom luminanceThreshold={0.2} intensity={1.0} />
          <Vignette eskil={false} offset={0.1} darkness={0.8} />
        </EffectComposer>
      )}
    </PerformanceMonitor>
  );
}

function LoadingScreen() {
  return (
    <Html center>
      <div style={{ 
        color: 'white', 
        background: 'rgba(0,0,0,0.7)', 
        padding: '20px 40px',
        borderRadius: '10px',
        fontFamily: 'Arial',
        textAlign: 'center' 
      }}>
        <h2>Cargando mundo inmersivo...</h2>
        <div style={{
          width: '150px',
          height: '8px',
          background: 'rgba(255,255,255,0.2)',
          borderRadius: '4px',
          overflow: 'hidden',
          position: 'relative',
          margin: '10px auto'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            height: '100%',
            width: '30%',
            background: '#2196f3',
            borderRadius: '4px',
            animation: 'loading 1.5s infinite ease-in-out'
          }} />
        </div>
        <style>
          {`
            @keyframes loading {
              0% { left: -30%; }
              100% { left: 100%; }
            }
          `}
        </style>
      </div>
    </Html>
  );
}

function ImmersiveScene() {
  return (
    <Canvas shadows dpr={[1, 2]}>
      <SceneOptimizer />
      
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
      
      <directionalLight
        position={[10, 20, 15]}
        intensity={1.5}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <ambientLight intensity={0.4} />
      <pointLight position={[-10, 0, -10]} intensity={0.5} color="#0066ff" />
      
      <Suspense fallback={<LoadingScreen />}>
        <Sky 
          distance={450000} 
          sunPosition={[10, 4, 1]} 
          inclination={0.5}
          turbidity={8}
          rayleigh={6}
          mieCoefficient={0.005}
          mieDirectionalG={0.8}
        />
        <CloudBackground />
        <ImmersiveMenu />
        <Floor />
        <AdaptiveQuality />
      </Suspense>
    </Canvas>
  );
}

export default ImmersiveScene; 